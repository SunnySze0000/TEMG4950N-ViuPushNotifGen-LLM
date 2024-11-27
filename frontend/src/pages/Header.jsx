import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom'; // Import useLocation
// hii
const Header = ({ activeButton, handleButtonClick }) => {
  const navigate = useNavigate(); // Initialize the navigate function
  const location = useLocation(); // Get the current location

  useEffect(() => {
    // Set active button based on the current path
    if (location.pathname === '/generation_history') {
      handleButtonClick('history');
    } else {
      handleButtonClick('generator');
    }
  }, [location.pathname, handleButtonClick]); // Run effect when the pathname changes

  return (
    <div className="bg-white h-auto flex flex-col justify-between p-4 shadow-md">
      <div className="flex flex-col justify-between ml-3">
        <h1 className="text-lg md:text-xl font-bold mt-3">Copywriter AI</h1>
        <p className="text-gray-500 mt-2 text-sm md:text-base">
          With our Copywriter AI, you can generate multilingual text off a prompt, a show or an actor.
        </p>
      </div>
      <div className="flex pl-3 flex wrap">
        <button
          className={`text-pink-500 py-2 px-4 font-bold ${activeButton === 'generator' ? 'border-b-4 border-pink-500' : ''}`}
          onClick={() => {
            handleButtonClick('generator');
            navigate('/'); // Navigate to the homepage
          }}
        >
          AI Generator
        </button>
        <button
          className={`text-pink-500 py-2 px-4 font-bold ${activeButton === 'history' ? 'border-b-4 border-pink-500' : ''}`}
          onClick={() => {
            handleButtonClick('history');
            navigate('/generation_history'); // Navigate to the test page
          }}
        >
          Generation History
        </button>
      </div>
    </div>
  );
};

export default Header;