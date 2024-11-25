import React from 'react';

interface LoadingOverlayProps {
  message?: string;
}

export const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ 
  message = "Generating your animation..." 
}) => {
  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-gray-900/90 rounded-2xl p-8 max-w-md w-full mx-4">
        <div className="flex flex-col items-center">
          {/* Animated logo */}
          <div className="w-16 h-16 mb-6">
            <div className="w-full h-full rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 animate-pulse" />
          </div>
          
          {/* Loading spinner */}
          <div className="w-12 h-12 border-4 border-violet-600/30 border-t-violet-600 rounded-full animate-spin mb-4" />
          
          {/* Message */}
          <p className="text-white text-lg font-medium mb-2">{message}</p>
          <p className="text-gray-400 text-sm text-center">
            This might take a few moments...
          </p>
        </div>
      </div>
    </div>
  );
}; 