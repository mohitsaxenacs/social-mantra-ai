import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { FaCog, FaSearch, FaFileAlt, FaUpload, FaChartBar } from 'react-icons/fa';

const Layout = () => {
  // Navigation items with icons
  const navItems = [
    { to: '/setup', icon: <FaCog />, label: 'Setup' },
    { to: '/niche-research', icon: <FaSearch />, label: 'Niche Research' },
    { to: '/generate-content', icon: <FaFileAlt />, label: 'Generate Content' },
    { to: '/upload', icon: <FaUpload />, label: 'Upload' },
    { to: '/analytics', icon: <FaChartBar />, label: 'Analytics' },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar Navigation */}
      <div className="w-64 bg-white shadow-md">
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-xl font-semibold text-gray-800">Shorts Automation</h1>
        </div>
        <nav className="mt-4">
          <ul>
            {navItems.map((item) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center px-4 py-3 text-gray-700 ${isActive ? 'bg-primary-50 text-primary-600 border-r-4 border-primary-500' : 'hover:bg-gray-100'}`
                  }
                >
                  <span className="mr-3">{item.icon}</span>
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="p-6">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;
