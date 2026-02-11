# Market Dashboard Backend

FastAPI 기반 금융 데이터 API 서버

## 🚀 빠른 시작

### 1. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 서버 실행

```bash
python main.py
```

서버가 `http://localhost:8000` 에서 실행됩니다.

## 📚 API 문서

서버 실행 후 브라우저에서:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔌 API 엔드포인트

### 시장 데이터
- `GET /api/market/korea` - KOSPI, KOSDAQ
- `GET /api/market/us` - S&P500, NASDAQ, DOW, VIX
- `GET /api/dashboard` - 모든 데이터 한번에

### 경제 지표
- `GET /api/fear-greed` - Fear & Greed Index
- `GET /api/forex` - USD/KRW 환율
- `GET /api/gold` - 금 가격
- `GET /api/forex-gold` - 환율 + 금 가격

### 뉴스
- `GET /api/news` - 모든 뉴스 (CNBC, Bloomberg, WSJ)
- `GET /api/news/{source}` - 특정 소스 (cnbc, bloomberg, wsj)
  - 쿼리 파라미터: `limit` (기본값: 5)

## 📁 프로젝트 구조

```
backend/
├── main.py              # 메인 애플리케이션
├── requirements.txt     # 의존성 패키지
├── api/
│   └── routes.py       # API 라우터
└── services/
    ├── korea_market.py  # 한국 시장 데이터
    ├── us_market.py     # 미국 시장 데이터
    ├── fear_greed.py    # Fear & Greed Index
    ├── forex_gold.py    # 환율 & 금
    └── news.py          # 뉴스 RSS
```

## 🔧 개발 모드

자동 재시작 활성화:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 참고사항

- pykrx는 한국 주말/공휴일에 데이터가 없을 수 있습니다
- yfinance는 미국 장 마감 후 데이터가 지연될 수 있습니다
- RSS 피드는 각 언론사 정책에 따라 변경될 수 있습니다
