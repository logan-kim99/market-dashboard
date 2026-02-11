import yfinance as yf
from datetime import datetime


class KoreaMarketService:
    """한국 주식시장 데이터 서비스 (yfinance 기반)"""

    INDICES = {
        "kospi": {"ticker": "^KS11", "name": "KOSPI"},
        "kosdaq": {"ticker": "^KQ11", "name": "KOSDAQ"},
    }

    def get_market_data(self):
        """KOSPI, KOSDAQ 현재 데이터 가져오기"""
        try:
            kospi_data = self._get_index_data("^KS11", "KOSPI")
            kosdaq_data = self._get_index_data("^KQ11", "KOSDAQ")

            return {
                "success": True,
                "data": {
                    "kospi": kospi_data,
                    "kosdaq": kosdaq_data,
                    "updated_at": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            return {"success": False, "error": str(e), "data": None}

    def _get_index_data(self, ticker: str, name: str) -> dict:
        """개별 지수 데이터 가져오기"""
        try:
            t = yf.Ticker(ticker)
            df = t.history(period="5d")

            # 값이 0인 행 제거 (당일 장 시작 전 등)
            df = df[df["Close"] > 0]

            if df.empty:
                return {
                    "name": name,
                    "value": 0,
                    "change": 0,
                    "change_percent": 0,
                    "status": "closed",
                }

            current = df.iloc[-1]["Close"]
            if len(df) >= 2:
                prev_close = df.iloc[-2]["Close"]
            else:
                prev_close = df.iloc[-1]["Open"]

            change = current - prev_close
            change_percent = (change / prev_close) * 100 if prev_close != 0 else 0

            return {
                "name": name,
                "value": round(float(current), 2),
                "change": round(float(change), 2),
                "change_percent": round(float(change_percent), 2),
                "status": "open",
            }

        except Exception as e:
            print(f"Error fetching {name}: {e}")
            return {
                "name": name,
                "value": 0,
                "change": 0,
                "change_percent": 0,
                "status": "error",
            }
