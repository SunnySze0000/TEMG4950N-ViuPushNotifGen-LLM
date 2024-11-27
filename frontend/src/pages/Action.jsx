import React, { useState, useRef, useEffect } from 'react';

const Action = ({ title, body, onRefineRequest }) => {
    const [showOptions, setShowOptions] = useState(false);
    const actionRef = useRef(null); // Create a ref for the action button

    const handleButtonClick = () => {
        setShowOptions(prev => !prev);
    };

    const handleOptionClick = (option) => {
        console.log(option); // Handle the option click (e.g., refine content or confirm)
        setShowOptions(false); // Hide options after selection
    };

    // Effect to handle clicks outside the component
    useEffect(() => {
        const handleClickOutside = (event) => {
            // Check if the click is outside the action button
            if (actionRef.current && !actionRef.current.contains(event.target)) {
                setShowOptions(false); // Close options if clicked outside
            }
        };

        // Attach the event listener
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            // Cleanup the event listener on component unmount
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    return (
        <div className="flex-grow flex flex-col items-start ml-4 relative" ref={actionRef}>
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
                            onClick={() => {
                                onRefineRequest(title, body);
                                console.log({ title, body });
                                handleOptionClick('Refine Content');
                            }}
                        >
                            Refine Content
                        </button>
                        <div className="border-t border-black my-1"></div>
                        <button 
                            className="w-full text-left text-black py-2 px-4 rounded-lg mb-0"
                            onClick={() => {
                                const copiedText = `${title}\n${body}`;
                                navigator.clipboard.writeText(copiedText);
                                handleOptionClick('Confirm and Finalise');
                            }}
                        >
                            Confirm and Copy
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Action;
