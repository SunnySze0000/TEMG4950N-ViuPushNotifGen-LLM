import React, { useEffect, useState, useContext} from 'react';
import { SettingsContext } from './SettingsContext';

// hi
const ContentNameSelector = ({promotionType, onContentSelect}) => {
    const { settings, setSettings } = useContext(SettingsContext);
    const [seriesNames, setSeriesNames] = useState([]);

    useEffect(() => {
        // Fetch the JSON data
        fetch('/malay_meta.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Extract unique series names
                const uniqueSeriesNames = [...new Set(data.map(item => item.GROUP_SERIES_NAME))];
                setSeriesNames(uniqueSeriesNames);
            })
            .catch(error => console.error('Error fetching the JSON:', error));
    }, []);

    const handleChange = (event) => {
        onContentSelect(event.target.value); // Call the onContentSelect prop with the selected value
    };

    return (
        <div className="mb-4">
            <div className="flex">
                <label className="block text-lg font-bold text-lg text-gray-700">Content Name</label>
                <label className="text-red-400 font-bold text-lg ml-1">*</label>
            </div>
            <select
                className={`mt-1 block w-full h-8 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-[#F5B919] focus:border-[#F5B919] ${!promotionType ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={!promotionType} // Disable if promotionType is not chosen
                onChange={handleChange}
                value={settings.selectedContent} // Set default value to show placeholder
            >
                <option value="" disabled>Select Content Name</option> {/* Placeholder option */}
                {seriesNames.map((name, index) => (
                    <option key={index} value={name}>
                        {name}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default ContentNameSelector;