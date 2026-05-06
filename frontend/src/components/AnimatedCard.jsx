import React from 'react';
import { motion } from 'framer-motion';
import { cardHover } from '../utils/animations';

function AnimatedCard({ children, className = '', delay = 0, ...props }) {
  return (
    <motion.div
      className={`card animated-card ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.5,
        delay,
        ease: [0.6, -0.05, 0.01, 0.99],
      }}
      // whileHover={cardHover}
      {...props}
    >
      {children}
    </motion.div>
  );
}

export default AnimatedCard;

