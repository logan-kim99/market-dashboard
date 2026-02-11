import yfinance as yf
import requests
from datetime import datetime

class ForexGoldService:
    """환율 및 금 가격 서비스"""
    
    def get_forex(self):
        """USD/KRW 환율 가져오기"""
        try:
            # yfinance로 환율 데이터 가져오기
            ticker = yf.Ticker("KRW=X")
            hist = ticker.history(period="2d")
            
            if hist.empty:
                return self._fallback_forex()
            
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2] if len(hist) > 1 else hist['Open'].iloc[-1]
            change = current - prev
            change_percent = (change / prev) * 100 if prev != 0 else 0
            
            return {
                "success": True,
                "data": {
                    "pair": "USD/KRW",
                    "rate": round(float(current), 2),
                    "change": round(float(change), 2),
                    "change_percent": round(float(change_percent), 2),
                    "updated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"Error fetching forex: {e}")
            return self._fallback_forex()
    
    def get_gold(self):
        """금 가격 가져오기 (온스당 USD)"""
        try:
            # GC=F: Gold Futures
            ticker = yf.Ticker("GC=F")
            hist = ticker.history(period="2d")
            
            if hist.empty:
                return self._fallback_gold()
            
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2] if len(hist) > 1 else hist['Open'].iloc[-1]
            change = current - prev
            change_percent = (change / prev) * 100 if prev != 0 else 0
            
            return {
                "success": True,
                "data": {
                    "name": "Gold (XAU/USD)",
                    "price": round(float(current), 2),
                    "change": round(float(change), 2),
                    "change_percent": round(float(change_percent), 2),
                    "unit": "USD per Troy Ounce",
                    "updated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"Error fetching gold price: {e}")
            return self._fallback_gold()
    
    def get_all(self):
        """환율과 금 가격 모두 가져오기"""
        return {
            "forex": self.get_forex(),
            "gold": self.get_gold()
        }
    
    def _fallback_forex(self):
        """환율 대체 데이터"""
        return {
            "success": False,
            "data": {
                "pair": "USD/KRW",
                "rate": 0,
                "change": 0,
                "change_percent": 0,
                "updated_at": datetime.now().isoformat()
            },
            "error": "Failed to fetch forex data"
        }
    
    def _fallback_gold(self):
        """금 가격 대체 데이터"""
        return {
            "success": False,
            "data": {
                "name": "Gold (XAU/USD)",
                "price": 0,
                "change": 0,
                "change_percent": 0,
                "unit": "USD per Troy Ounce",
                "updated_at": datetime.now().isoformat()
            },
            "error": "Failed to fetch gold price"
        }
