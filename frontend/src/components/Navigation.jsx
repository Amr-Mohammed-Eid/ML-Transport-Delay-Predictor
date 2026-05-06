import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FiMenu, FiX, FiBarChart2, FiZap, FiTrendingUp, FiActivity } from 'react-icons/fi';
import './Navigation.css';

function Navigation() {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const navItems = [
    { path: '/', label: 'Dashboard', icon: FiBarChart2, exact: true },
    { path: '/predict', label: 'Predict Delay', icon: FiZap },
    { path: '/analysis', label: 'Data Analysis', icon: FiTrendingUp },
    { path: '/performance', label: 'Model Performance', icon: FiActivity },
  ];

  const isActive = (path, exact = false) => {
    if (exact) {
      return location.pathname === path;
    }
    return location.pathname.startsWith(path);
  };

  return (
    <motion.nav
      className="modern-navbar"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      <div className="nav-container">
        <motion.div
          className="nav-brand"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Link to="/" className="brand-link">
            <span className="brand-icon">🚌</span>
            <span className="brand-text">
              <span className="brand-title">Transport Delay</span>
              <span className="brand-subtitle">Predictor</span>
            </span>
          </Link>
        </motion.div>

        {/* Desktop Navigation */}
        <div className="nav-menu-desktop">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path, item.exact);
            return (
              <motion.div
                key={item.path}
                whileHover={{ y: -2 }}
                whileTap={{ scale: 0.95 }}
              >
                <Link
                  to={item.path}
                  className={`nav-item ${active ? 'active' : ''}`}
                >
                  <Icon className="nav-icon" />
                  <span>{item.label}</span>
                  {active && (
                    <motion.div
                      className="nav-indicator"
                      layoutId="activeIndicator"
                      initial={false}
                      transition={{
                        type: "spring",
                        stiffness: 380,
                        damping: 30,
                      }}
                    />
                  )}
                </Link>
              </motion.div>
            );
          })}
        </div>

        {/* Mobile Menu Button */}
        <motion.button
          className="mobile-menu-button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          whileTap={{ scale: 0.9 }}
          aria-label="Toggle menu"
        >
          <AnimatePresence mode="wait">
            {mobileMenuOpen ? (
              <motion.div
                key="close"
                initial={{ rotate: -90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: 90, opacity: 0 }}
                transition={{ duration: 0.2 }}
              >
                <FiX />
              </motion.div>
            ) : (
              <motion.div
                key="menu"
                initial={{ rotate: 90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: -90, opacity: 0 }}
                transition={{ duration: 0.2 }}
              >
                <FiMenu />
              </motion.div>
            )}
          </AnimatePresence>
        </motion.button>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            className="mobile-menu"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
          >
            <div className="mobile-menu-content">
              {navItems.map((item, index) => {
                const Icon = item.icon;
                const active = isActive(item.path, item.exact);
                return (
                  <motion.div
                    key={item.path}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Link
                      to={item.path}
                      className={`mobile-nav-item ${active ? 'active' : ''}`}
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      <Icon className="nav-icon" />
                      <span>{item.label}</span>
                      {active && <div className="mobile-nav-indicator" />}
                    </Link>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
}

export default Navigation;

