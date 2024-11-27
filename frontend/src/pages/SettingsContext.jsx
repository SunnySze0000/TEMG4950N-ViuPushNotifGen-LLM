import React, { createContext, useState } from 'react';
export const SettingsContext = createContext();
// hi
export const SettingsProvider = ({ children }) => {
  const [settings, setSettings] = useState({
    promotionType: '',
    creativity: 0,
    age: [18, 65],
    starName: '',
    isEmoji: false,
    isSlang: false,
    addRequirements: '',
    selectedContent: '',
    returnToGeneration: false,
    englishTitles: [], // Add englishTitles to settings
    malayTitles: [],   // Add malayTitles to settings
    englishBodies: [], // Add englishBodies to settings
    malayBodies: [],   // Add malayBodies to settings
    titles: [],        // Add titles to settings
    bodies: [],        // Add bodies to settings
    genHistory: []
  });

  return (
    <SettingsContext.Provider value={{ settings, setSettings }}>
      {children}
    </SettingsContext.Provider>
  );
};