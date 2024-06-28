import React, { useState, useEffect } from 'react';
import axios from 'axios';


function IndexFund() {
  const [indexFund, setIndexFund] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchIndexFund();
  }, []);

  const fetchIndexFund = async () => {
    try {
      const response = await axios.get('http://localhost:5000/index-fund');
      setIndexFund(response.data);
      setLoading(false);
    } catch (error) {
      setError('Failed to fetch index fund data');
      setLoading(false);
    }
  };

  const handleRecapitalize = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/index-fund/recapitalize');
      setIndexFund(response.data);
      setLoading(false);
    } catch (error) {
      setError('Failed to recapitalize index fund');
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen">{error}</div>;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100" style={{
      background: "linear-gradient(90deg, rgba(131, 126, 226, 1) 24%, rgba(114, 114, 226, 1) 58%, rgba(0, 212, 255, 1) 100%)"
    }}>
      <div className="max-w-4xl w-full bg-white shadow-md rounded-lg p-8" style={{
        background: "linear-gradient(90deg, rgba(131, 126, 226, 1) 24%, rgba(114, 114, 226, 1) 58%, rgba(0, 212, 255, 1) 100%)"
      }}>
        <h2 className="text-2xl font-bold mb-6 text-center">Top 10 Crypto by Market Cap</h2>
        <button
          onClick={handleRecapitalize}
          className="bg-blue-800 text-white py-2 px-4 rounded hover:bg-blue-600 mb-6"
        >
          Recapitalize Fund
        </button>
        <ul className="space-y-4">
          {indexFund.map((coin, index) => (
            <li key={coin.id} className="p-4 border rounded-lg bg-gray-400">
              <p><strong>#{index + 1}</strong> {coin.name} ({coin.symbol})</p>
              <p>Market Cap: ${coin.market_cap.toLocaleString()}</p>
              <p>Price: ${coin.price.toFixed(2)}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default IndexFund;