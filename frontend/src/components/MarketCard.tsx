import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface MarketCardProps {
  name: string;
  value: number;
  change: number;
  changePercent: number;
  subtitle?: string;
}

const MarketCard: React.FC<MarketCardProps> = ({
  name,
  value,
  change,
  changePercent,
  subtitle,
}) => {
  const isPositive = change >= 0;

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">{name}</h3>
          {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
        </div>
        {isPositive ? (
          <TrendingUp className="text-green-500" size={24} />
        ) : (
          <TrendingDown className="text-red-500" size={24} />
        )}
      </div>
      
      <div className="mb-2">
        <p className="text-3xl font-bold text-gray-900">
          {value.toLocaleString('ko-KR', { maximumFractionDigits: 2 })}
        </p>
      </div>
      
      <div className={`flex items-center gap-2 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
        <span className="font-semibold">
          {isPositive ? '+' : ''}{change.toLocaleString('ko-KR', { maximumFractionDigits: 2 })}
        </span>
        <span className="font-semibold">
          ({isPositive ? '+' : ''}{changePercent.toFixed(2)}%)
        </span>
      </div>
    </div>
  );
};

export default MarketCard;
