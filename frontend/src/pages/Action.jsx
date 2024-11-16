import React, { useState } from 'react';
// hi
const Action = () => {
    const [showOptions, setShowOptions] = useState(false);

    const handleButtonClick = () => {
        setShowOptions(!showOptions);
    };

    const handleOptionClick = (option) => {
        console.log(option); // Handle the option click (e.g., refine content or confirm)
        setShowOptions(false); // Hide options after selection
    };

    return (
        <div className="flex-grow flex flex-col items-start ml-4 relative">
            <button 
                className="text-4xl mt-6 font-bold p-0 rounded-lg focus:outline-none" 
                onClick={handleButtonClick}
            >
                &#x22EE; {/* Three dots icon */}
            </button>
            {showOptions && (
                <div className="absolute top-0 mt-6 left-full w-48 bg-white rounded-lg shadow-md z-10">
                    <div className="p-0">
                        <button 
                            className="w-full text-left text-black py-2 px-4 rounded-lg mb-0"
                            onClick={() => handleOptionClick('Refine Content')}
                        >
                            Refine Content
                        </button>
                        <div className="border-t border-black my-1"></div>
                        <button 
                            className="w-full text-left text-black py-2 px-4 rounded-lg mb-0"
                            onClick={() => handleOptionClick('Confirm and Finalise')}
                        >
                            Confirm and Finalise
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Action;