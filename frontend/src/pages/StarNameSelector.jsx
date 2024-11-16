import React, { useEffect, useState } from 'react';
// hi
const StarNameSelector = ({ selectedContent, allSeriesData, isCastDriven, onStarSelect}) => {
    const [uniqueCasts, setUniqueCasts] = useState([]);
    const [filteredCasts, setFilteredCasts] = useState([]);

    const handleChange = (event) => {
        onStarSelect(event.target.value); // Call the function to set the star name
      };

    useEffect(() => {
        // Extract unique casts from all series
        const allCasts = new Set();
        allSeriesData.forEach(item => {
            if (item.MAIN_CASTS) {
                item.MAIN_CASTS.split(',').forEach(cast => allCasts.add(cast.trim()));
            }
            if (item.SUPPORTING_CASTS) {
                item.SUPPORTING_CASTS.split(',').forEach(cast => allCasts.add(cast.trim()));
            }
        });
        setUniqueCasts(Array.from(allCasts));
    }, [allSeriesData]);

    useEffect(() => {
        // Filter casts based on the selected content
        if (selectedContent) {
            const selectedSeries = allSeriesData.find(item => item.GROUP_SERIES_NAME === selectedContent);
            const selectedCasts = new Set();
            if (selectedSeries) {
                if (selectedSeries.MAIN_CASTS) {
                    selectedSeries.MAIN_CASTS.split(',').forEach(cast => selectedCasts.add(cast.trim()));
                }
                if (selectedSeries.SUPPORTING_CASTS) {
                    selectedSeries.SUPPORTING_CASTS.split(',').forEach(cast => selectedCasts.add(cast.trim()));
                }
            }
            setFilteredCasts(Array.from(selectedCasts));
        } else {
            setFilteredCasts([]); // Reset if no content is selected
        }
    }, [selectedContent, allSeriesData]);

    return (
        <div className="mb-4">
            <div className="flex">
                <label className="block text-sm font-bold text-lg text-gray-700">Star Name</label>
                <label className="text-red-400 font-bold text-lg ml-1">*</label>
            </div>
            <select
                className={`mt-1 block w-full h-8 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-[#F5B919] focus:border-[#F5B919] ${!isCastDriven ? 'opacity-50 cursor-not-allowed' : ''}`}
                onChange={handleChange}
                disabled={!isCastDriven} // Disable if cast-driven promotion is not selected
                defaultValue="" // Set default value to show placeholder
            >
                <option value="" disabled={!isCastDriven}>Select Star Name</option> {/* Placeholder option */}
                {(isCastDriven ? filteredCasts : uniqueCasts).length > 0 ? (
                    (isCastDriven ? filteredCasts : uniqueCasts).map((cast, index) => (
                        <option key={index} value={cast}>
                            {cast}
                        </option>
                    ))
                ) : (
                    <option value="" disabled>No casts available</option>
                )}
            </select>
        </div>
    );
};

export default StarNameSelector;