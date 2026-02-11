import React from 'react';

interface FearGreedGaugeProps {
  value: number;
  classification: string;
  description: string;
}

const FearGreedGauge: React.FC<FearGreedGaugeProps> = ({
  value,
  classification,
  description,
}) => {
  const getColor = (val: number) => {
    if (val <= 25) return '#ef4444'; // 극도의 공포 - 빨강
    if (val <= 45) return '#f97316'; // 공포 - 주황
    if (val <= 55) return '#eab308'; // 중립 - 노랑
    if (val <= 75) return '#84cc16'; // 탐욕 - 연두
    return '#22c55e'; // 극도의 탐욕 - 초록
  };

  const rotation = (value / 100) * 180 - 90; // -90도에서 +90도

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Fear & Greed Index</h3>
      
      <div className="relative w-full max-w-xs mx-auto">
        {/* 반원 게이지 배경 */}
        <svg viewBox="0 0 200 100" className="w-full">
          {/* 배경 아크 */}
          <path
            d="M 10 90 A 90 90 0 0 1 190 90"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="20"
            strokeLinecap="round"
          />
          
          {/* 값 표시 아크 */}
          <path
            d="M 10 90 A 90 90 0 0 1 190 90"
            fill="none"
            stroke={getColor(value)}
            strokeWidth="20"
            strokeLinecap="round"
            strokeDasharray={`${(value / 100) * 283} 283`}
          />
          
          {/* 중심점 */}
          <circle cx="100" cy="90" r="5" fill="#374151" />
          
          {/* 바늘 */}
          <line
            x1="100"
            y1="90"
            x2="100"
            y2="30"
            stroke="#374151"
            strokeWidth="3"
            strokeLinecap="round"
            transform={`rotate(${rotation} 100 90)`}
          />
        </svg>
        
        {/* 값 표시 */}
        <div className="text-center mt-4">
          <p className="text-4xl font-bold" style={{ color: getColor(value) }}>
            {value}
          </p>
          <p className="text-sm font-semibold text-gray-700 mt-1">
            {classification}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            {description}
          </p>
        </div>
      </div>
    </div>
  );
};

export default FearGreedGauge;
