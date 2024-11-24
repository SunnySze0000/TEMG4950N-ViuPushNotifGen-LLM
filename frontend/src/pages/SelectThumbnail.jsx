// SelectThumbnail.jsx
import React, { useState, useEffect, useRef } from 'react';
// hii
const SelectThumbnail = ({ onClose, onSelectThumbnail }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [logoPosition, setLogoPosition] = useState({ x: 250, y: 150 }); // Starting position for the logo
    const [buttonPosition, setButtonPosition] = useState({ x: 450, y: 350 }); // Starting position for the button
    const [draggingLogo, setDraggingLogo] = useState(false);
    const [draggingButton, setDraggingButton] = useState(false);
    const thumbnails = [
        "thumbnail1.png", // Replace with your image sources
        "thumbnail2.png",
        "thumbnail1.png",
        "thumbnail2.png"
    ];
    const canvasRef = useRef(null); // Ref for the canvas

    const handleNext = () => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % thumbnails.length);
    };

    const updateThumbnail = async () => {
        const exportedImageURL = await exportImage(); // Get the exported image URL
        // Update the current thumbnail with the exported image URL
        thumbnails[currentIndex] = exportedImageURL; // Update the thumbnails array
        onSelectThumbnail(exportedImageURL); // Call the onSelectThumbnail with the new image
    };

    const handlePrevious = () => {
        setCurrentIndex((prevIndex) => (prevIndex - 1 + thumbnails.length) % thumbnails.length);
    };

    const handleMouseDown = (e, setDragging) => {
        e.preventDefault();
        setDragging(true);
    };

    const handleMouseMove = (e) => {
        if (draggingLogo || draggingButton) {
            const image = document.querySelector('.thumbnail-image');
            const rect = image.getBoundingClientRect(); // Get the image's bounding rectangle
            const offsetX = e.clientX - rect.left; // Mouse position relative to the left of the image
            const offsetY = e.clientY - rect.top;  // Mouse position relative to the top of the image
    
            if (draggingLogo) {
                const logoWidth = 248.2-115.625; // Replace with actual logo width
                const logoHeight = 96; // Replace with actual logo height
                const newX = Math.max(115.625+0, Math.min(offsetX - logoWidth / 2, rect.width - logoWidth));
                const newY = Math.max(0, Math.min(offsetY - logoHeight / 2, rect.height - logoHeight));
                setLogoPosition({ x: newX, y: newY });
            } else if (draggingButton) {
                const buttonWidth = 190-115.625; // Replace with actual button width
                const buttonHeight = 48; // Replace with actual button height
                const newX = Math.max(115.625+0, Math.min(offsetX - buttonWidth / 2, rect.width - buttonWidth));
                const newY = Math.max(0, Math.min(offsetY - buttonHeight / 2, rect.height - buttonHeight));
                setButtonPosition({ x: newX, y: newY });
            }
        }
    };

    const handleMouseUp = () => {
        setDraggingLogo(false);
        setDraggingButton(false);
    };

    useEffect(() => {
        // Attach mousemove and mouseup listeners to the document
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        // Clean up the event listeners on component unmount
        return () => {
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }, [draggingLogo, draggingButton]);

    const exportImage = () => {
        return new Promise((resolve) => {
            const canvas = canvasRef.current;
            const context = canvas.getContext('2d');
    
            const thumbnailImage = new Image();
            thumbnailImage.src = thumbnails[currentIndex];
    
            thumbnailImage.onload = () => {
                canvas.width = thumbnailImage.width;
                canvas.height = thumbnailImage.height;
    
                context.drawImage(thumbnailImage, 0, 0);
    
                const logoImage = new Image();
                logoImage.src = 'viu_logo.png'; 
                logoImage.onload = () => {
                    const logoWidth = 248.2; 
                    const logoHeight = 96; 
    
                    const logoX = logoPosition.x; 
                    const logoY = logoPosition.y; 
    
                    context.drawImage(logoImage, (logoX - 115.625) / 1.72, logoY / 1.8, logoWidth / 2, logoHeight / 2); 
    
                    const buttonImage = new Image();
                    buttonImage.src = 'cta_button.png'; 
                    buttonImage.onload = () => {
                        const buttonWidth = 190; 
                        const buttonHeight = 48; 
    
                        const buttonX = buttonPosition.x; 
                        const buttonY = buttonPosition.y; 
    
                        context.drawImage(buttonImage, (buttonX - 115.625) / 1.72, buttonY / 1.8, buttonWidth / 2, buttonHeight / 2); 
    
                        const dataURL = canvas.toDataURL('image/png');
    
                        // Trigger download
                        const link = document.createElement('a');
                        link.href = dataURL;
                        link.download = 'thumbnail.png'; // Set the file name
                        document.body.appendChild(link); // Append to body
                        link.click(); // Trigger the download
                        document.body.removeChild(link); // Clean up
    
                        resolve(dataURL); // Resolve the promise with the data URL
                    };
                };
            };
        });
    };

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white p-6 rounded-lg shadow-lg w-1/2 relative">
                <h2 className="text-2xl font-bold mb-2 absolute top-4 left-4 pl-2">Select Thumbnail</h2>
                <button 
                    className="absolute top-4 right-4 text-gray-600 text-4xl pr-2"
                    onClick={onClose}
                >
                    &times; {/* Cross icon */}
                </button>
                <p className="mb-4 pt-6">Choose a thumbnail from the show or episode that will be featured in the push notification.</p>
                <div className="flex flex-col items-center relative">
                    <img 
                        src={thumbnails[currentIndex]} 
                        alt="Thumbnail" 
                        className="w-3/4 h-auto mb-2 thumbnail-image" 
                    />
                    {/* Draggable Logo */}
                    <img 
                        src="viu_logo.png" 
                        alt="Viu Logo" 
                        className="absolute cursor-move h-24" 
                        style={{ left: `${logoPosition.x}px`, top: `${logoPosition.y}px` }} 
                        onMouseDown={(e) => handleMouseDown(e, setDraggingLogo)}
                    />
                    {/* Draggable Call to Action Button */}
                    <button
                        className="absolute border-2 border-[#F5B919] bg-white text-[#F5B919] text-lg py-2 px-4 rounded cursor-move rounded-full"
                        style={{ left: `${buttonPosition.x}px`, top: `${buttonPosition.y}px` }}
                        onMouseDown={(e) => handleMouseDown(e, setDraggingButton)}
                    >
                        Tonton Sekarang &gt;
                    </button>
                    <div className="flex items-center mt-2">
                        <button onClick={handlePrevious} className="text-xl text-gray-600 mr-2">&lt;</button>
                        <span className='text-xl'>{currentIndex + 1} / {thumbnails.length}</span>
                        <button onClick={handleNext} className="text-xl text-gray-600 ml-2">&gt;</button>
                    </div>
                </div>
                <div className="flex justify-end">
                    <button 
                        className="bg-white text-[#3078BE] border-2 border-[#3078BE] py-3 px-6 rounded mr-2 hover:bg-[#3078BE] hover:text-white transition duration-300"
                        onClick={onClose}
                    >
                        Cancel
                    </button>
                    <button 
                        className="bg-white text-[#3078BE] border-2 border-[#3078BE] py-3 px-6 rounded mr-2 hover:bg-[#3078BE] hover:text-white transition duration-300"
                        onClick={updateThumbnail} // Call updateThumbnail on click
                    >
                        Update
                    </button>
                    <button 
                        className="bg-white text-[#3078BE] border-2 border-[#3078BE] py-3 px-6 rounded hover:bg-[#3078BE] hover:text-white transition duration-300"
                        onClick={exportImage} // Call export function on click
                    >
                        Export Image
                    </button>
                </div>
                <canvas ref={canvasRef} style={{ display: 'none' }} /> {/* Hidden canvas for exporting */}
            </div>
        </div>
    );
};

export default SelectThumbnail;