from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
import httpx
import os
import logging
import json
from typing import Optional

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()

# API 키와 URL 확인
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://open.neis.go.kr/hub/schoolInfo"

if not API_KEY:
    raise RuntimeError("API_KEY가 환경 변수에 설정되어 있어야 합니다.")

app = FastAPI(
    title="School Info API",
    description="학교 정보 조회 API",
    version="1.0.0"
)

# 시도교육청 코드 목록
ATPT_OFCDC_SC_CODES = [
    "B10",  # 서울특별시교육청
    "C10",  # 부산광역시교육청
    "D10",  # 대구광역시교육청
    "E10",  # 인천광역시교육청
    "F10",  # 광주광역시교육청
    "G10",  # 대전광역시교육청
    "H10",  # 울산광역시교육청
    "I10",  # 세종특별자치시교육청
    "J10",  # 경기도교육청
    "K10",  # 강원도교육청
    "M10",  # 충청북도교육청
    "N10",  # 충청남도교육청
    "P10",  # 전라북도교육청
    "Q10",  # 전라남도교육청
    "R10",  # 경상북도교육청
    "S10",  # 경상남도교육청
    "T10",  # 제주특별자치도교육청
]

@app.get("/api/school-info")
async def get_school_info(
    school_name: Optional[str] = Query(None, description="검색할 학교 이름 (부분 검색 가능)")
):
    """
    고등학교 기본 정보를 조회하는 API
    - school_name: 학교 이름으로 검색 (선택사항)
    """
    try:
        # API 요청 파라미터 설정
        params = {
            "KEY": API_KEY,
            "Type": "json",
            "pIndex": "1",
            "pSize": "100",
            "SCHUL_KND_SC_NM": "고등학교"
        }
        
        # 학교 이름이 있는 경우 검색 조건 추가
        if school_name:
            params["SCHUL_NM"] = school_name

        # API 요청 및 응답 처리
        async with httpx.AsyncClient(verify=False) as client:
            logger.info(f"API 요청: URL={BASE_URL}, 파라미터={params}")
            response = await client.get(BASE_URL, params=params)
            
            logger.info(f"API 응답: 상태 코드={response.status_code}")
            logger.info(f"API 응답 내용: {response.text[:200]}...")

            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # 에러 응답 처리
                    if "RESULT" in data:
                        error_msg = data["RESULT"]["MESSAGE"]
                        if "해당하는 데이터가 없습니다" in error_msg:
                            logger.info("검색 결과가 없습니다.")
                            return {"schools": []}
                        else:
                            logger.error(f"API 오류: {error_msg}")
                            raise HTTPException(
                                status_code=500,
                                detail=f"학교알리미 API 오류: {error_msg}"
                            )
                    
                    # 정상 응답 처리
                    if "schoolInfo" in data:
                        school_list = data["schoolInfo"][1]["row"]
                        schools = []
                        for school in school_list:
                            school_info = {
                                "schoolName": school.get("SCHUL_NM", ""),
                                "schoolType": school.get("SCHUL_KND_SC_NM", "고등학교"),
                                "location": f"{school.get('LCTN_SC_NM', '')} {school.get('ATPT_OFCDC_SC_NM', '')}",
                                "foundation": school.get("FOND_SC_NM", ""),
                                "studentCount": school.get("COEDU_SC_NM", "0"),
                                "teacherCount": school.get("HGHT_SC_NM", "0")
                            }
                            schools.append(school_info)
                        return {"schools": schools}
                    else:
                        logger.info("검색 결과가 없습니다.")
                        return {"schools": []}
                        
                except json.JSONDecodeError as e:
                    logger.error(f"JSON 파싱 오류: {str(e)}")
                    raise HTTPException(
                        status_code=500,
                        detail="API 응답을 처리하는 중 오류가 발생했습니다."
                    )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"학교알리미 API 오류: {response.text}"
                )

    except Exception as e:
        logger.error(f"에러 발생: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"서버 오류가 발생했습니다: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 