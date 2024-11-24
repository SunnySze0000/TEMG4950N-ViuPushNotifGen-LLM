import React, {useContext} from 'react';
import { SettingsContext } from './SettingsContext';
// hi
const DisplayValues = () => {
  const { settings, setSettings } = useContext(SettingsContext);
  return (
    <div className="p-4 border border-gray-300 rounded-md shadow-md">
      <h2 className="text-xl font-bold mb-2">Current Values</h2>
      <p><strong>Promotion Type:</strong> {settings.promotionType}</p>
      <p><strong>Creativity Level:</strong> {settings.creativity/100}</p>
      <p><strong>Age Range:</strong> {settings.age.join(' - ')}</p>
      <p><strong>Star Name:</strong> {settings.starName}</p>
      <p><strong>Selected Content:</strong> {settings.selectedContent}</p>
      <p><strong>Include Emojis:</strong> {settings.isEmoji ? 'Yes' : 'No'}</p>
      <p><strong>Include Slang:</strong> {settings.isSlang ? 'Yes' : 'No'}</p>
      <p><strong>Additional Requirements:</strong> {settings.addRequirements}</p>
    </div>
  );
};

export default DisplayValues;