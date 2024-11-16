import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from './Header';
import PushNotification from './PushNotification';
import EditPushNotification from './EditPushNotification';
// hi
const GenerationPage = () => {
    const [activeButton, setActiveButton] = useState('generator');
    const navigate = useNavigate();

    // Predefined titles and bodies in Malay
    const predefinedTitles = [
        'KIM Ha Neul Panas! 🔥',
        'Drama Panas KIM Ha Neul!',
        'KIM Ha Neul Terhangat! 🌟',
        'KIM Ha Neul Bikin Panas!',
        'KIM Ha Neul & Cuaca Panas!'
    ];

    const predefinedBodies = [
        'Cuaca panas? KIM Ha Neul lagi panas di Nothing Uncovered! Jom tonton sekarang! 🌞',
        'KIM Ha Neul buat hati berdebar di Nothing Uncovered. Jangan ketinggalan! 🌡️',
        'Cuaca panas, drama lagi panas! Saksikan KIM Ha Neul di Nothing Uncovered. 🌞',
        'Hari panas? KIM Ha Neul lagi bikin panas di Nothing Uncovered! Tonton sekarang! 🔥',
        'Cuaca panas, drama pun panas! Jangan lepaskan KIM Ha Neul di Nothing Uncovered. 🌡️'
    ];

    // Predefined titles and bodies in English
    const englishTitles = [
        'Kim Na Heul is Hot! 🔥',
        'Hot Drama Kim Na Heul!',
        'The Hottest Kim Na Heul! 🌟',
        'Kim Na Heul is Heating Up!',
        'Kim Na Heul & Hot Weather!'
    ];

    const englishBodies = [
        'Hot weather? Kim Na Heul is on fire in Nothing Uncovered! Watch now! 🌞',
        'Kim Na Heul makes hearts race in Nothing Uncovered. Don’t miss it! 🌡️',
        'Hot weather, hotter drama! Watch Kim Na Heul in Nothing Uncovered. 🌞',
        'Hot day? Kim Na Heul is heating things up in Nothing Uncovered! Watch now! 🔥',
        'Hot weather, hot drama! Don’t miss Kim Na Heul in Nothing Uncovered. 🌡️'
    ];

    const [titles, setTitles] = useState(predefinedTitles);
    const [bodies, setBodies] = useState(predefinedBodies);
    const [isEnglish, setIsEnglish] = useState(false); // State to track the current language

    const handleTitleChange = (index, value) => {
        const newTitles = [...titles];
        newTitles[index] = value;
        setTitles(newTitles);
    };

    const handleBodyChange = (index, value) => {
        const newBodies = [...bodies];
        newBodies[index] = value;
        setBodies(newBodies);
    };

    // Function to switch to English
    const switchToEnglish = () => {
        setTitles(englishTitles);
        setBodies(englishBodies);
        setIsEnglish(true); // Update state to indicate English is active
    };

    // Function to switch back to Malay
    const switchToMalay = () => {
        setTitles(predefinedTitles);
        setBodies(predefinedBodies);
        setIsEnglish(false); // Update state to indicate Malay is active
    };

    return (
        <div className="h-screen flex flex-col">
            <Header activeButton={activeButton} handleButtonClick={setActiveButton} />

            {/* Main Content Area */}
            <div className="flex flex-grow bg-[#F5F5F5]">
                {/* First Section (3/5) */}
                <div className="flex-grow flex flex-col items-start w-3/5 pt-8 pl-16">

                    <div className='flex'>
                        <div className="pl-8">
                            {/* Back Button */}
                            <button className="bg-white text-pink-500 border-2 border-pink-500 text-lg font-bold py-2 px-4 rounded-lg mb-4 hover:bg-pink-100 transition duration-300" onClick={() => navigate('/')}>
                                Return to Generation Settings
                            </button>
                        </div>

                        {/* Language Switch Button */}
                        <div className="pl-8">
                            {isEnglish ? (
                                <button 
                                    className="bg-white text-blue-500 border-2 border-blue-500 text-lg font-bold py-2 px-4 rounded-lg mb-4 hover:bg-blue-100 transition duration-300" 
                                    onClick={switchToMalay}
                                >
                                    Switch to Malay
                                </button>
                            ) : (
                                <button 
                                    className="bg-white text-blue-500 border-2 border-blue-500 text-lg font-bold py-2 px-4 rounded-lg mb-4 hover:bg-blue-100 transition duration-300" 
                                    onClick={switchToEnglish}
                                >
                                    Switch to English
                                </button>
                            )}
                        </div>
                    </div>

                    {/* Right Section for Columns */}
                    <div className="flex-grow flex flex-col w-full items-center">
                        <div className="flex justify-around w-full flex-grow">
                            <EditPushNotification
                                titles={titles}
                                bodies={bodies}
                                onTitleChange={handleTitleChange}
                                onBodyChange={handleBodyChange}
                            />
                        </div>
                    </div>
                    {/* Regenerate Button */}
                    <div className="flex justify-center mb-4 w-full px-6 mt-4 mb-8">
                        <button className="bg-[#F5B919] w-full text-3xl text-black font-bold py-3 px-6 rounded-lg shadow-md hover:bg-yellow-600 transition duration-300">
                            Regenerate All
                        </button>
                    </div>
                </div>

                {/* Vertical Line Separator */}
                <div className="w-1 bg-gray-300 my-10"></div>

                {/* Second Section (2/5) */}
                <div className="flex flex-col justify-center items-center w-2/5">
                    <div className="flex items-start">
                        <h2 className="text-2xl font-bold">Push Notifications</h2>
                    </div>
                    <div className="w-4/5 h-full bg-white flex flex-col rounded-lg shadow-md mt-4 overflow-y-auto" style={{ maxHeight: '700px' }}>
                        <div className="flex flex-col w-full">
                            {titles.map((title, index) => (
                                <PushNotification
                                    key={index}
                                    title={title}
                                    description={bodies[index]}
                                />
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GenerationPage;