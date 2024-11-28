import React, { useState, useContext, useEffect } from 'react';
import { SettingsContext } from './SettingsContext';

const TrendComponent = ({ title, trendClass }) => {
    const { settings, setSettings } = useContext(SettingsContext);
    const [checked, setChecked] = useState(false);

    // Initialize the checked state based on the selectedTrend value in settings
    useEffect(() => {
        setChecked(settings.selectedTrend === title);
    }, [settings.selectedTrend, title]);

    const handleCheckboxChange = () => {
        const newChecked = !checked;
        setChecked(newChecked);
        setSettings(prevState => ({
            ...prevState,
            selectedTrend: newChecked ? title : ''
        }));
    };

    console.log('TrendComponent:', { title, trendClass });

    return (
        <div className='px-4 sm:px-2 py-3'>
            <div className={`flex items-center rounded-lg p-4 mb-4 shadow-md ${checked ? 'bg-yellow-300 border-black' : 'bg-[#F5B919]'}`}>
                <div 
                    className={`w-4 h-4 border-2 rounded-lg flex items-center justify-center mr-4 cursor-pointer ${checked ? 'bg-gray-800' : 'bg-white'}`} 
                    onClick={handleCheckboxChange}
                >
                    {checked && <div className="w-2 h-2 bg-white rounded-full" />}
                </div>
                <div className='flex-1'>
                    <p className="font-bold text-md">{trendClass}</p>
                    <h3 className="text-md">{title}</h3>
                </div>
            </div>
        </div>
    );
};

export default TrendComponent;