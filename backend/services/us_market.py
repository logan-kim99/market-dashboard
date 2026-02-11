import yfinance as yf
from datetime import datetime

class USMarketService:
    """미국 주식시장 데이터 서비스"""
    
    def __init__(self):
        self.indices = {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones",
            "^IXIC": "NASDAQ",
            "^VIX": "VIX"  # 변동성 지수도 추가
        }
    
    def get_market_data(self):
        """S&P500, NASDAQ, DOW 현재 데이터 가져오기"""
        try:
            result = {}
            
            for ticker, name in self.indices.items():
                data = self._get_ticker_data(ticker, name)
                result[ticker.replace("^", "").lower()] = data
            
            return {
                "success": True,
                "data": result,
                "updated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def _get_ticker_data(self, ticker, name):
        """개별 티커 데이터 가져오기"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="2d")
            
            if hist.empty:
                return self._empty_data(name)
            
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2] if len(hist) > 1 else hist['Open'].iloc[-1]
            change = current - prev
            change_percent = (change / prev) * 100 if prev != 0 else 0
            
            return {
                "name": name,
                "ticker": ticker,
                "value": round(float(current), 2),
                "change": round(float(change), 2),
                "change_percent": round(float(change_percent), 2),
                "open": round(float(hist['Open'].iloc[-1]), 2),
                "high": round(float(hist['High'].iloc[-1]), 2),
                "low": round(float(hist['Low'].iloc[-1]), 2),
                "volume": int(hist['Volume'].iloc[-1]),
                "previous_close": round(float(prev), 2),
                "status": "open" if self._is_market_open() else "closed"
            }
            
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            return self._empty_data(name)
    
    def _is_market_open(self):
        """미국 시장 개장 여부 확인 (간단 버전)"""
        now = datetime.now()
        # 주말 체크
        if now.weekday() >= 5:
            return False
        # 시간 체크는 나중에 타임존 고려해서 정확히
        return True
    
    def _empty_data(self, name):
        """빈 데이터 반환"""
        return {
            "name": name,
            "value": 0,
            "change": 0,
            "change_percent": 0,
            "status": "unavailable"
        }
