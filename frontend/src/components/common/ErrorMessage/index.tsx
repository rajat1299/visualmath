import React from 'react';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => {
  return (
    <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-4 my-4">
      <div className="flex items-center gap-3">
        <svg className="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span className="text-red-500">{message}</span>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-3 text-sm text-red-500 hover:text-red-400 underline"
        >
          Try again
        </button>
      )}
    </div>
  );
}; 