# Market Dashboard Frontend

React + TypeScript + Tailwind CSS로 만든 금융 시장 대시보드

## 🚀 빠른 시작

### 1. 패키지 설치

```bash
npm install
```

### 2. 개발 서버 실행

```bash
npm run dev
```

앱이 `http://localhost:3000`에서 실행됩니다.

## 🏗️ 빌드

프로덕션 빌드:
```bash
npm run build
```

빌드 미리보기:
```bash
npm run preview
```

## 📁 프로젝트 구조

```
frontend/
├── src/
│   ├── components/
│   │   ├── MarketCard.tsx       # 시장 데이터 카드
│   │   ├── FearGreedGauge.tsx   # Fear & Greed 게이지
│   │   └── NewsFeed.tsx         # 뉴스 피드
│   ├── services/
│   │   └── api.ts              # API 통신
│   ├── App.tsx                 # 메인 앱
│   ├── main.tsx               # 엔트리 포인트
│   └── index.css              # 글로벌 스타일
├── public/                    # 정적 파일
├── index.html
└── package.json
```

## 🎨 주요 기능

### 화면 구성
1. **한국 시장**: KOSPI, KOSDAQ
2. **미국 시장**: S&P500, NASDAQ, DOW, VIX
3. **경제 지표**: Fear & Greed Index, USD/KRW, 금 가격
4. **뉴스**: CNBC, Bloomberg, WSJ 헤드라인

### 기능
- ✅ 자동 새로고침 (5분마다)
- ✅ 수동 새로고침 버튼
- ✅ Pull-to-refresh (모바일)
- ✅ 반응형 디자인
- ✅ Material Design 3 스타일

## 🔧 환경 변수

`.env` 파일 생성:
```env
VITE_API_URL=http://localhost:8000
```

## 📱 PWA 변환 (나중에)

PWA로 만들려면:
1. `vite-plugin-pwa` 설치
2. `manifest.json` 설정
3. Service Worker 등록

## 🎯 다음 단계

- [ ] 로그인/회원가입
- [ ] 개인화 설정
- [ ] 푸시 알림
- [ ] 오프라인 지원
- [ ] 다크 모드
