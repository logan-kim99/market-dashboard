import time
import logging
from fastapi import APIRouter, HTTPException
from services.korea_market import KoreaMarketService
from services.us_market import USMarketService
from services.fear_greed import FearGreedService
from services.forex_gold import ForexGoldService
from services.news import NewsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["market"])

# 서비스 인스턴스
korea_service = KoreaMarketService()
us_service = USMarketService()
fear_greed_service = FearGreedService()
forex_gold_service = ForexGoldService()
news_service = NewsService()

# ── 인메모리 캐시 ──────────────────────────────────
CACHE_TTL = 300  # 5분 (초)

_cache: dict = {
    "dashboard": None,
    "korea": None,
    "us": None,
    "fear_greed": None,
    "forex": None,
    "gold": None,
    "forex_gold": None,
    "news": None,
}
_cache_ts: dict = {k: 0.0 for k in _cache}


def _is_fresh(key: str) -> bool:
    return _cache[key] is not None and (time.time() - _cache_ts[key]) < CACHE_TTL


def refresh_all_cache():
    """모든 데이터를 외부 API에서 가져와 캐시에 저장 (APScheduler에서 호출)"""
    logger.info("캐시 갱신 시작...")
    now = time.time()

    try:
        korea = korea_service.get_market_data()
        _cache["korea"] = korea
        _cache_ts["korea"] = now
    except Exception as e:
        logger.warning(f"한국 시장 데이터 갱신 실패: {e}")

    try:
        us = us_service.get_market_data()
        _cache["us"] = us
        _cache_ts["us"] = now
    except Exception as e:
        logger.warning(f"미국 시장 데이터 갱신 실패: {e}")

    try:
        fg = fear_greed_service.get_index()
        _cache["fear_greed"] = fg
        _cache_ts["fear_greed"] = now
    except Exception as e:
        logger.warning(f"Fear & Greed 갱신 실패: {e}")

    try:
        fxg = forex_gold_service.get_all()
        _cache["forex_gold"] = fxg
        _cache["forex"] = forex_gold_service.get_forex()
        _cache["gold"] = forex_gold_service.get_gold()
        _cache_ts["forex_gold"] = now
        _cache_ts["forex"] = now
        _cache_ts["gold"] = now
    except Exception as e:
        logger.warning(f"환율/금 갱신 실패: {e}")

    try:
        news = news_service.get_all_news(limit=5)
        _cache["news"] = news
        _cache_ts["news"] = now
    except Exception as e:
        logger.warning(f"뉴스 갱신 실패: {e}")

    # 대시보드 종합 캐시
    if _cache["korea"] and _cache["us"] and _cache["fear_greed"] and _cache["forex_gold"] and _cache["news"]:
        _cache["dashboard"] = {
            "success": True,
            "data": {
                "korea_market": _cache["korea"].get("data"),
                "us_market": _cache["us"].get("data"),
                "fear_greed": _cache["fear_greed"].get("data"),
                "forex": _cache["forex_gold"].get("forex", {}).get("data"),
                "gold": _cache["forex_gold"].get("gold", {}).get("data"),
                "news": _cache["news"].get("data"),
            },
        }
        _cache_ts["dashboard"] = now

    logger.info("캐시 갱신 완료")


# ── 라우트 ──────────────────────────────────────────

@router.get("/market/korea")
async def get_korea_market():
    """한국 주식시장 데이터 (KOSPI, KOSDAQ)"""
    if _is_fresh("korea"):
        return _cache["korea"]
    result = korea_service.get_market_data()
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to fetch data"))
    _cache["korea"] = result
    _cache_ts["korea"] = time.time()
    return result


@router.get("/market/us")
async def get_us_market():
    """미국 주식시장 데이터 (S&P500, NASDAQ, DOW, VIX)"""
    if _is_fresh("us"):
        return _cache["us"]
    result = us_service.get_market_data()
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to fetch data"))
    _cache["us"] = result
    _cache_ts["us"] = time.time()
    return result


@router.get("/fear-greed")
async def get_fear_greed():
    """Fear & Greed Index"""
    if _is_fresh("fear_greed"):
        return _cache["fear_greed"]
    result = fear_greed_service.get_index()
    _cache["fear_greed"] = result
    _cache_ts["fear_greed"] = time.time()
    return result


@router.get("/forex")
async def get_forex():
    """USD/KRW 환율"""
    if _is_fresh("forex"):
        return _cache["forex"]
    result = forex_gold_service.get_forex()
    _cache["forex"] = result
    _cache_ts["forex"] = time.time()
    return result


@router.get("/gold")
async def get_gold():
    """금 가격 (XAU/USD)"""
    if _is_fresh("gold"):
        return _cache["gold"]
    result = forex_gold_service.get_gold()
    _cache["gold"] = result
    _cache_ts["gold"] = time.time()
    return result


@router.get("/forex-gold")
async def get_forex_and_gold():
    """환율과 금 가격 함께"""
    if _is_fresh("forex_gold"):
        return _cache["forex_gold"]
    result = forex_gold_service.get_all()
    _cache["forex_gold"] = result
    _cache_ts["forex_gold"] = time.time()
    return result


@router.get("/news")
async def get_all_news(limit: int = 5):
    """모든 뉴스 소스 (CNBC, Bloomberg, WSJ)"""
    if _is_fresh("news"):
        return _cache["news"]
    result = news_service.get_all_news(limit=limit)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to fetch news"))
    _cache["news"] = result
    _cache_ts["news"] = time.time()
    return result


@router.get("/news/{source}")
async def get_news_by_source(source: str, limit: int = 5):
    """특정 소스의 뉴스만 (cnbc, bloomberg, wsj)"""
    result = news_service.get_news_by_source(source, limit=limit)
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error", "Source not found"))
    return result


@router.get("/dashboard")
async def get_dashboard_data():
    """대시보드용 모든 데이터 한번에"""
    if _is_fresh("dashboard"):
        return _cache["dashboard"]

    try:
        korea = _cache["korea"] if _is_fresh("korea") else korea_service.get_market_data()
        us = _cache["us"] if _is_fresh("us") else us_service.get_market_data()
        fear_greed = _cache["fear_greed"] if _is_fresh("fear_greed") else fear_greed_service.get_index()
        forex_gold = _cache["forex_gold"] if _is_fresh("forex_gold") else forex_gold_service.get_all()
        news = _cache["news"] if _is_fresh("news") else news_service.get_all_news(limit=5)

        now = time.time()
        _cache["korea"] = korea; _cache_ts["korea"] = now
        _cache["us"] = us; _cache_ts["us"] = now
        _cache["fear_greed"] = fear_greed; _cache_ts["fear_greed"] = now
        _cache["forex_gold"] = forex_gold; _cache_ts["forex_gold"] = now
        _cache["news"] = news; _cache_ts["news"] = now

        result = {
            "success": True,
            "data": {
                "korea_market": korea.get("data"),
                "us_market": us.get("data"),
                "fear_greed": fear_greed.get("data"),
                "forex": forex_gold.get("forex", {}).get("data"),
                "gold": forex_gold.get("gold", {}).get("data"),
                "news": news.get("data"),
            },
        }
        _cache["dashboard"] = result
        _cache_ts["dashboard"] = now
        return result
    except Exception as e:
        # 캐시에 이전 데이터가 있으면 그걸 반환 (stale but better than nothing)
        if _cache["dashboard"] is not None:
            return _cache["dashboard"]
        raise HTTPException(status_code=500, detail=str(e))
