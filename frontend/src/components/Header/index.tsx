import React from 'react';

interface HeaderProps {
  username?: string;
}

export const Header: React.FC<HeaderProps> = ({ username = 'rajat' }) => {
  return (
    <div className="w-full flex justify-between items-center px-16 py-12">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-xl flex items-center justify-center relative overflow-hidden group">
          <div className="absolute inset-0 flex items-center justify-center">
            <svg 
              className="w-6 h-6 text-white transform group-hover:scale-110 transition-transform" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              strokeWidth="2"
            >
              <path d="M4 4h16v2l-8 6 8 6v2H4v-3h10l-6-5 6-5H4z" />
            </svg>
            <div className="absolute inset-0 bg-white/20 transform scale-0 group-hover:scale-100 transition-transform rounded-xl" />
          </div>
        </div>
        <span className="text-2xl font-bold text-white hover:text-violet-300 transition-colors">
          visualmath-ai
        </span>
      </div>
      
      <div className="px-4 py-2.5 rounded-md">
        <span className="text-sm font-bold text-white opacity-50 hover:opacity-100 transition-opacity">
          {username}
        </span>
      </div>
    </div>
  );
}; 