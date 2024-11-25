import React from 'react';

interface AnimationHistoryItem {
  id: number;
  description: string;
  url: string;
  createdAt: string;
  quality: string;
}

interface AnimationHistoryProps {
  items: AnimationHistoryItem[];
  onSelect: (url: string) => void;
}

export const AnimationHistory: React.FC<AnimationHistoryProps> = ({ items, onSelect }) => {
  return (
    <div className="mt-8">
      <h2 className="text-xl font-bold text-white mb-4">Recent Animations</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((item) => (
          <div
            key={item.id}
            className="bg-gray-900/50 rounded-xl p-4 cursor-pointer hover:bg-gray-800/50 transition-colors"
            onClick={() => onSelect(item.url)}
          >
            <div className="aspect-video bg-black/50 rounded-lg mb-3 overflow-hidden">
              <video
                src={item.url}
                className="w-full h-full object-cover"
                muted
                onMouseOver={(e) => e.currentTarget.play()}
                onMouseOut={(e) => {
                  e.currentTarget.pause();
                  e.currentTarget.currentTime = 0;
                }}
              />
            </div>
            <p className="text-sm text-gray-300 line-clamp-2">{item.description}</p>
            <div className="flex justify-between items-center mt-2">
              <span className="text-xs text-gray-500">
                {new Date(item.createdAt).toLocaleDateString()}
              </span>
              <span className="text-xs text-violet-400 uppercase">{item.quality}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}; 