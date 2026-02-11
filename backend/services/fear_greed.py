import requests
from datetime import datetime

class FearGreedService:
    """CNN Fear & Greed Index 서비스"""
    
    def __init__(self):
        # Alternative Fear & Greed Index API (무료)
        self.api_url = "https://api.alternative.me/fng/"
    
    def get_index(self):
        """Fear & Greed Index 데이터 가져오기"""
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                current = data['data'][0]
                
                value = int(current['value'])
                classification = current['value_classification']
                
                return {
                    "success": True,
                    "data": {
                        "value": value,
                        "classification": classification,
                        "description": self._get_description(value),
                        "timestamp": current.get('timestamp', ''),
                        "updated_at": datetime.now().isoformat()
                    }
                }
            else:
                return self._fallback_data()
                
        except Exception as e:
            print(f"Error fetching Fear & Greed Index: {e}")
            return self._fallback_data()
    
    def _get_description(self, value):
        """값에 따른 설명 반환"""
        if value <= 25:
            return "극도의 공포 (Extreme Fear)"
        elif value <= 45:
            return "공포 (Fear)"
        elif value <= 55:
            return "중립 (Neutral)"
        elif value <= 75:
            return "탐욕 (Greed)"
        else:
            return "극도의 탐욕 (Extreme Greed)"
    
    def _fallback_data(self):
        """API 실패 시 대체 데이터"""
        return {
            "success": False,
            "data": {
                "value": 50,
                "classification": "Neutral",
                "description": "데이터를 불러올 수 없습니다",
                "timestamp": "",
                "updated_at": datetime.now().isoformat()
            },
            "error": "Failed to fetch data"
        }
