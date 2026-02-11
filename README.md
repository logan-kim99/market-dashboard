# 📊 Market Dashboard

> 한국 및 미국 주식시장, 경제 지표, 실시간 뉴스를 한눈에 보는 금융 대시보드

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18+-61dafb.svg)

## ✨ 주요 기능

- 🇰🇷 **한국 시장**: KOSPI, KOSDAQ 실시간 지수
- 🇺🇸 **미국 시장**: S&P 500, NASDAQ, DOW Jones, VIX
- 📈 **경제 지표**: Fear & Greed Index, USD/KRW 환율, 금 가격
- 📰 **뉴스**: CNBC, Bloomberg, WSJ 최신 헤드라인
- 🔄 **자동 업데이트**: 5분마다 자동 새로고침
- 📱 **반응형**: 모바일, 태블릿, 데스크톱 지원

## 🏗️ 기술 스택

### Backend
- **FastAPI** - 고성능 Python 웹 프레임워크
- **pykrx** - 한국 주식 데이터
- **yfinance** - 미국 주식 데이터
- **feedparser** - RSS 뉴스 파싱

### Frontend
- **React 18** + **TypeScript**
- **Tailwind CSS** - 유틸리티 CSS
- **React Query** - 서버 상태 관리
- **Recharts** - 차트 라이브러리
- **Vite** - 빌드 도구

## 🚀 빠른 시작

### 1️⃣ 백엔드 실행

```bash
cd backend

# 가상환경 생성 및 활성화 (Windows)
python -m venv venv
venv\Scripts\activate

# 가상환경 생성 및 활성화 (Mac/Linux)
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
python main.py
```

백엔드가 `http://localhost:8000`에서 실행됩니다.

API 문서: `http://localhost:8000/docs`

### 2️⃣ 프론트엔드 실행

```bash
cd frontend

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드가 `http://localhost:3000`에서 실행됩니다.

## 📁 프로젝트 구조

```
market-dashboard/
├── backend/                 # FastAPI 백엔드
│   ├── main.py             # 메인 앱
│   ├── api/                # API 라우터
│   │   └── routes.py
│   ├── services/           # 데이터 서비스
│   │   ├── korea_market.py
│   │   ├── us_market.py
│   │   ├── fear_greed.py
│   │   ├── forex_gold.py
│   │   └── news.py
│   └── requirements.txt
│
└── frontend/               # React 프론트엔드
    ├── src/
    │   ├── components/     # UI 컴포넌트
    │   ├── services/       # API 통신
    │   ├── App.tsx        # 메인 앱
    │   └── main.tsx       # 엔트리 포인트
    └── package.json
```

## 🔌 API 엔드포인트

| 엔드포인트 | 설명 |
|-----------|------|
| `GET /api/dashboard` | 모든 데이터 한번에 |
| `GET /api/market/korea` | 한국 시장 (KOSPI, KOSDAQ) |
| `GET /api/market/us` | 미국 시장 (S&P500, NASDAQ, DOW, VIX) |
| `GET /api/fear-greed` | Fear & Greed Index |
| `GET /api/forex` | USD/KRW 환율 |
| `GET /api/gold` | 금 가격 |
| `GET /api/news` | 모든 뉴스 |

## 🎯 Claude Code & Cursor 협업 워크플로우

### **Claude Code 역할** (터미널)
```bash
# 1. 프로젝트 초기화
claude-code "Initialize project structure"

# 2. 새로운 API 엔드포인트 추가
claude-code "Add endpoint for Bitcoin price"

# 3. 데이터 수집 로직 개선
claude-code "Optimize data fetching with caching"

# 4. 테스트 실행
claude-code "Run unit tests for all services"
```

### **Cursor 역할** (IDE)
- 프론트엔드 UI 세밀 조정
- 컴포넌트 리팩토링
- 스타일링 개선
- 버그 수정

## 📱 다음 단계 (Phase 2)

### MVP 완성 후 추가할 기능
- [ ] PWA 변환 (홈 화면에 추가)
- [ ] 푸시 알림
- [ ] 다크 모드
- [ ] 커스텀 워치리스트
- [ ] 로그인/회원가입
- [ ] 구독제 시스템
- [ ] 앱스토어 배포

## 🐛 문제 해결

### 백엔드 서버가 안 열릴 때
```bash
# 포트 8000이 사용 중인지 확인
# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000
```

### pykrx 데이터가 안 받아질 때
- 한국 주말/공휴일에는 데이터가 없을 수 있습니다
- 최근 거래일 데이터를 가져오도록 구현되어 있습니다

### CORS 에러
- 백엔드 main.py의 `allow_origins`에 프론트엔드 URL 추가

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

---

**Made with ❤️ by Claude Code + Cursor**
