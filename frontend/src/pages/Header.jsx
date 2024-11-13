import React from 'react';

const Header = ({ activeButton, handleButtonClick }) => {
  return (
    <div className="bg-white h-1/6 flex flex-col justify-between p-4 shadow-md">
      <div className="flex flex-col justify-between ml-3">
        <h1 className="text-xl font-bold mt-3">Copywriter AI</h1>
        <p className="text-gray-500 mt-3">
          With our Copywriter AI, you can generate multilingual text off a prompt, a show or an actor.
        </p>
      </div>
      <div className="flex pl-3">
        <button
          className={`text-pink-500 py-2 px-4 font-bold ${activeButton === 'generator' ? 'border-b-4 border-pink-500' : ''}`}
          onClick={() => handleButtonClick('generator')}
        >
          AI Generator
        </button>
        <button
          className={`text-pink-500 py-2 px-4 font-bold ${activeButton === 'audit' ? 'border-b-4 border-pink-500' : ''}`}
          onClick={() => handleButtonClick('audit')}
        >
          Audit
        </button>
      </div>
    </div>
  );
};

export default Header;