import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { SettingsContext } from './SettingsContext';

const RegenPopup = ({ isOpen, onClose, push }) => {
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [additionalRequirements, setAdditionalRequirements] = useState('');
    const { settings, setSettings } = useContext(SettingsContext);
    
    const navigate = useNavigate();

    const backendUrl = process.env.REACT_APP_BACKEND_URL

    const regenPush = async (inputData) => {
        const response = await fetch(`${backendUrl}/regenPush`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(inputData),
        });
        const data = await response.json();
        console.log(data);
        return data
    };
    
    const handleRegenPush = async () => {
        let inputData;
        if (push == null) {
            inputData = {
                addRequirements: additionalRequirements,
            };
        } else {
            inputData = {
                basePush: push,
                addRequirements: additionalRequirements,
            };
        }
    
        console.log("Sending request data:", inputData);
    
        setLoading(true);
    
        try {
            const data = await regenPush(inputData);
            setMessage(JSON.stringify(data, null, 2));
    
            // Initialize arrays to hold the titles and bodies
            const newEnglishTitles = [];
            const newEnglishBodies = [];
            const newMalayTitles = [];
            const newMalayBodies = [];
    
            // Initialize an array to hold new entries
            const newGenHistoryEntries = [];

            // Get current date and time
            const now = new Date();
            const formattedDate = now.toLocaleString(); 

            // Iterate over the keys in the response
            for (const key in data) {
                if (data[key].english) {
                    newEnglishTitles.push(data[key].english.title);
                    newEnglishBodies.push(data[key].english.body);
    
                    // Push entries directly to newGenHistoryEntries
                    newGenHistoryEntries.push({
                        english: {
                            title: data[key].english.title,
                            body: data[key].english.body,
                        },
                        malay: data[key].malay ? {
                            title: data[key].malay.title,
                            body: data[key].malay.body,
                        } : null,
                    });
                }
                if (data[key].malay) {
                    newMalayTitles.push(data[key].malay.title);
                    newMalayBodies.push(data[key].malay.body);
                }
            }
    
            // Update SettingsContext with new values
            setSettings((prevSettings) => {
                const updatedGenHistory = [...prevSettings.genHistory];
    
                // Add a new entry with heading and new entries
                updatedGenHistory.push({
                    heading: `Regeneration - ${formattedDate}`,
                });
    
                // Add the generated entries directly to the updatedGenHistory
                newGenHistoryEntries.forEach(entry => {
                    updatedGenHistory.push(entry);
                });
    
                return {
                    ...prevSettings,
                    englishTitles: newEnglishTitles,
                    englishBodies: newEnglishBodies,
                    malayTitles: newMalayTitles,
                    malayBodies: newMalayBodies,
                    genHistory: updatedGenHistory,
                };
            });
    
            onClose();
    
            navigate('/generation', {
                state: {
                    englishTitles: newEnglishTitles, // Use updated titles
                    englishBodies: newEnglishBodies, // Use updated bodies
                    malayTitles: newMalayTitles,
                    malayBodies: newMalayBodies,
                },
            });
    
        } catch (error) {
            console.error("Error generating push:", error);
            setMessage("An error occurred while generating the push.");
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white p-6 rounded-lg shadow-md max-w-2xl w-full">
                <h2 className="text-xl font-bold mb-4">Regenerate Push</h2>
                <textarea
                    placeholder="Enter additional requirements"
                    value={additionalRequirements}
                    onChange={(e) => setAdditionalRequirements(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded mb-4 resize-none h-48"
                />
                <div className="flex space-x-4 mt-4">
                    <button onClick={onClose} className="bg-gray-300 px-4 py-2 rounded">Cancel</button>
                    <button onClick={handleRegenPush} className="bg-blue-500 text-white px-4 py-2 rounded">Regenerate</button>
                </div>
            </div>
            {loading && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
                    <div className="bg-white p-6 rounded-lg shadow-lg text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-4 border-t-4 border-[#F5B919] border-t-transparent mx-auto mb-4"></div>
                    <p className="text-lg font-semibold">Regenerating...</p>
                    </div>
                </div>
                )
            }
        </div>
    );
};

export default RegenPopup;