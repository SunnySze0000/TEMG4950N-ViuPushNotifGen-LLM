import React, { useState } from 'react';
import SelectThumbnail from './SelectThumbnail';
// hii
let expandedNotification = null; // Static variable to track the currently expanded notification

const PushNotification = ({ title, description, imageSrc, appName, iconSrc }) => {
    const [expanded, setExpanded] = useState(false);
    const [showModal, setShowModal] = useState(false); 
    const [selectedThumbnail, setSelectedThumbnail] = useState(imageSrc); // New state for selected thumbnail

    const handleNotificationClick = () => {
        if (expanded) {
            setExpanded(false);
            expandedNotification = null; // Reset the expanded notification
        } else {
            if (expandedNotification) {
                expandedNotification.setExpanded(false); // Collapse the previously expanded notification
            }
            setExpanded(true);
            expandedNotification = { setExpanded }; // Update the static reference to the current notification
        }
    };

    const handleThumbnailClick = () => {
        setShowModal(true);
    };

    const closeModal = () => {
        setShowModal(false);
    };

    const updateThumbnail = (newThumbnail) => {
        setSelectedThumbnail(newThumbnail);
        closeModal(); // Close the modal after updating
    };

    return (
        <div className='px-8 py-3'>
            <div 
                className={`flex flex-col items-start bg-[#F5B919] rounded-lg p-4 mb-4 shadow-md transition-all duration-300 ${expanded ? 'max-h-full' : 'max-h-32 overflow-hidden'}`} 
                onClick={handleNotificationClick}
            >
                <div className='flex w-full justify-between items-center'>
                    <div className='flex items-center'>
                        <img src={iconSrc || "viu_icon.png"} alt="App Icon" className="w-7 h-7 rounded-full mr-3" />
                        <span className="font-semibold">{appName}</span>
                    </div>
                    <span className="text-gray-600 text-sm">1m ago</span>
                </div>
                <div className='flex w-full justify-between items-start'>
                    {expanded ? (
                        <div className="flex flex-col items-center relative">
                            <img src={selectedThumbnail || "viu_icon.png"} alt="Notification Image" className="w-full h-32 rounded-lg mb-2 object-cover" />
                            <button className="absolute top-1/4 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white text-pink-500 border-2 border-pink-500 font-semibold py-1 px-3 rounded-lg z-10" onClick={handleThumbnailClick}>
                                Generate Thumbnail
                            </button>
                            <h3 className="text-lg font-semibold text-center">{title}</h3>
                            <p className="text-gray-600 text-center">{description}</p>
                        </div>
                    ) : (
                        <div className="flex flex-row items-center w-full">
                            <div className="flex flex-col flex-grow max-w-[calc(100%-4rem)]">
                                <h3 className="text-lg font-semibold overflow-hidden text-ellipsis whitespace-nowrap">{title}</h3>
                                <p className="text-gray-600 overflow-hidden text-ellipsis whitespace-nowrap">{description}</p>
                            </div>
                            <img src={selectedThumbnail || "viu_icon.png"} alt="Notification Image" className="w-16 h-16 ml-3 rounded-lg" style={{ flexShrink: 0 }} />
                        </div>              
                    )}
                </div>   
            </div>
            {showModal && <SelectThumbnail onClose={closeModal} onSelectThumbnail={updateThumbnail} />}
        </div>
    );
};

export default PushNotification;