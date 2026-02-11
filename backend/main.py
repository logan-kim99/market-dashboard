import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from api.routes import router, refresh_all_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시: 초기 캐시 채우기 + 스케줄러 시작
    logger.info("서버 시작 - 초기 데이터 캐시 수집 중...")
    refresh_all_cache()
    scheduler.add_job(refresh_all_cache, "interval", minutes=5, id="refresh_cache")
    scheduler.start()
    logger.info("스케줄러 시작 (5분 간격 자동 갱신)")
    yield
    # 서버 종료 시: 스케줄러 정리
    scheduler.shutdown(wait=False)
    logger.info("스케줄러 종료")


app = FastAPI(
    title="Market Dashboard API",
    description="Real-time market data API for Korea, US markets, and economic indicators",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 설정 (프론트엔드 연결용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Market Dashboard API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "korea_market": "/api/market/korea",
            "us_market": "/api/market/us",
            "fear_greed": "/api/fear-greed",
            "forex": "/api/forex",
            "gold": "/api/gold",
            "forex_gold": "/api/forex-gold",
            "news": "/api/news",
            "dashboard": "/api/dashboard (모든 데이터 한번에)"
        },
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
