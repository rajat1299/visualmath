import React, { useState } from 'react';

interface AnimationPlayerProps {
    url: string;
    onClose?: () => void;
}

export const AnimationPlayer: React.FC<AnimationPlayerProps> = ({ url, onClose }) => {
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const handleLoadComplete = () => {
        setIsLoading(false);
    };

    const handleError = () => {
        setError('Failed to load animation');
        setIsLoading(false);
    };

    return (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="relative max-w-4xl w-full bg-gray-900/90 rounded-2xl p-6">
                {/* Close button */}
                {onClose && (
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 text-gray-400 hover:text-white"
                    >
                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                )}

                {/* Loading indicator */}
                {isLoading && (
                    <div className="absolute inset-0 flex items-center justify-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-violet-600"></div>
                    </div>
                )}

                {/* Error message */}
                {error && (
                    <div className="text-red-500 text-center py-8">
                        {error}
                        <button
                            onClick={() => window.location.reload()}
                            className="block mx-auto mt-4 text-white bg-red-600 px-4 py-2 rounded-lg"
                        >
                            Retry
                        </button>
                    </div>
                )}

                {/* Video player */}
                <video
                    className={`w-full rounded-xl ${isLoading ? 'opacity-0' : 'opacity-100'}`}
                    controls
                    autoPlay
                    loop
                    onLoadedData={handleLoadComplete}
                    onError={handleError}
                    src={url}
                >
                    Your browser does not support the video tag.
                </video>
            </div>
        </div>
    );
}; 