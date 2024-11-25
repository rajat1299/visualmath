import React, { useState } from 'react';
import { Header } from './components/Header';
import MainContent from './components/MainContent';
import { ErrorMessage } from './components/common/ErrorMessage';

export const App: React.FC = () => {
  const [globalError, setGlobalError] = useState<string | null>(null);

  const handleAnimationCreate = async (description: string): Promise<string> => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/animations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create animation');
      }
      
      const data = await response.json();
      return `http://localhost:8000${data.animation_url}`;
    } catch (error) {
      setGlobalError(error instanceof Error ? error.message : 'An unexpected error occurred');
      throw error;
    }
  };

  return (
    <div className="min-h-screen bg-black bg-gradient-to-br from-violet-900 via-black to-indigo-900">
      <div className="container mx-auto px-4">
        <Header />
        {globalError && (
          <ErrorMessage 
            message={globalError}
            onRetry={() => setGlobalError(null)}
          />
        )}
        <MainContent onGenerateAnimation={handleAnimationCreate} />
      </div>
    </div>
  );
};

export default App; 