import React from 'react';
// hi
const Slider = ({ value, onChange }) => {
  return ( 
    <div className="flex-grow mb-4"> 
    <div className="flex">
      <label className="block text-lg font-bold text-gray-700">Creativity</label> 
      <label className="text-red-400 font-bold text-lg ml-1">*</label> 
    </div> 
    <input type="range" min="0" max="100" value={value} onChange={(e) => onChange(e.target.value)} className="mt-4 w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer" style={{ accentColor: '#3B82F6', }} /> 
      <style jsx>{` input[type='range'] { -webkit-appearance: none; width: 100%; }
      input[type='range']::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 24px; /* Increase the size of the thumb */
        height: 24px; /* Increase the size of the thumb */
        border-radius: 50%;
        background: #3B82F6; /* Tailwind blue-500 color */
        cursor: pointer;
        margin-top: -1px; /* Center the thumb vertically */
      }

      input[type='range']::-webkit-slider-runnable-track {
        height: 22px; /* Height of the track */
        background: #e5e7eb; /* Color of the unfilled portion */
        border-radius: 5px;
      }
    `}</style>
  </div>
); };

export default Slider;