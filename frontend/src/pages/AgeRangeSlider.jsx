import React, { useState, useContext, useEffect } from 'react';
import ReactSlider from 'react-slider';
import { SettingsContext } from './SettingsContext';
// hi
const AgeRangeSlider = ({ setAge }) => {
    const { settings, setSettings } = useContext(SettingsContext);
    const [ageRange, setAgeRange] = useState(settings.age); // Initialize with default values

    // Effect to sync with context settings on mount
    useEffect(() => {
        if (settings.ageRange) {
            setAgeRange(settings.ageRange); // Set initial slider value from context
        }
    }, [settings.ageRange]);

    const handleSliderChange = (value) => {
        setAgeRange(value);
        setAge(value); // Set age as an array in the parent component
        setSettings(prevSettings => ({
            ...prevSettings,
            age: value // Update context with new age range
        })); 
    };

    return (
        <div className="mb-4">
            <div className="flex">
                <label className="block font-bold text-lg text-gray-700">Target Age</label>
                <label className="text-red-400 font-bold text-lg ml-1">*</label>

                <div className="pl-12 flex justify-center text-sm font-bold">
                    <span>{ageRange[0]} years t</span>
                    <span>o {ageRange[1]} years</span>
                </div>
            </div>

            <ReactSlider
                className="slider text-sm"
                thumbClassName="thumb"
                trackClassName="track"
                value={ageRange} // Use local state for the slider value
                onChange={handleSliderChange}
                min={0}
                max={100}
                renderThumb={(props, state) => <div {...props}>{state.valueNow}</div>}
            />

            <style jsx>{`
                .slider {
                    width: 100%;
                    height: 20px;
                    background: #ddd;
                }
                .track {
                    background: #F5B919;
                }
                .thumb {
                    height: 25px;
                    width: 25px;
                    background: #fff;
                    border: 2px solid #F5B919;
                    border-radius: 50%;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
            `}</style>
        </div>
    );
};

export default AgeRangeSlider;