// src/App.js

import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState('');

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleGenerateButtonClick = async () => {
    try {
      const response = await fetch('http://localhost:5522/prompt_return_endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: inputText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data.result);
    } catch (error) {
      console.error('API Request Error:', error); // Log the error to the console
      setResult('Error occurred. Please check the console for details.');
    }
  };

  return (
    <div className="container">
      <h1>Generate Prompt</h1>
      <label>
        Input Text:
        <input type="text" value={inputText} onChange={handleInputChange} />
      </label>
      <button onClick={handleGenerateButtonClick}>Generate</button>
      <div className="result">
        <h2>Result:</h2>
        <pre>{result}</pre>
      </div>
    </div>
  );
};

export default App;
