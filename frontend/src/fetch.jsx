import React, { useState, useEffect } from 'react';
import Header from './pages/Header';
// hi
const backendUrl = process.env.REACT_APP_BACKEND_URL


export const TestPage = () => {

  const [message, setMessage] = useState('');

  const handleGenPush = async () => {
    const inputData = {
      push_type: "cast-driven",
      series_name: "Nothing Uncovered",
      cast_name: "KIM Ha Neul",
      creativity: 0.2,
      demographics: [18, 35],
      isEmojis: true,
      isSlangs: true,
      addRequirements: "",
      selected_trend: "Kimitsu: Kimitsu is a typhoon number 8 hitting Malaysia today",
    };
    console.log("Sending request data:", JSON.stringify(inputData));
    const data = await genPush(inputData);
    setMessage(JSON.stringify(data, null, 2));
  };

  const handleRegenPush = async () => {
    const inputData = {
      basePush: {
        "english": {
          "title": "KIM Ha Neul's Life Turned Upside Down! 🤯",
          "body": "The queen of romantic comedies is now a murder suspect? 🚔️ Don't believe it! Watch Nothing Uncovered to uncover the truth behind the scandal! 💥 #KimHaNeul #NothingUncovered"
        },
        "malay": {
          "title": "Kehidupan KIM Ha Neul Terbalik! 🤯",
          "body": "Ratu komedi romantik kini menjadi suspek pembunuhan? 🚔️ Jangan percayya! Tonton Nothing Uncovered untuk mengungkapkan kebenaran di sebalik skandal! 💥 #KimHaNeul #NothingUncovered"
        }
      },
      addRequirements: "more scary",
    };
    console.log("Sending request data:", JSON.stringify(inputData));
    const data = await regenPush(inputData);
    setMessage(JSON.stringify(data, null, 2));
  };

  const [activeButton, setActiveButton] = useState('audit'); // State for the Active page

  const handleButtonClick = (button) => {
    setActiveButton(button);
  };

  return (
    <div className="h-screen flex flex-col">
      <Header activeButton={activeButton} handleButtonClick={handleButtonClick} />
      <div className='flex flex-col items-center'>
        <h1>Fetched Data</h1>
        <div className='flex'>
          <button className='mr-2' onClick={handleGenPush}>Gen Push</button>
          <button className='ml-2' onClick={handleRegenPush}>Regen Push</button>
        </div>
        <pre>{message}</pre>
      </div>
    </div>
  );
}      


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
// useEffect(() => {
//   const inputData = {
//     push_type: "cast-driven",
//     series_name: "Nothing Uncovered",
//     cast_name: "Kim Ha-Nuel",
//     creativity: 0.2,
//     demographics: [18, 35],
//     isEmojis: true,
//     isSlangs: true,
//     addRequirements: "",
//     selected_trend: "Kimitsu: Kimitsu is a typhoon number 8 hitting Malaysia today",
//   };
//   console.log("Sending request data:", JSON.stringify(inputData));
//   genPush(inputData);
//   }, []);

const regenPush = async (inputData) => {
  const response = await fetch(`${backendUrl}/regenPush`, {
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
// useEffect(() => {
//   const inputData = {
//     basePush: {
//                 "english": 
//                   {"title": "KIM Ha Neul's Life Turned Upside Down! 🤯", 
//                     "body": "The queen of romantic comedies is now a murder suspect? �️️ Don't believe it! Watch Nothing Uncovered to uncover the truth behind the scandal! 💥 #KimHaNeul #NothingUncovered"
//                   }, 
//                 "malay": 
//                   {"title": "Kehidupan KIM Ha Neul Terbalik! 🤯", 
//                     "body": "Ratu komedi romantik kini menjadi suspek pembunuhan? 🚔️ Jangan percayya! Tonton Nothing Uncovered untuk mengungkapkan kebenaran di sebalik skandal! 💥 #KimHaNeul #NothingUncovered"
//                   }
//               },
//     addRequirements: "more scary",
//   };
//   console.log("Sending request data:", JSON.stringify(inputData));
//   regenPush(inputData);
//   }, []);