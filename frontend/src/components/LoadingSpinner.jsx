import React from 'react';
import { motion } from 'framer-motion';

function LoadingSpinner({ size = 40, color = '#1a1a1a' }) {
  return (
    <div className="loading-spinner-container">
      <motion.div
        className="loading-spinner"
        style={{ width: size, height: size, borderTopColor: color }}
        animate={{ rotate: 360 }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: 'linear',
        }}
      />
    </div>
  );
}

function SkeletonLoader({ width = '100%', height = '1rem', className = '' }) {
  return (
    <motion.div
      className={`skeleton-loader ${className}`}
      style={{ width, height }}
      animate={{
        opacity: [0.5, 1, 0.5],
      }}
      transition={{
        duration: 1.5,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
    />
  );
}

export { LoadingSpinner, SkeletonLoader };

