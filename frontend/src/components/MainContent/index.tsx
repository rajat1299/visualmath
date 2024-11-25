import React, { useState } from 'react';
import { ErrorMessage } from '../common/ErrorMessage';
import { AnimationPlayer } from '../AnimationPlayer/AnimationPlayer';
import { LoadingOverlay } from '../LoadingOverlay';
import { Tooltip } from '../common/Tooltip';

interface MainContentProps {
  onGenerateAnimation: (description: string, quality: string) => Promise<string>;
}

interface ExampleConcept {
  label: string;
  prompt: string;
}

interface QualityOption {
  label: string;
  value: string;
  description: string;
}

export const MainContent: React.FC<MainContentProps> = ({ onGenerateAnimation }) => {
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [animationUrl, setAnimationUrl] = useState<string | null>(null);
  const [selectedQuality, setSelectedQuality] = useState<string>("medium");

  const exampleConcepts: ExampleConcept[] = [
    {
      label: 'Bezier Curve',
      prompt: 'Create an animation of a cubic Bezier curve, showing its control points and how they influence the curve shape. Animate the curve being drawn and highlight the control points.'
    },
    {
      label: 'Mobius Strip',
      prompt: 'Create a 3D animation of a Mobius strip forming from a rectangular strip. Show the twisting process and color one side red and the other blue to demonstrate the single-sided nature.'
    },
    {
      label: 'Binary Tree',
      prompt: 'Animate the construction of a binary tree with 7 nodes. Show each node being added one by one, with edges growing to connect them. Color the root node differently and add labels to show the tree structure.'
    },
    {
      label: 'Fourier Transform',
      prompt: 'Demonstrate the Fourier transform by showing how a complex waveform can be built from simple sine waves. Start with a simple wave, then add harmonics one by one, showing the resulting approximation.'
    },
    {
      label: 'Double Pendulum',
      prompt: 'Create an animation of the double pendulum system, showing its chaotic behavior. Include phase space trajectories and demonstrate sensitivity to initial conditions by showing two nearly identical starting positions diverging over time.'
    }
  ];

  const qualityOptions: QualityOption[] = [
    {
      label: "Low",
      value: "low",
      description: "480p, faster loading"
    },
    {
      label: "Medium",
      value: "medium",
      description: "720p, balanced"
    },
    {
      label: "High",
      value: "high",
      description: "1080p, best quality"
    }
  ];

  const handleSubmit = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const url = await onGenerateAnimation(description, selectedQuality);
      setAnimationUrl(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate animation');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setDescription('');
    setError(null);
    setAnimationUrl(null);
  };

  return (
    <div className="max-w-4xl mx-auto text-center">
      <h1 className="text-6xl font-bold text-purple-500 mb-4">
        Text to Math Animations
      </h1>
      <p className="text-xl text-gray-400 mb-12">
        powered by manim engine
      </p>
      
      {/* Example Tags with Tooltips */}
      <div className="flex flex-wrap gap-3 justify-center mb-8">
        {exampleConcepts.map((concept) => (
          <Tooltip 
            key={concept.label}
            content={concept.prompt}
            position="bottom"
          >
            <button
              onClick={() => setDescription(concept.prompt)}
              className="px-4 py-2.5 bg-gray-900/50 rounded-xl border border-gray-800 text-white text-sm hover:bg-gray-800/50 transition-colors"
            >
              {concept.label}
            </button>
          </Tooltip>
        ))}
      </div>

      {/* Error Display */}
      {error && (
        <ErrorMessage 
          message={error} 
          onRetry={() => {
            setError(null);
            handleSubmit();
          }}
        />
      )}

      {/* Input Area */}
      <div className="p-8 bg-gray-900/50 rounded-2xl border border-gray-800 backdrop-blur-xl">
        <div className="relative">
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe the mathematical concept you want to visualize..."
            className="w-full h-30 p-4 bg-gray-800/50 rounded-xl border border-gray-700 text-white placeholder-zinc-500 resize-none focus:outline-none focus:ring-2 focus:ring-violet-600"
            rows={4}
            disabled={isLoading}
          />
          {description && (
            <button
              onClick={handleClear}
              className="absolute top-2 right-2 p-2 text-gray-400 hover:text-white rounded-lg hover:bg-gray-700/50 transition-colors"
              title="Clear input"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
        
        <div className="flex gap-4 mt-4 mb-6">
          {qualityOptions.map((option) => (
            <button
              key={option.value}
              onClick={() => setSelectedQuality(option.value)}
              className={`flex-1 p-3 rounded-xl border transition-colors ${
                selectedQuality === option.value
                  ? 'border-violet-500 bg-violet-500/20 text-white'
                  : 'border-gray-700 bg-gray-800/50 text-gray-400 hover:bg-gray-700/50'
              }`}
            >
              <div className="text-sm font-medium">{option.label}</div>
              <div className="text-xs opacity-60">{option.description}</div>
            </button>
          ))}
        </div>

        <div className="flex gap-4 mt-6">
          <button
            onClick={handleSubmit}
            disabled={isLoading || !description.trim()}
            className="flex-1 py-3 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-xl text-white font-normal text-lg disabled:opacity-50 transition-opacity relative"
          >
            {isLoading ? (
              <>
                <span className="opacity-0">Generate Animation</span>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                </div>
              </>
            ) : (
              'Generate Animation'
            )}
          </button>
          
          <button
            onClick={handleClear}
            disabled={isLoading || !description.trim()}
            className="px-6 py-3 bg-gray-800/50 hover:bg-gray-700/50 rounded-xl text-gray-300 font-normal text-lg disabled:opacity-50 transition-colors"
            title="Clear all"
          >
            Clear
          </button>
        </div>
      </div>

      {/* Animation Display */}
      {animationUrl && (
        <AnimationPlayer 
          url={animationUrl} 
          onClose={() => setAnimationUrl(null)}
        />
      )}

      {/* Loading Overlay */}
      {isLoading && <LoadingOverlay />}
    </div>
  );
};

export default MainContent; 