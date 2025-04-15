import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
import json
import urllib3
import io

# SSL 경고 메시지 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# .env 파일 로드
load_dotenv()

# API 설정
API_KEY = st.secrets["API_KEY"] if "API_KEY" in st.secrets else os.getenv('API_KEY')
BASE_URL = st.secrets["BASE_URL"] if "BASE_URL" in st.secrets else os.getenv('BASE_URL')

# API 타입 정의
API_TYPES = {
    '학교기본정보': '0',               # 학교기본정보
    '수업일수 및 수업시수 현황': '08',  # 수업일수 및 수업시수 현황
    '자유학기제 운영': '04',          # 자유학기제 운영에 관한 사항
    '학교 현황': '62',               # 학교 현황
    '성별 학생수': '63',             # 성별 학생수
    '학년별·학급별 학생수': '09',     # 학년별·학급별 학생수
    '전·출입 및 학업중단 학생 수': '10', # 전·출입 및 학업중단 학생 수
    '직위별 교원 현황': '22',         # 직위별 교원 현황
    '자격종별 교원 현황': '64',       # 자격종별 교원 현황
    '표시과목별 교원 현황': '24',      # 표시과목별 교원 현황
    '학교폭력 예방교육 실적': '94',    # 대상별 학교폭력 예방교육 실적
    '입학생 현황': '51'              # 입학생 현황
}

# 학교급 코드 정의
SCHOOL_TYPES = {
    '초등학교': '02',
    '중학교': '03',
    '고등학교': '04'
}

# 컬럼 헤더 한글 매핑
COLUMN_MAPPINGS = {
    # 학교기본정보 (0)
    'ATPT_OFCDC_ORG_NM': '시도교육청',
    'ATPT_OFCDC_ORG_CODE': '시도교육청코드',
    'JU_ORG_NM': '교육지원청',
    'JU_ORG_CODE': '교육지원청코드',
    'ADRCD_NM': '지역',
    'ADRCD_CD': '지역코드',
    'LCTN_SC_CODE': '소재지구분코드',
    'SCHUL_CODE': '정보공시 학교코드',
    'SCHUL_NM': '학교명',
    'SCHUL_KND_SC_CODE': '학교급코드',
    'FOND_SC_CODE': '설립구분',
    'HS_KND_SC_NM': '학교특성',
    'BNHH_YN': '분교여부',
    'SCHUL_FOND_TYP_CODE': '설립유형',
    'DGHT_SC_CODE': '주야구분',
    'FOAS_MEMRD': '개교기념일',
    'FOND_YMD': '설립일',
    'ADRCD_ID': '법정동코드',
    'ADRES_BRKDN': '주소내역',
    'DTLAD_BRKDN': '상세주소내역',
    'ZIP_CODE': '우편번호',
    'SCHUL_RDNZC': '학교도로명 우편번호',
    'SCHUL_RDNMA': '학교도로명 주소',
    'SCHUL_RDNDA': '학교도로명 상세주소',
    'LTTUD': '위도',
    'LGTUD': '경도',
    'USER_TELNO': '전화번호',
    'USER_TELNO_SW': '전화번호(교무실)',
    'USER_TELNO_GA': '전화번호(행정실)',
    'PERC_FAXNO': '팩스번호',
    'HMPG_ADRES': '홈페이지 주소',
    'COEDU_SC_CODE': '남녀공학 구분',
    'ABSCH_YN': '폐교여부',
    'ABSCH_YMD': '폐교일자',
    'CLOSE_YN': '휴교여부',
    'SCHUL_CRSE_SC_VALUE': '학교과정구분값(2-3-4)',
    'SCHUL_CRSE_SC_VALUE_NM': '학교과정구분명(초-중-고)',

    # 수업일수 및 수업시수 현황 (08)
    'COL_1': '1학년',
    'COL_2': '2학년',
    'COL_3': '3학년',
    'COL_4': '4학년',
    'COL_5': '5학년',
    'COL_6': '6학년',
    'PER_STUDAY_DAY': '주당평균수업시수(교사 1인당)',
    'WEEK_TOT_ITRT_HR_FGR': '주당수업시수',
    'ITRT_TCR_TOT_FGR': '수업교원수',
    'SCHUL_CRSE_SC_CODE_P': '학교과정구분(초등)',
    'COL_1_P': '1학년(초등)',
    'COL_2_P': '2학년(초등)',
    'COL_3_P': '3학년(초등)',
    'COL_4_P': '4학년(초등)',
    'COL_5_P': '5학년(초등)',
    'COL_6_P': '6학년(초등)',
    'SCHUL_CRSE_SC_CODE_M': '학교과정구분(중등)',
    'COL_1_M': '1학년(중등)',
    'COL_2_M': '2학년(중등)',
    'COL_3_M': '3학년(중등)',
    'SCHUL_CRSE_SC_CODE_H': '학교과정구분(고등)',
    'COL_1_H': '1학년(고등)',
    'COL_2_H': '2학년(고등)',
    'COL_3_H': '3학년(고등)',

    # 자유학기제 운영 (04)
    'SCHUL_CRSE_SC_CODE': '학교과정구분코드',
    'FREE_SEM_DGST': '자유학기 요약',
    'FREE_SEM_DETAIL': '자유학기 상세내용',
    
    # 학교 현황 (62)
    'COL_1': '1학년',
    'COL_2': '2학년',
    'COL_3': '3학년',
    'COL_4': '4학년',
    'COL_5': '5학년',
    'COL_6': '6학년',
    'COL_7': '7학년',
    'COL_8': '8학년',
    'COL_SUM': '학년별 합계',
    'COL_FGR_SUM': '전체 합계',
    'AVG_FGR_SUM': '평균',
    'SP_SUM': '특수학급 합계',
    'SP_FGR_SUM': '특수학급 전체 합계',
    
    # 성별 학생수 (63)
    'COL_M1': '1학년 남학생수',
    'COL_M2': '2학년 남학생수',
    'COL_M3': '3학년 남학생수',
    'COL_M4': '4학년 남학생수',
    'COL_M5': '5학년 남학생수',
    'COL_M6': '6학년 남학생수',
    'COL_M7': '7학년 남학생수',
    'COL_M8': '8학년 남학생수',
    'COL_MSUM': '남학생 총계',
    'COL_W1': '1학년 여학생수',
    'COL_W2': '2학년 여학생수',
    'COL_W3': '3학년 여학생수',
    'COL_W4': '4학년 여학생수',
    'COL_W5': '5학년 여학생수',
    'COL_W6': '6학년 여학생수',
    'COL_W7': '7학년 여학생수',
    'COL_W8': '8학년 여학생수',
    'COL_WSUM': '여학생 총계',
    'SUM': '전체 학생수',
    
    # 학년별·학급별 학생수 (09)
    'COL_1': '1학년 학생수',
    'COL_2': '2학년 학생수',
    'COL_3': '3학년 학생수',
    'COL_4': '4학년 학생수',
    'COL_5': '5학년 학생수',
    'COL_6': '6학년 학생수',
    'COL_7': '7학년 학생수',
    'COL_8': '8학년 학생수',
    'COL_SUM': '전체 학생수',
    'COL_C1': '1학년 학급수',
    'COL_C2': '2학년 학급수',
    'COL_C3': '3학년 학급수',
    'COL_C4': '4학년 학급수',
    'COL_C5': '5학년 학급수',
    'COL_C6': '6학년 학급수',
    'COL_C7': '7학년 학급수',
    'COL_C8': '8학년 학급수',
    'COL_C_SUM': '전체 학급수',
    'TEACH_CNT': '교원수',
    'TEACH_CAL': '교원 1인당 학생수',
    
    # 전·출입 및 학업중단 학생 수 (10)
    'COL_211': '초등부1학년 전입학생수',
    'COL_212': '초등부1학년 전출학생수',
    'COL_221': '초등부2학년 전입학생수',
    'COL_222': '초등부2학년 전출학생수',
    'COL_231': '초등부3학년 전입학생수',
    'COL_232': '초등부3학년 전출학생수',
    'COL_241': '초등부4학년 전입학생수',
    'COL_242': '초등부4학년 전출학생수',
    'COL_251': '초등부5학년 전입학생수',
    'COL_252': '초등부5학년 전출학생수',
    'COL_261': '초등부6학년 전입학생수',
    'COL_262': '초등부6학년 전출학생수',
    'MVIN_SUM': '전입학생수(계)',
    'MVT_SUM': '전출학생수(계)',
    'STDNT_SUM': '전체학생수(계)',
    
    # 직위별 교원 현황 (22)
    'COL_1': '교장',
    'COL_2': '교감',
    'COL_3': '수석교사',
    'COL_4': '보직교사',
    'COL_5': '교사',
    'COL_6': '특수교사',
    'COL_7': '전문상담교사',
    'COL_8': '사서교사',
    'COL_9': '실기교사',
    'COL_10': '보건교사',
    'COL_11': '영양교사',
    'COL_13': '기간제교사',
    'COL_14': '강사',
    'COL_15': '기타',
    
    # 자격종별 교원 현황 (64)
    'COL_1': '정교사(1급)',
    'COL_2': '정교사(2급)',
    'COL_3': '준교사',
    'COL_4': '전문상담교사(1급)',
    'COL_5': '전문상담교사(2급)',
    'COL_6': '사서교사(1급)',
    'COL_7': '사서교사(2급)',
    'COL_8': '실기교사',
    'COL_9': '보건교사(1급)',
    'COL_10': '보건교사(2급)',
    'COL_11': '영양교사(1급)',
    'COL_19': '영양교사(2급)',
    'COL_20': '특수학교(1급)',
    'COL_21': '특수학교(2급)',
    
    # 학교폭력 예방교육 실적 (94)
    'SEM_SC_CODE': '학기구분코드',
    'SEM_SC_NM': '학기구분명',
    'TOT_AVG_TM': '총 평균시간',
    'FRL_CURR_ITRT_TM': '정규교과 시간',
    'NN_FRL_CURR_ITRT_TM': '비정규교과 시간',
    'PTPT_NMPR_FGR1': '1학기 참여인원',
    'PTPT_NMPR_FGR2': '2학기 참여인원',
    'PTPT_NMPR_PER1': '1학기 참여율',
    'PTPT_NMPR_PER2': '2학기 참여율',
    
    # 입학생 현황 (51)
    'BEAGE_BOY_FGR': '적정연령 남학생수',
    'BEAGE_GIR_FGR': '적정연령 여학생수',
    'ELPD_ETRC_BOY_FGR': '조기입학 남학생수',
    'ELPD_ETRC_GIR_FGR': '조기입학 여학생수',
    'HEST_AWA_LTAGE_BOY_FGR': '취학유예 남학생수',
    'HEST_AWA_LTAGE_GIR_FGR': '취학유예 여학생수',
    'TOT_SUM': '전체 합계',
    'TOTAL_1': '1학기 전체',
    'TOTAL_2': '2학기 전체',
    
    # 공통 필드 (여러 API에서 사용)
    'PBAN_EXCP_YN': '제외여부',
    'PBAN_EXCP_RSN': '제외사유'
}

def fetch_school_data(api_type, school_type, year):
    """API를 통해 학교 데이터를 가져옵니다."""
    url = f"{BASE_URL}?apiKey={API_KEY}&apiType={api_type}&pbanYr={year}&schulKndCode={school_type}"
    
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            try:
                # JSON 데이터 가져오기
                data = response.json()
                
                # 실제 데이터는 'list' 키에 있음
                if data.get('resultCode') == 'success' and 'list' in data:
                    df = pd.DataFrame(data['list'])
                    # 컬럼명을 한글로 변환
                    df = translate_columns(df)
                    return df
                
                st.error("데이터를 찾을 수 없습니다.")
                return None
                
            except Exception as e:
                st.error(f"데이터 파싱 중 오류 발생: {str(e)}")
                return None
        else:
            st.error(f"API 응답 오류: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"데이터 조회 중 오류가 발생했습니다: {str(e)}")
        return None

def translate_columns(df):
    """데이터프레임의 컬럼명을 한글로 변환합니다."""
    if df is None or df.empty:
        return df
    
    # 컬럼명 변환
    new_columns = {}
    for col in df.columns:
        if col in COLUMN_MAPPINGS:
            new_columns[col] = COLUMN_MAPPINGS[col]
        else:
            new_columns[col] = col  # 매핑이 없는 경우 원래 이름 유지
    
    return df.rename(columns=new_columns)

def main():
    st.title("🏫 전국 학교 정보 대시보드")
    
    # 사이드바 설정
    st.sidebar.header("검색 조건")
    
    # 조회 연도 선택
    year = st.sidebar.selectbox(
        "조회 연도",
        options=list(range(2024, 2019, -1))
    )
    
    # 학교급 선택
    selected_school_type = st.sidebar.selectbox(
        "학교급",
        options=list(SCHOOL_TYPES.keys())
    )
    
    # API 타입 선택
    selected_api_type = st.sidebar.selectbox(
        "조회할 정보",
        options=list(API_TYPES.keys())
    )
    
    # 데이터 조회 버튼
    if st.sidebar.button("데이터 조회"):
        with st.spinner("데이터를 불러오는 중..."):
            df = fetch_school_data(
                API_TYPES[selected_api_type],
                SCHOOL_TYPES[selected_school_type],
                year
            )
            
            if df is not None and not df.empty:
                st.success("데이터를 성공적으로 불러왔습니다!")
                
                # 데이터프레임 표시
                st.subheader("📊 조회 결과")
                st.dataframe(df)
                
                # 엑셀 다운로드 버튼
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='학교정보')
                
                excel_buffer.seek(0)
                st.download_button(
                    label="📥 엑셀 파일로 다운로드",
                    data=excel_buffer,
                    file_name=f"school_data_{year}_{selected_school_type}_{selected_api_type}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                # 기본 통계 정보 표시
                st.subheader("📈 기본 통계")
                st.write(df.describe())
                
            else:
                st.error("데이터를 불러오지 못했습니다.")

if __name__ == "__main__":
    main() 