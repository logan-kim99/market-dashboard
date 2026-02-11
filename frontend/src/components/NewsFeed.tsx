import React from 'react';
import { ExternalLink, Newspaper } from 'lucide-react';
import { NewsArticle } from '../services/api';

interface NewsFeedProps {
  source: string;
  articles: NewsArticle[];
}

const NewsFeed: React.FC<NewsFeedProps> = ({ source, articles }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center gap-2 mb-4">
        <Newspaper className="text-primary-600" size={24} />
        <h3 className="text-lg font-semibold text-gray-800">{source}</h3>
      </div>
      
      <div className="space-y-3">
        {articles.length === 0 ? (
          <p className="text-gray-500 text-sm">뉴스를 불러올 수 없습니다.</p>
        ) : (
          articles.map((article, index) => (
            <a
              key={index}
              href={article.link}
              target="_blank"
              rel="noopener noreferrer"
              className="block p-3 rounded-lg hover:bg-gray-50 transition-colors border border-gray-100"
            >
              <div className="flex justify-between items-start gap-2">
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 text-sm line-clamp-2 mb-1">
                    {article.title}
                  </h4>
                  {article.summary && (
                    <p className="text-xs text-gray-600 line-clamp-2">
                      {article.summary}
                    </p>
                  )}
                  {article.published && (
                    <p className="text-xs text-gray-400 mt-1">
                      {new Date(article.published).toLocaleDateString('ko-KR')}
                    </p>
                  )}
                </div>
                <ExternalLink size={16} className="text-gray-400 flex-shrink-0 mt-1" />
              </div>
            </a>
          ))
        )}
      </div>
    </div>
  );
};

export default NewsFeed;
