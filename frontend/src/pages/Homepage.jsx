import React, { useEffect, useState } from "react";
import ToggleSwitch from './ToggleSwitch';
import Header from './Header';
import CreativitySlider from './Slider';
import TrendComponent from "./TrendComponent";
import { useNavigate } from 'react-router-dom';
import AgeRangeSlider from "./AgeRangeSlider";
import ContentNameSelector from "./ContentNameSelector";
import StarNameSelector from './StarNameSelector';
// hi
const ViuDataContext = React.createContext({
  viuData: [], fetchViudata: () => {}
})

export const Homepage = () => {
  //Call a get api to retrieve viu data for dropdown menus of cast and show
  // const [viuDatas, setViuDatas] = useState([])

  // const fetchViuData = async () => {
  //   const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/viuData`);
  //   const data = await response.json()
  //   console.log(data)
  //   setViuDatas(data.key)
  // }

  // useEffect(() => { fetchViuData() }, [])

  // State to track the active button
  const [activeButton, setActiveButton] = useState('generator'); 
  const [promotionType, setPromotionType] = useState(''); 
  const [creativity, setCreativity] = useState(0); 
  const [age, setAge] = useState([18, 65]);
  const [starName, setStarName] = useState(''); 
  const [isFormEnabled, setIsFormEnabled] = useState(false);
  const [showTrends, setShowTrends] = useState(false);
  const [selectedContent, setSelectedContent] = useState('');
  const [allSeriesData, setAllSeriesData] = useState([]);
  const [isEmoji, setIsEmoji] = useState(false);
  const [isSlang, setIsSlang] = useState(false);
  const [addRequirements, setAddRequirements] = useState(''); 
  const [englishTitles, setEnglishTitles] = useState([]);
  const [englishBodies, setEnglishBodies] = useState([]);
  const [malayTitles, setMalayTitles] = useState([]);
  const [malayBodies, setMalayBodies] = useState([]);
  const [trendTitles, setTrendTitles] = useState([]);
  const [trendClassifier, setTrendClassifier] = useState([]);
  const [selectedTrend, setSelectedTrend] = useState('');
  const [loading, setLoading] = useState(false);
  const [trendLoading, setTrendLoading] = useState(false);
  const [inputShow, setInputShow] = useState({});
  const [message, setMessage] = useState('');

  const backendUrl = process.env.REACT_APP_BACKEND_URL

  const genPush = async (inputData) => {
    const response = await fetch(`${backendUrl}/genPush`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(inputData),
    });
    const data = await response.json();
    console.log(data);
    return data
  };

  const regenTrend = async (inputShow) => {
    console.log('Sending request with payload:', inputShow); // Log the payload
    const response = await fetch(`${backendUrl}/refreshTrends`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(inputShow),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    console.log(data);
    return data;
  };

  const genTrend = async () => {
    const response = await fetch(`${backendUrl}/scrapeTrends`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    console.log(data);
    return data;
  };

  const navigate = useNavigate();

  const handleGenPush = async () => {
    const inputData = {
      push_type: promotionType, // Use the promotionType state
      series_name: selectedContent, // Use the selectedContent state
      cast_name: starName, // Use the starName state
      creativity: creativity/100, // Use the creativity state
      demographics: age, // Use the age state
      isEmojis: isEmoji, // Use the isEmoji state
      isSlangs: isSlang, // Use the isSlang state 
      addRequirements: addRequirements, // Use the addRequirements state
      selected_trend: selectedTrend, // Use the selectedTrend state
    };
  
    console.log("Sending request data:", JSON.stringify(inputData));

    //Start loading
    setLoading(true);

    try {
      const data = await genPush(inputData);
      setMessage(JSON.stringify(data, null, 2));

      // Initialize arrays to hold the titles and bodies
      const newEnglishTitles = [];
      const newEnglishBodies = [];
      const newMalayTitles = [];
      const newMalayBodies = [];

      // Iterate over the keys in the response
      for (const key in data) {
        if (data[key].english) {
          newEnglishTitles.push(data[key].english.title);
          newEnglishBodies.push(data[key].english.body);
        }
        if (data[key].malay) {
          newMalayTitles.push(data[key].malay.title);
          newMalayBodies.push(data[key].malay.body);
        }
      }

      // Update state with the new values
      setEnglishTitles(newEnglishTitles);
      setEnglishBodies(newEnglishBodies);
      setMalayTitles(newMalayTitles);
      setMalayBodies(newMalayBodies);

      navigate('/generation', {
        state: {
          englishTitles: newEnglishTitles,
          englishBodies: newEnglishBodies,
          malayTitles: newMalayTitles,
          malayBodies: newMalayBodies,
        },
      });
  
    } catch (error) {
      console.error("Error generating push:", error);
      setMessage("An error occurred while generating the push.");
    } finally {
      // Stop loading
      setLoading(false);
    }
  };

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
            setAllSeriesData(data); // Store all series data
        })
        .catch(error => console.error('Error fetching the JSON:', error));
  }, []);

  const handleContentSelection = (content) => {
    setSelectedContent(content);
  };

  // Function to handle refresh trends logic
  const handleRefreshTrends = async () => {
    const newInputShow = {
      series_name: selectedContent, // Use the selectedContent state
      cast_name: starName, // Use the starName state
    };
    setInputShow(newInputShow);
    setTrendLoading(true);
    try {
      const data = await regenTrend(newInputShow);

      const newTrendTitles = []
      const newTrendClassifier = []

      for (const key in data) {
        if (data[key].trend_title) {
          newTrendTitles.push(data[key].trend_title);
        }
        if (data[key].classification_type) {
          newTrendClassifier.push(data[key].classification_type)
        }
      }
      setTrendTitles(newTrendTitles);
      setTrendClassifier(newTrendClassifier);
      setShowTrends(true);
    }
    catch (error) {
      console.error("Error generating trend:", error);
      setMessage("An error occurred while generating the trend.");
    } finally {
      // Stop loading
      setTrendLoading(false);
      console.log('Trends refreshed!');
    }
  };

  const isFormValid = () => {
    return promotionType &&
           age &&
           selectedContent &&
           (promotionType === 'cast-driven' ? starName : true);
  };

  useEffect(() => {
    setIsFormEnabled(isFormValid());
  }, [promotionType, age, selectedContent, starName]); 

  const handlePromotionTypeChange = (event) => {
    setPromotionType(event.target.value);
  };

  const handleGenerateTrends = async () => {
    setShowTrends(true);
    setTrendLoading(true);
    try {
      const data = await genTrend();

      const newTrendTitles = []
      const newTrendClassifier = []

      for (const key in data) {
        if (data[key].trend_title) {
          newTrendTitles.push(data[key].trend_title);
        }
        if (data[key].classification_type) {
          newTrendClassifier.push(data[key].classification_type)
        }
      }
      setTrendTitles(newTrendTitles);
      setTrendClassifier(newTrendClassifier);
      setShowTrends(true);
    }
    catch (error) {
      console.error("Error generating trend:", error);
      setMessage("An error occurred while generating the trend.");
    } finally {
      // Stop loading
      setTrendLoading(false);
    }
  };
  
  const handleTrendSelect = (title) => {
    setSelectedTrend(title); // Update selected trend with the title from TrendComponent
  };

  // Function to handle button clicks
  const handleButtonClick = (button) => {
    setActiveButton(button);
  };

  const isCastDriven = promotionType === 'cast-driven';

  return (
    <div className="h-screen flex flex-col">
    <Header activeButton={activeButton} handleButtonClick={handleButtonClick} />
    {loading && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-t-4 border-[#F5B919] border-t-transparent mx-auto mb-4"></div>
          <p className="text-lg font-semibold">Generating...</p>
        </div>
      </div>
    )}
    
    {/* Main Content Area */}
    <div className="flex flex-grow bg-[#F5F5F5]">
        {/* First Section (3/5) */}
        <div className="flex-grow flex flex-col items-center">
          <div className="flex items-center pr-11 mb-8 mt-6">
            <img src="viu_logo.png" className="w-60 ml-8" alt="VIU Logo" />
            <h2 className="text-5xl font-bold text-[#F5B919] ml-8">Push Notification Generator</h2>
          </div>

          {/* Input Fields Section */}
          <div className="flex flex-col w-full px-36">
            <div className="flex space-x-10 justify-center">
              
            {/* Promotion Type Dropdown */}
            <div className="flex-grow mb-4 w-full">
              <div className="flex">
                <label className="block text-sm font-bold text-lg text-gray-700">Promotion Type</label>
                <label className="text-red-400 font-bold text-lg ml-1">*</label>
              </div>
              <select
                className="mt-1 block h-8 w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-[#F5B919] focus:border-[#F5B919]"
                value={promotionType}
                onChange={handlePromotionTypeChange}
              >
                <option value="" disabled hidden>
                  Select Promotion
                </option>
                <option value="content-based">Content-based promotion</option>
                <option value="cast-driven">Cast-driven promotion</option>
              </select>
            </div>

            <div className="w-full">
              <CreativitySlider value={creativity} onChange={(e) => setCreativity(e.target.value)} />
            </div>
            
          </div>

          <div className="grid grid-cols-2 gap-4">
              {/* Content Name Selector */}
              <ContentNameSelector promotionType={promotionType} onContentSelect={handleContentSelection} />

              {/* Star Name Selector */}
              <StarNameSelector selectedContent={selectedContent} allSeriesData={allSeriesData} isCastDriven={isCastDriven} onStarSelect={setStarName}/>
              <AgeRangeSlider setAge={setAge} />

              <div className="flex flex-col">
              <ToggleSwitch 
                label="Include Local Lingo?" 
                checked={isSlang} 
                onChange={() => setIsSlang(!isSlang)} 
              />
              <ToggleSwitch 
                label="Include Emojis?" 
                checked={isEmoji} 
                onChange={() => setIsEmoji(!isEmoji)} 
              />
              </div>
            </div>

            {/* Additional Input Field */}
            <div className="flex flex-col w-full mb-4">
              <label className="block text-sm font-bold text-lg text-gray-700 mb-2">Additional Input</label>
              <textarea
                placeholder="Enter additional information here..."
                value={addRequirements} // Bind the value to the state variable
                onChange={(e) => setAddRequirements(e.target.value)} // Step 2: Update state on change
                className="mt-1 block w-full h-60 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-[#F5B919] focus:border-[#F5B919] p-2"
              />
            </div>

            {/* Generate Button */}
            <div className="flex justify-center mb-4">
              <button className={`bg-[#F5B919] w-full text-3xl text-black font-bold py-3 px-6 rounded-lg shadow-md hover:bg-yellow-600 transition duration-300 ${isFormEnabled ? '' : 'cursor-not-allowed opacity-50'}`} disabled={!isFormEnabled} onClick={handleGenPush} >
                Generate
              </button>
            </div>
          </div>
        </div>

        {/* Vertical Line Separator */}
        <div className="w-1 bg-gray-300 my-10 mr-10"></div>

        {/* Second Section (2/5) */}
        <div className="flex flex-col justify-center items-center w-2/5 mt-10 mb-10 relative">
        {trendLoading && (
          <div className= "absolute inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
            <div className="bg-white p-6 rounded-lg shadow-lg text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-t-4 border-[#F5B919] border-t-transparent mx-auto mb-4"></div>
              <p className="text-lg font-semibold">Generating Trend...</p>
            </div>
          </div>
        )}
          <div className="flex md:flex-row items-center">
            <h2 className="text-xl md:text-2xl font-bold mr-4 mb-2 md:mb-0">Trends</h2>
            {/* Refresh Trends Button */}
                  {showTrends && (<button 
                      onClick={handleRefreshTrends} 
                      className="bg-green-500 text-white text-sm md:text-xs font-bold py-2 px-4 rounded-full hover:bg-green-600 transition duration-300"
                  >
                      Refresh Trends
                  </button>)}
          </div>
          <div className="w-full max-w-4xl h-auto bg-white flex justify-center items-center rounded-lg shadow-md mt-4 p-4">
            {!showTrends ? (
              <button className={`bg-[#F5B919] text-black font-bold py-2 px-4 hover:bg-yellow-600 rounded-full cursor-not-allowed" ${!showTrends ? '' : 'cursor-not-allowed opacity-50'}`} disabled={showTrends} onClick={handleGenerateTrends} >
                Generate Trends
              </button>
            ) : (
              <div className="flex flex-col w-full max-h-screen overflow-y-auto p-4">
                {trendTitles.map((title, index) => (
                  <TrendComponent 
                    key={index} 
                    title={title} 
                    trendClass={trendClassifier[index]} 
                    onTrendSelect={handleTrendSelect}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
