import React, { useEffect, useRef } from 'react';
import { motion, useMotionValue, useSpring } from 'framer-motion';

function AnimatedMetric({ value, label, delay = 0, suffix = '', prefix = '' }) {
  const motionValue = useMotionValue(0);
  const springValue = useSpring(motionValue, {
    damping: 30,
    stiffness: 100,
  });
  const displayValue = useMotionValue(0);

  useEffect(() => {
    motionValue.set(value);
  }, [value, motionValue]);

  useEffect(() => {
    const unsubscribe = springValue.on('change', (latest) => {
      displayValue.set(Math.round(latest));
    });
    return () => unsubscribe();
  }, [springValue, displayValue]);

  return (
    <motion.div
      className="animated-metric"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.5,
        delay,
        ease: [0.6, -0.05, 0.01, 0.99],
      }}
      // whileHover={{ scale: 1.05 }}
    >
      <motion.div className="metric-label">{label}</motion.div>
      <motion.div className="metric-value">
        {prefix}
        <motion.span>{displayValue}</motion.span>
        {suffix}
      </motion.div>
    </motion.div>
  );
}

export default AnimatedMetric;

