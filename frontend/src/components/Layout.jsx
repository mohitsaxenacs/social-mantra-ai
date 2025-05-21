import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { 
  FaCog, FaSearch, FaFileAlt, FaUpload, FaChartBar, FaBars, FaTimes, 
  FaQuestionCircle, FaRobot, FaRegLightbulb, FaRegChartBar, FaUsers, 
  FaTasks, FaRegNewspaper, FaSignOutAlt, FaHashtag
} from 'react-icons/fa';

// Tooltip component for consistent styling and behavior
const Tooltip = ({ content, position = 'right' }) => {
  return (
    <div className={`absolute z-10 ${position === 'right' ? 'left-full ml-2' : 'top-full mt-2'} px-3 py-2 bg-gray-800 text-white text-xs rounded shadow-lg w-64 opacity-0 group-hover:opacity-100 transition-opacity duration-200`}>
      {content}
      <div className={`absolute ${position === 'right' ? 'right-full' : 'bottom-full'} ${position === 'right' ? 'top-1/2 -translate-y-1/2' : 'left-1/2 -translate-x-1/2'} border-4 ${position === 'right' ? 'border-r-0 border-t-transparent border-b-transparent border-l-gray-800' : 'border-b-0 border-l-transparent border-r-transparent border-t-gray-800'}`}></div>
    </div>
  );
};

const Layout = () => {
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [showNewFeatureHint, setShowNewFeatureHint] = useState(true);

  // Navigation items with icons and tooltips - aligned with roadmap phases
  const navItems = [
    // Core features - Phase 1
    { 
      to: '/setup', 
      icon: <FaCog />, 
      label: 'Setup', 
      tooltip: 'Configure your API keys, social logins, and application preferences',
      isImplemented: true 
    },
    { 
      to: '/niche-research', 
      icon: <FaSearch />, 
      label: 'Niche Research', 
      tooltip: 'Research trending niches, low competition niches, AI-friendly niches, and analyze custom niches',
      isImplemented: true,
      badge: 'Real-time data' 
    },
    { 
      to: '/analytics', 
      icon: <FaChartBar />, 
      label: 'Analytics Dashboard', 
      tooltip: 'View real-time analytics for all your connected social media platforms',
      isImplemented: false,
      isNew: true 
    },
    { 
      to: '/social-media-marketing', 
      icon: <FaHashtag />, 
      label: 'Marketing Toolset', 
      tooltip: 'Optimize content with SEO tools, hashtag generators, and thumbnail recommendations using real data from APIs',
      isImplemented: true,
      isNew: true,
      badge: 'NEW' 
    },
    { 
      to: '/ai-assistant', 
      icon: <FaRobot />, 
      label: 'AI Assistant', 
      tooltip: 'Get intelligent insights and recommendations for improving your content strategy',
      isImplemented: false,
      isNew: true 
    },
    { 
      to: '/automation', 
      icon: <FaTasks />, 
      label: 'Automation Workflows', 
      tooltip: 'Create custom automation workflows for your content creation and posting',
      isImplemented: false 
    },
    // Content Creation - Phase 1
    { 
      to: '/generate-content', 
      icon: <FaFileAlt />, 
      label: 'Generate Content', 
      tooltip: 'Use AI to generate content based on your selected niche and platform',
      isImplemented: true 
    },
    { 
      to: '/scheduler', 
      icon: <FaRegChartBar />, 
      label: 'Post Scheduler', 
      tooltip: 'Schedule and manage your content across multiple platforms',
      isImplemented: false,
      isNew: true 
    },
    { 
      to: '/competitor-analysis', 
      icon: <FaUsers />, 
      label: 'Competitor Analysis', 
      tooltip: 'Analyze your competitors\'s posting time, content type, and engagement',
      isImplemented: false 
    },
    { 
      to: '/upload', 
      icon: <FaUpload />, 
      label: 'Upload Content', 
      tooltip: 'Upload and manage your content across platforms',
      isImplemented: true 
    },
    { 
      to: '/news-feed', 
      icon: <FaRegNewspaper />, 
      label: 'AI News & Updates', 
      tooltip: 'Stay updated with the latest AI model news and feature updates',
      isImplemented: false,
      isNew: true 
    },
  ];

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };
  
  // Handle logout functionality
  const handleLogout = () => {
    // Clear authentication data from localStorage
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('authProvider');
    localStorage.removeItem('userEmail');
    
    // Redirect to login page
    navigate('/login');
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Mobile Sidebar Toggle */}
      <button
        onClick={toggleSidebar}
        className="lg:hidden fixed z-20 top-4 left-4 p-2 rounded-md bg-white shadow-md text-gray-700 hover:text-primary-600 focus:outline-none"
      >
        {isSidebarOpen ? <FaTimes /> : <FaBars />}
      </button>

      {/* Sidebar Navigation - now with improved aesthetics and tooltips */}
      <div 
        className={`${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} 
                   fixed lg:static lg:translate-x-0 z-10 h-full w-64 bg-white shadow-lg transition-transform duration-300 ease-in-out
                   flex flex-col`}
      >
        <div className="p-6 bg-gradient-to-r from-primary-600 to-secondary-600">
          <h1 className="text-xl font-bold text-white">Social Mantra AI</h1>
          <p className="text-primary-100 text-sm mt-1 opacity-80">AI-Powered Content Creation</p>
        </div>

        <div className="px-4 py-3 bg-blue-50 border-b border-blue-100 flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-2">
              <FaRegLightbulb className="text-blue-600 text-sm" />
            </div>
            <span className="text-sm font-medium text-blue-800">User Mode:</span>
          </div>
          <div className="relative inline-block w-12 align-middle select-none">
            <input type="checkbox" name="toggle" id="user-mode-toggle" defaultChecked className="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-2 border-gray-300 appearance-none cursor-pointer transition-transform duration-200 ease-in left-0 top-0 transform translate-x-0" />
            <label htmlFor="user-mode-toggle" className="toggle-label block overflow-hidden h-5 rounded-full bg-gray-300 cursor-pointer"></label>
          </div>
          <span className="text-xs font-medium text-blue-800">Advanced</span>
          
          <style jsx>{`
            .toggle-checkbox:checked {
              transform: translateX(100%);
              border-color: primary-500;
            }
            .toggle-checkbox:checked + .toggle-label {
              background-color: primary-400;
            }
          `}</style>
        </div>

        <nav className="flex-1 overflow-y-auto py-6 px-4">
          <div className="mb-4 px-4">
            <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Core Features</div>
          </div>
          
          <ul className="space-y-1.5">
            {navItems.slice(0, 5).map((item) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    `group relative flex items-center px-4 py-2.5 text-sm rounded-lg transition-all duration-200 ${!item.isImplemented ? 'opacity-60 cursor-not-allowed' : ''} ${isActive 
                      ? 'bg-gradient-to-r from-primary-50 to-primary-100 text-primary-700 font-medium shadow-sm' 
                      : 'text-gray-700 hover:bg-gray-100'}`
                  }
                  onClick={(e) => !item.isImplemented && e.preventDefault()}
                >
                  <span className="mr-3 text-lg">{item.icon}</span>
                  <span>{item.label}</span>
                  {item.isNew && showNewFeatureHint && (
                    <span className="ml-2 px-1.5 py-0.5 text-xs font-medium bg-green-100 text-green-800 rounded-full">New</span>
                  )}
                  {item.badge && (
                    <span className="ml-2 px-1.5 py-0.5 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">{item.badge}</span>
                  )}
                  
                  {/* Tooltip */}
                  <div className="group-hover:block hidden">
                    <Tooltip content={item.tooltip} />
                  </div>
                  
                  {/* Implementation status for non-implemented features */}
                  {!item.isImplemented && (
                    <span className="absolute right-3 top-1/2 transform -translate-y-1/2 w-2 h-2 rounded-full bg-gray-300"></span>
                  )}
                </NavLink>
              </li>
            ))}
          </ul>
          
          <div className="my-4 px-4 pt-4 border-t border-gray-100">
            <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Content Management</div>
          </div>
          
          <ul className="space-y-1.5">
            {navItems.slice(5).map((item) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    `group relative flex items-center px-4 py-2.5 text-sm rounded-lg transition-all duration-200 ${!item.isImplemented ? 'opacity-60 cursor-not-allowed' : ''} ${isActive 
                      ? 'bg-gradient-to-r from-primary-50 to-primary-100 text-primary-700 font-medium shadow-sm' 
                      : 'text-gray-700 hover:bg-gray-100'}`
                  }
                  onClick={(e) => !item.isImplemented && e.preventDefault()}
                >
                  <span className="mr-3 text-lg">{item.icon}</span>
                  <span>{item.label}</span>
                  {item.isNew && showNewFeatureHint && (
                    <span className="ml-2 px-1.5 py-0.5 text-xs font-medium bg-green-100 text-green-800 rounded-full">New</span>
                  )}
                  
                  {/* Tooltip */}
                  <div className="group-hover:block hidden">
                    <Tooltip content={item.tooltip} />
                  </div>
                  
                  {/* Implementation status for non-implemented features */}
                  {!item.isImplemented && (
                    <span className="absolute right-3 top-1/2 transform -translate-y-1/2 w-2 h-2 rounded-full bg-gray-300"></span>
                  )}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-200">
          {/* Logout Button */}
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center px-4 py-2 mb-4 text-sm font-medium text-red-600 bg-red-50 rounded-md hover:bg-red-100 transition-colors duration-200"
          >
            <FaSignOutAlt className="mr-2" />
            Logout
          </button>
          
          <div className="bg-primary-50 rounded-lg p-4">
            <h3 className="text-sm font-medium text-primary-800 mb-2 flex items-center">
              <FaQuestionCircle className="mr-2 text-primary-600" />
              Need Help?
            </h3>
            <p className="text-xs text-gray-600 mb-3">
              Check our documentation for detailed guides on how to use each feature effectively.
            </p>
            <a 
              href="/docs" 
              className="block text-center text-xs font-medium text-primary-600 bg-white py-2 px-3 rounded border border-primary-200 hover:bg-primary-50 transition-colors"
            >
              View Documentation
            </a>
          </div>
          
          <div className="mt-4 text-xs text-center text-gray-500">
            <p>Using real-time YouTube data</p>
            <p className="mt-1">&copy; 2025 Social Mantra AI</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto relative">
        {/* Overlay for mobile when sidebar is open */}
        {isSidebarOpen && (
          <div 
            className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-0"
            onClick={() => setIsSidebarOpen(false)}
          ></div>
        )}
        
        <div className="p-6 max-w-7xl mx-auto">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;
