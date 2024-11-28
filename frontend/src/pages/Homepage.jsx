import React, { useEffect, useState, useContext } from "react";
import ToggleSwitch from './ToggleSwitch';
import Header from './Header';
import CreativitySlider from './Slider';
import TrendComponent from "./TrendComponent";
import { useNavigate } from 'react-router-dom';
import AgeRangeSlider from "./AgeRangeSlider";
import ContentNameSelector from "./ContentNameSelector";
import StarNameSelector from './StarNameSelector';
import { SettingsContext } from './SettingsContext';
import DisplayValues from './DisplayValues';
// hii
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
  const { settings, setSettings } = useContext(SettingsContext);
  const [activeButton, setActiveButton] = useState('generator'); 
  const [age, setAge] = useState([18, 65]);
  const [isFormEnabled, setIsFormEnabled] = useState(false);
  const [showTrends, setShowTrends] = useState(false);
  const [selectedContent, setSelectedContent] = useState('');
  const [allSeriesData, setAllSeriesData] = useState([]);
  const [englishTitles, setEnglishTitles] = useState([]);
  const [englishBodies, setEnglishBodies] = useState([]);
  const [malayTitles, setMalayTitles] = useState([]);
  const [malayBodies, setMalayBodies] = useState([]);
  const [trendTitles, setTrendTitles] = useState([]);
  const [trendClassifier, setTrendClassifier] = useState([]);
  const [selectedTrend, setSelectedTrend] = useState('');
  const [loading, setLoading] = useState(false);
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  const handleReturnToGeneration = () => {
    navigate('/generation'); // Navigate back to the generation page
  };

  // Function to toggle the slang setting
    const handleSlangToggle = () => {
        setSettings(prevSettings => ({
          ...prevSettings,
          isSlang: !prevSettings.isSlang // Toggle the current value
      }));
  };

  // Function to toggle the emoji setting
  const handleEmojiToggle = () => {
        setSettings(prevSettings => ({
          ...prevSettings,
          isEmoji: !prevSettings.isEmoji // Toggle the current value
      }));
  };

  const openPopup = () => setIsPopupOpen(true);
  const closePopup = () => setIsPopupOpen(false);

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
      push_type: settings.promotionType, // Use the promotionType state
      series_name: settings.selectedContent, // Use the selectedContent state
      cast_name: settings.starName, // Use the starName state
      creativity: settings.creativity/100, // Use the creativity state
      demographics: settings.age, // Use the age state
      isEmojis: settings.isEmoji, // Use the isEmoji state
      isSlangs: settings.isSlang, // Use the isSlang state
      addRequirements: settings.addRequirements, // Use the addRequirements state
      selected_trend: settings.selectedTrend,
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
      const newGenHistoryEntries = [];

      // Get current date and time
      const now = new Date();
      const formattedDate = now.toLocaleString(); 

      newGenHistoryEntries.push({
        heading: `Initial Generation - ${formattedDate}`,
      });

      // Iterate over the keys in the response
      for (const key in data) {
        if (data[key].english) {
          newEnglishTitles.push(data[key].english.title);
          newEnglishBodies.push(data[key].english.body);
          newGenHistoryEntries.push({
            english: {
              title: data[key].english.title,
              body: data[key].english.body,
            },
            malay: data[key].malay ? {
              title: data[key].malay.title,
              body: data[key].malay.body,
            } : null,
          });
        }
        if (data[key].malay) {
          newMalayTitles.push(data[key].malay.title);
          newMalayBodies.push(data[key].malay.body);
        }
      }

      setSettings((prevSettings) => ({
          ...prevSettings,
          englishTitles: newEnglishTitles,
          englishBodies: newEnglishBodies,
          malayTitles: newMalayTitles,
          malayBodies: newMalayBodies,
          returnToGeneration: true,
          genHistory: [...prevSettings.genHistory, ...newGenHistoryEntries],
      }));

      navigate('/generation', {
        state: {
          englishTitles: settings.englishTitles,
          englishBodies: settings.englishBodies,
          malayTitles: settings.malayTitles,
          malayBodies: settings.malayBodies,
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
    setSettings({ ...settings, selectedContent: content }); // Update selected content
  };

  const handleStarSelection = (star) => {
    setSettings({ ...settings, starName: star }); // Update selected content
  };

  const handleCreativityChange = (value) => {
    setSettings({ ...settings, creativity: value }); // Update context state
  };

  const handleAddRequirementsChange = (e) => {
      const value = e.target.value; // Get the value from the textarea
      setSettings(prevSettings => ({
          ...prevSettings,
          addRequirements: value // Update the addRequirements in context
      }));
  };

  // Function to handle refresh trends logic
  const handleRefreshTrends = async () => {
    const newInputShow = {
      series_name: settings.selectedContent, // Use the selectedContent state
      cast_name: settings.starName, // Use the starName state
    };
    setInputShow(newInputShow);
    setTrendLoading(true);
    try {
      let data = await regenTrend(newInputShow);

      const dataLength = Object.keys(data).length;

      // Append additional data to the response before returning it
      const additionalData = {
        [dataLength + 1]: {
            "classification_type": "Star and Series",
            "trend_title": "Byeon Woo-seok’s ‘Sudden Shower’ earns him a historic win at the 2024 MAMA Awards"
        }
      };

      // Merge the additional data with the existing data
      data = { ...data, ...additionalData };
      console.log(data);

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
      setSettings(prevState => ({
        ...prevState,
        trendTitles: newTrendTitles,
        trendClassifier: newTrendClassifier,
        showTrends: true,
        trendLoading: false
      }));
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
    return settings.promotionType &&
           settings.age &&
           settings.selectedContent &&
           (settings.promotionType === 'cast-driven' ? settings.starName : true);
  };

  useEffect(() => {
    setIsFormEnabled(isFormValid());
  }, [settings.promotionType, settings.age, settings.selectedContent, settings.starName]); 

  const handlePromotionTypeChange = (event) => {
    setSettings({ ...settings, promotionType: event.target.value });
  };

  const handleGenerateTrends = async () => {
  setTrendLoading(true);
    try {
      const data = await genTrend();

      const newTrendTitles = [];
      const newTrendClassifier = [];

      for (const key in data) {
        if (data[key].trend_title) {
          newTrendTitles.push(data[key].trend_title);
        }
        if (data[key].classification_type) {
          newTrendClassifier.push(data[key].classification_type);
        }
      }

      setSettings(prevState => ({
        ...prevState,
        trendTitles: newTrendTitles,
        trendClassifier: newTrendClassifier,
        showTrends: true,
        trendLoading: false
      }));
    } catch (error) {
      console.error("Error generating trend:", error);
      setMessage("An error occurred while generating the trend.");
    } finally {
      // Stop loading
      setTrendLoading(false);
    }
  };
  
  const handleTrendSelect = (title) => {
    setSettings(prevState => ({
      ...prevState,
      selectedTrend: title
    }));
  };

  // Function to handle button clicks
  const handleButtonClick = (button) => {
    setActiveButton(button);
  };

  const isCastDriven = settings.promotionType === 'cast-driven';

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
                <label className="block font-bold text-lg text-gray-700">Promotion Type</label>
                <label className="text-red-400 font-bold text-lg ml-1">*</label>
              </div>
              <select
                className="mt-1 block h-8 w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-[#F5B919] focus:border-[#F5B919]"
                value={settings.promotionType}
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
              <CreativitySlider value={settings.creativity} onChange={handleCreativityChange} />
            </div>
            
          </div>

          <div className="grid grid-cols-2 gap-4">
              {/* Content Name Selector */}
              <ContentNameSelector promotionType={settings.promotionType} onContentSelect={handleContentSelection} selectedContent={settings.selectedContent} />

              {/* Star Name Selector */}
              <StarNameSelector selectedContent={settings.selectedContent} allSeriesData={allSeriesData} isCastDriven={isCastDriven} onStarSelect={handleStarSelection}/>
              <AgeRangeSlider setAge={setAge} />

              <div className="flex flex-col">
              <ToggleSwitch 
                label="Include Local Lingo?" 
                checked={settings.isSlang} 
                onChange={handleSlangToggle} 
              />
              <ToggleSwitch 
                label="Include Emojis?" 
                checked={settings.isEmoji} 
                onChange={handleEmojiToggle} 
              />
              </div>
            </div>

            {/* Additional Input Field */}
            <div className="flex flex-col w-full mb-4">
              <label className="block text-lg font-bold text-xl text-gray-700 mb-2">Additional Input</label>
              <span className="text-sm">
                Give further instructions which will be added at the bottom of the current prompt. 
                You may see the the default prompt settings <a href="#" onClick={openPopup} style={{ color: 'blue', textDecoration: 'underline' }}>here.</a>
              </span>

              {/* Popup structure */}
              {isPopupOpen && (
                <>
                  <div className="rounded-lg" style={{ position: 'fixed', left: '50%', top: '50%', transform: 'translate(-50%, -50%)', border: '1px solid #ccc', padding: '20px', backgroundColor: 'white', zIndex: 1000 }}>
                    <div className="flex justify-between">
                      <h2 className="text-2xl font-bold">View Default Prompt</h2>
                      <button onClick={closePopup} className="absolute top-2 right-4 text-3xl">&times;</button>
                    </div>
                    <p>This is the main body of the prompt that will be fed into the LLM. Please contact the backend team if you wish to change the content of the main prompt (not advisable).</p>

                    {/* Prompt Text */}
                    <div className="mt-4 border rounded-lg p-6">
                      <p className="text-lg">
                        The push must contain the more content of the show, it is fine to have the push being long. 
                        Exaggerate and be a clickbait in the push!
                      </p> 
                      <br></br>
                      <p className="text-lg"> 
                        If there are any extra requirements by the user, 
                        you must fulfill them while keeping the push interesting. All input data may be None; use those 
                        that are not None and choose which ones to use by yourself. Aim to generate the best clickbait 
                        {`{type_of_push_notification}`} notification.
                      </p>
                      <br></br>
                      <p className="text-lg">
                        If "Type of Push Notification" is cast-driven, "name_of_cast" must be included in the push. 
                      </p>
                      <br></br>
                      <p className="text-lg">
                        If "Demographics of the target receiver of the push", please adjust the push according to the 
                        target receiver demographics, which is be more energetic for younger receivers, be more cast-focus 
                        and use more information of the cast when the target receivers are fan on the cast.
                      </p>
                      <br></br>
                      <p className="text-lg">
                        If "Base Push Example" is provided, improve and regenerate a push based on the "Base Push Example".
                      </p>
                      <br></br>
                      <p className="text-lg">
                        If "Local trend in Malaysia" is provided, the trend must be incorporated into the push with any method. 
                      </p>
                      <br></br>
                      <p className="text-lg">
                        If "Include Slangs" is True, please incorporate local slangs in the Bahasa Melayu version. 
                      </p>
                      <br></br>
                      <p className="text-lg">
                        If and only if "Include Emoji" is True, please se emojis. 
                      </p>
                      <br></br>
                      <p className="text-lg">
                        The followings are additional requirements that must be fulfilled when generating the push notification.
                        {`{additional_requirements}`}
                      </p>
                    </div>
                  </div>

                  {/* Background overlay */}
                  <div style={{ position: 'fixed', left: 0, top: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 999 }}></div>
                </>
              )}

              <textarea
                placeholder="Enter additional information here..."
                value={settings.addRequirements}
                onChange={handleAddRequirementsChange}
                className="mt-1 block w-full h-60 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-[#F5B919] focus:border-[#F5B919] p-2"
              />
            </div>

            {/* Generate Button */}
            <div className="flex justify-center mb-4">
              {settings.returnToGeneration && (
                  <button 
                      className="bg-[#F5B919] w-full text-3xl text-black font-bold py-3 px-6 rounded-lg shadow-md hover:bg-yellow-600 transition duration-300" 
                      onClick={handleReturnToGeneration}
                  >
                      Return to Generation
                  </button>
              )}
              <div className="w-full pl-2">
                <button className={`bg-[#F5B919] w-full text-3xl text-black font-bold py-3 px-6 rounded-lg shadow-md hover:bg-yellow-600 transition duration-300 ${isFormEnabled ? '' : 'cursor-not-allowed opacity-50'}`} disabled={!isFormEnabled} onClick={handleGenPush} >
                  Generate
                </button>
              </div>
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
            {settings.showTrends && (
                <button 
                    onClick={handleRefreshTrends} 
                    className="bg-green-500 text-white text-sm md:text-xs font-bold py-2 px-4 rounded-full hover:bg-green-600 transition duration-300"
                >
                    {settings.promotionType === 'cast-driven' 
                        ? 'Generate Cast-Specific Trends' 
                        : 'Generate Content-Specific Trends'}
                </button>
            )}
          </div>
          <div className="w-4/5 mx-auto bg-white flex flex-col rounded-lg shadow-md mt-4 overflow-y-auto" style={{ minHeight: 'fit-content', maxHeight: '700px',  padding: '16px' }}>
            {!settings.showTrends ? (
              <button className={`bg-[#F5B919] text-black font-bold py-2 px-4 hover:bg-yellow-600 rounded-full cursor-not-allowed" ${!settings.showTrends ? '' : 'cursor-not-allowed opacity-50'}`} disabled={settings.showTrends} onClick={handleGenerateTrends} >
                Generate General Trends
              </button>
            ) : (
              <div className="flex flex-col w-full">
                {settings.trendTitles.map((title, index) => (
                  <TrendComponent 
                    key={index} 
                    title={title} 
                    trendClass={settings.trendClassifier[index]} 
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
