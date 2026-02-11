import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface MarketData {
  name: string;
  value: number;
  change: number;
  change_percent: number;
  status?: string;
}

export interface KoreaMarketResponse {
  success: boolean;
  data: {
    kospi: MarketData;
    kosdaq: MarketData;
    updated_at: string;
  };
}

export interface USMarketResponse {
  success: boolean;
  data: {
    gspc: MarketData;
    dji: MarketData;
    ixic: MarketData;
    vix: MarketData;
  };
}

export interface FearGreedResponse {
  success: boolean;
  data: {
    value: number;
    classification: string;
    description: string;
    updated_at: string;
  };
}

export interface ForexResponse {
  success: boolean;
  data: {
    pair: string;
    rate: number;
    change: number;
    change_percent: number;
    updated_at: string;
  };
}

export interface GoldResponse {
  success: boolean;
  data: {
    name: string;
    price: number;
    change: number;
    change_percent: number;
    unit: string;
    updated_at: string;
  };
}

export interface NewsArticle {
  title: string;
  link: string;
  published: string;
  summary: string;
}

export interface NewsResponse {
  success: boolean;
  data: {
    [key: string]: {
      source: string;
      articles: NewsArticle[];
    };
  };
  updated_at: string;
}

export interface DashboardResponse {
  success: boolean;
  data: {
    korea_market: KoreaMarketResponse['data'];
    us_market: USMarketResponse['data'];
    fear_greed: FearGreedResponse['data'];
    forex: ForexResponse['data'];
    gold: GoldResponse['data'];
    news: NewsResponse['data'];
  };
}

// API 함수들
export const marketApi = {
  // 대시보드 전체 데이터
  getDashboard: async (): Promise<DashboardResponse> => {
    const { data } = await api.get('/api/dashboard');
    return data;
  },

  // 한국 시장
  getKoreaMarket: async (): Promise<KoreaMarketResponse> => {
    const { data } = await api.get('/api/market/korea');
    return data;
  },

  // 미국 시장
  getUSMarket: async (): Promise<USMarketResponse> => {
    const { data } = await api.get('/api/market/us');
    return data;
  },

  // Fear & Greed Index
  getFearGreed: async (): Promise<FearGreedResponse> => {
    const { data } = await api.get('/api/fear-greed');
    return data;
  },

  // 환율
  getForex: async (): Promise<ForexResponse> => {
    const { data } = await api.get('/api/forex');
    return data;
  },

  // 금 가격
  getGold: async (): Promise<GoldResponse> => {
    const { data } = await api.get('/api/gold');
    return data;
  },

  // 뉴스
  getNews: async (limit: number = 5): Promise<NewsResponse> => {
    const { data } = await api.get(`/api/news?limit=${limit}`);
    return data;
  },
};

export default api;
