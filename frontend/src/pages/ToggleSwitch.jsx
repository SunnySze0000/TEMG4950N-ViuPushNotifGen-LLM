// ToggleSwitch.js
import React from 'react';
// hi
const ToggleSwitch = ({ label, checked, onChange }) => {
  return (
    <div className="flex justify-between items-center mb-4">
      <label htmlFor={label} className="text-lg">{label}</label>
      <div className="relative">
        <input
          type="checkbox"
          id={label}
          checked={checked}
          onChange={onChange}
          className="hidden"
        />
        <div 
          className={`w-12 h-6 flex items-center rounded-full p-1 cursor-pointer transition-colors duration-300 ${checked ? 'bg-blue-500' : 'bg-gray-300'}`} 
          onClick={onChange}
        >
          <div className={`w-4 h-4 bg-white rounded-full shadow-md transform transition-transform duration-300 ${checked ? 'translate-x-6' : 'translate-x-0'}`} />
        </div>
      </div>
    </div>
  );
};

export default ToggleSwitch;