import React, { useContext, useState } from "react";
import Header from './Header';
import { SettingsContext } from './SettingsContext';

export const GenerationHistory = () => {
    const { settings } = useContext(SettingsContext);
    const [activeButton, setActiveButton] = useState('generation_history'); // State for the Active page

    const handleButtonClick = (button) => {
        setActiveButton(button);
    };

    const transformGenHistory = (genHistory) => {
        const transformedHistory = [];
        let currentHeading = null;

        genHistory.forEach(item => {
            if (item.heading) {
                // If we encounter a heading, create a new entry in the transformed array
                currentHeading = {
                    heading: item.heading,
                    generations: []
                };
                transformedHistory.push(currentHeading);
            } else if (currentHeading) {
                // If we have a current heading, push the item into its generations array
                currentHeading.generations.push(item);
            }
        });

        return transformedHistory.reverse();;
    };

    const newGenHistory = transformGenHistory(settings.genHistory);

    // State to track which sections are expanded
    const [expandedSections, setExpandedSections] = useState({});

    const toggleSection = (heading) => {
        setExpandedSections(prev => ({
            ...prev,
            [heading]: !prev[heading] // Toggle the expanded state for the clicked heading
        }));
    };

    return (
        <div className="h-screen flex flex-col" style={{ backgroundColor: '#F5F5F5' }}>
            <Header activeButton={activeButton} handleButtonClick={handleButtonClick} />
            <h1 className="text-3xl font-bold mb-5 pt-8 pl-8">Generation History</h1>
            <div className="space-y-4 pl-8 pr-8">
                {newGenHistory.map((item, index) => (
                    <div key={index} className="bg-[#F5B919] p-4 rounded-lg shadow-md">
                        {/* Render the heading with click handler */}
                        <h2 
                            className="text-xl font-bold cursor-pointer" 
                            onClick={() => toggleSection(item.heading)}
                        >
                            {item.heading}
                        </h2>
                        {/* Render generations if the section is expanded */}
                        {expandedSections[item.heading] && (
                            <div className="flex justify-between mt-2">
                                <div className="w-1/2 pr-2">
                                    {/* Render the English generations */}
                                    {item.generations.map((generation, genIndex) => (
                                        <div key={genIndex} className="mb-4">
                                            <h3 className="text-xl font-semibold">{generation.english.title}</h3>
                                            <p className="text-gray-700">{generation.english.body}</p>
                                        </div>
                                    ))}
                                </div>
                                <div className="w-1/2 pl-2">
                                    {/* Render the Malay generations */}
                                    {item.generations.map((generation, genIndex) => (
                                        <div key={genIndex} className="mb-4">
                                            {generation.malay && (
                                                <>
                                                    <h3 className="text-xl font-semibold">{generation.malay.title}</h3>
                                                    <p className="text-gray-700">{generation.malay.body}</p>
                                                </>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};