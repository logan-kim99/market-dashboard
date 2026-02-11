import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { RefreshCw, TrendingUp } from 'lucide-react';
import { marketApi } from './services/api';
import MarketCard from './components/MarketCard';
import FearGreedGauge from './components/FearGreedGauge';
import NewsFeed from './components/NewsFeed';

function App() {
  const { data, isLoading, error, refetch, isFetching } = useQuery({
    queryKey: ['dashboard'],
    queryFn: marketApi.getDashboard,
    refetchInterval: 5 * 60 * 1000, // 5분마다 자동 새로고침
  });

  const handleRefresh = () => {
    refetch();
  };

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="bg-white rounded-xl shadow-lg p-8 max-w-md">
          <h2 className="text-2xl font-bold text-red-600 mb-4">오류 발생</h2>
          <p className="text-gray-700 mb-4">
            데이터를 불러올 수 없습니다. 백엔드 서버가 실행 중인지 확인해주세요.
          </p>
          <button
            onClick={handleRefresh}
            className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 transition-colors"
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* 헤더 */}
        <div className="mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <TrendingUp className="text-primary-600" size={32} />
                <div>
                  <h1 className="text-3xl font-bold text-gray-900">Market Dashboard</h1>
                  <p className="text-sm text-gray-600">실시간 금융 시장 현황</p>
                </div>
              </div>
              <button
                onClick={handleRefresh}
                disabled={isFetching}
                className="flex items-center gap-2 bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <RefreshCw size={20} className={isFetching ? 'animate-spin' : ''} />
                새로고침
              </button>
            </div>
          </div>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-white text-xl">데이터를 불러오는 중...</div>
          </div>
        ) : data?.data ? (
          <>
            {/* 한국 시장 */}
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-white mb-4">🇰🇷 한국 시장</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <MarketCard
                  name="KOSPI"
                  value={data.data.korea_market.kospi.value}
                  change={data.data.korea_market.kospi.change}
                  changePercent={data.data.korea_market.kospi.change_percent}
                  subtitle="한국종합주가지수"
                />
                <MarketCard
                  name="KOSDAQ"
                  value={data.data.korea_market.kosdaq.value}
                  change={data.data.korea_market.kosdaq.change}
                  changePercent={data.data.korea_market.kosdaq.change_percent}
                  subtitle="코스닥지수"
                />
              </div>
            </section>

            {/* 미국 시장 */}
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-white mb-4">🇺🇸 미국 시장</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MarketCard
                  name="S&P 500"
                  value={data.data.us_market.gspc.value}
                  change={data.data.us_market.gspc.change}
                  changePercent={data.data.us_market.gspc.change_percent}
                />
                <MarketCard
                  name="NASDAQ"
                  value={data.data.us_market.ixic.value}
                  change={data.data.us_market.ixic.change}
                  changePercent={data.data.us_market.ixic.change_percent}
                />
                <MarketCard
                  name="Dow Jones"
                  value={data.data.us_market.dji.value}
                  change={data.data.us_market.dji.change}
                  changePercent={data.data.us_market.dji.change_percent}
                />
                <MarketCard
                  name="VIX"
                  value={data.data.us_market.vix.value}
                  change={data.data.us_market.vix.change}
                  changePercent={data.data.us_market.vix.change_percent}
                  subtitle="변동성 지수"
                />
              </div>
            </section>

            {/* Fear & Greed + 환율/금 */}
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-white mb-4">📊 경제 지표</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <FearGreedGauge
                  value={data.data.fear_greed.value}
                  classification={data.data.fear_greed.classification}
                  description={data.data.fear_greed.description}
                />
                <MarketCard
                  name="USD/KRW"
                  value={data.data.forex.rate}
                  change={data.data.forex.change}
                  changePercent={data.data.forex.change_percent}
                  subtitle="원/달러 환율"
                />
                <MarketCard
                  name="Gold"
                  value={data.data.gold.price}
                  change={data.data.gold.change}
                  changePercent={data.data.gold.change_percent}
                  subtitle={data.data.gold.unit}
                />
              </div>
            </section>

            {/* 뉴스 */}
            <section>
              <h2 className="text-2xl font-bold text-white mb-4">📰 경제 뉴스</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {data.data.news.cnbc && (
                  <NewsFeed
                    source={data.data.news.cnbc.source}
                    articles={data.data.news.cnbc.articles}
                  />
                )}
                {data.data.news.bloomberg && (
                  <NewsFeed
                    source={data.data.news.bloomberg.source}
                    articles={data.data.news.bloomberg.articles}
                  />
                )}
                {data.data.news.wsj && (
                  <NewsFeed
                    source={data.data.news.wsj.source}
                    articles={data.data.news.wsj.articles}
                  />
                )}
              </div>
            </section>

            {/* 푸터 */}
            <footer className="mt-12 text-center text-white text-sm">
              <p>Last updated: {new Date().toLocaleString('ko-KR')}</p>
            </footer>
          </>
        ) : null}
      </div>
    </div>
  );
}

export default App;
