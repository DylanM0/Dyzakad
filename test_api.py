import requests
import json
from dotenv import load_dotenv
import os
import urllib3

# SSL 경고 메시지 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# .env 파일 로드
load_dotenv()

# API 설정
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')

# API 타입 정의
API_TYPES = {
    '학교기본정보': '0',
    '수업일수 및 수업시수 현황': '08',
    '자유학기제 운영': '04',
    '학교 현황': '62',
    '성별 학생수': '63',
    '학년별·학급별 학생수': '09',
    '전·출입 및 학업중단 학생 수': '10',
    '직위별 교원 현황': '22',
    '자격종별 교원 현황': '64',
    '표시과목별 교원 현황': '24',
    '학교폭력 예방교육 실적': '94',
    '입학생 현황': '51'
}

def test_api(api_type, school_type='02', year='2024'):
    """각 API의 응답을 테스트하고 컬럼 정보를 출력합니다."""
    url = f"{BASE_URL}?apiKey={API_KEY}&apiType={api_type}&pbanYr={year}&schulKndCode={school_type}"
    
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            data = response.json()
            if data.get('resultCode') == 'success' and 'list' in data and data['list']:
                print(f"\n=== API 타입: {api_type} ===")
                # 첫 번째 항목의 모든 키를 출력
                sample_item = data['list'][0]
                print("\n컬럼 목록:")
                for key in sample_item.keys():
                    print(f"'{key}': '',")
            else:
                print(f"\nAPI 타입 {api_type}: 데이터 없음")
        else:
            print(f"\nAPI 타입 {api_type}: 응답 오류 {response.status_code}")
    except Exception as e:
        print(f"\nAPI 타입 {api_type}: 오류 발생 - {str(e)}")

def main():
    print("=== API 응답 테스트 시작 ===")
    for api_name, api_type in API_TYPES.items():
        print(f"\n테스트 중: {api_name} ({api_type})")
        test_api(api_type)

if __name__ == "__main__":
    main() 