# 학교 정보 조회 API

학교 기본 정보를 조회하는 API 서비스입니다.

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:
- `.env` 파일에 API 키와 기본 URL이 설정되어 있습니다.

## 실행 방법

```bash
python main.py
```

서버는 기본적으로 http://localhost:8000 에서 실행됩니다.

## API 엔드포인트

### GET /api/school-info

고등학교 기본 정보를 조회합니다.

#### 응답 예시:
```json
{
    "data": "XML 형식의 학교 정보"
}
```

## API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 