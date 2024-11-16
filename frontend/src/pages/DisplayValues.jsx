import React from 'react';
// hi
const DisplayValues = ({ promotionType, creativity, age, starName, selectedContent, isEmoji, isSlang, addRequirements }) => {
  return (
    <div className="p-4 border border-gray-300 rounded-md shadow-md">
      <h2 className="text-xl font-bold mb-2">Current Values</h2>
      <p><strong>Promotion Type:</strong> {promotionType}</p>
      <p><strong>Creativity Level:</strong> {creativity}</p>
      <p><strong>Age Range:</strong> {age.join(' - ')}</p>
      <p><strong>Star Name:</strong> {starName}</p>
      <p><strong>Selected Content:</strong> {selectedContent}</p>
      <p><strong>Include Emojis:</strong> {isEmoji ? 'Yes' : 'No'}</p>
      <p><strong>Include Slang:</strong> {isSlang ? 'Yes' : 'No'}</p>
      <p><strong>Additional Requirements:</strong> {addRequirements}</p>
    </div>
  );
};

export default DisplayValues;