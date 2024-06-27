import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from 'chart.js/auto';

function Dashboard() {
    const [scenes, setScenes] = useState([]);
    const [dateRange, setDateRange] = useState({ start: '', end: '' });
    const [indicator, setIndicator] = useState('');
    const [params, setParams] = useState('');
    const [backtestResults, setBacktestResults] = useState(null);

    useEffect(() => {
        const fetchScenes = async () => {
            const token = localStorage.getItem('token');
            try {
                const response = await axios.get('http://localhost:5000/scenes', { headers: { Authorization: `Bearer ${token}` } });
                setScenes(response.data);
            } catch (error) {
                console.error("Error fetching scenes:", error);
            }
            const response = await axios.get('http://localhost:5000/scenes', { headers: { Authorization: `Bearer ${token}` } });
            setScenes(response.data);
        };

        fetchScenes();
    }, []);

    const handleBacktest = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post('http://localhost:5000/scenes', { date_range: dateRange, indicator, params: JSON.parse(params) }, { headers: { Authorization: `Bearer ${token}` } });
            alert(response.data.message);
            setScenes([...scenes, response.data.scene]);
        } catch (error) {
            console.error("Error executing backtest:", error);
            alert(error.response ? error.response.data.error : 'An error occurred');
        }
    };

    const handleRunBacktest = async (sceneId) => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`http://localhost:5000/backtest/${sceneId}`, {}, { headers: { Authorization: `Bearer ${token}` } });
            setBacktestResults(response.data);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        if (backtestResults && backtestResults.chartData) {
            const ctx = document.getElementById('backtestChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: backtestResults.chartData.dates,
                    datasets: [
                        {
                            label: 'Close Price',
                            data: backtestResults.chartData.closePrices,
                            borderColor: 'blue',
                            fill: false,
                        },
                        {
                            label: '20-Day SMA',
                            data: backtestResults.chartData.sma20,
                            borderColor: 'orange',
                            fill: false,
                        },
                        {
                            label: 'MACD',
                            data: backtestResults.chartData.macd,
                            borderColor: 'red',
                            fill: false,
                        },
                        {
                            label: 'Signal Line',
                            data: backtestResults.chartData.signalLine,
                            borderColor: 'green',
                            fill: false,
                        },
                    ],
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day',
                            },
                        },
                    },
                },
            });
        }
    }, [backtestResults]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100" style={{
            background: "linear-gradient(90deg, rgba(131, 126, 226, 1) 24%, rgba(114, 114, 226, 1) 58%, rgba(0, 212, 255, 1) 100%)"
          }}>
            <div className="max-w-4xl w-full bg-white shadow-md rounded-lg p-8">
                <h2 className="text-2xl font-bold mb-6 text-center">Create Scene and Run Backtest</h2>
                <form onSubmit={handleCreateScene} className="mb-6">
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <input
                            type="date"
                            value={dateRange.start}
                            onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                            placeholder="Start Date"
                            className="w-full px-3 py-2 border rounded-lg"
                            required
                        />
                        <input
                            type="date"
                            value={dateRange.end}
                            onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
                            placeholder="End Date"
                            className="w-full px-3 py-2 border rounded-lg"
                            required
                        />
                    </div>
                    <input
                        type="text"
                        value={indicator}
                        onChange={(e) => setIndicator(e.target.value)}
                        placeholder="Indicator"
                        className="w-full px-3 py-2 border rounded-lg my-4"
                        required
                    />
                    <input
                        type="text"
                        value={params}
                        onChange={(e) => setParams(e.target.value)}
                        placeholder="Parameters (JSON)"
                        className="w-full px-3 py-2 border rounded-lg"
                        required
                    />
                    <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 mt-4">
                        Run Backtest
                    </button>
                </form>
                <div>
                    <h3 className="text-xl font-bold mb-4">Scenes</h3>
                    <ul className="space-y-4">
                        {scenes.map(scene => (
                            <li key={scene.id} className="p-4 border rounded-lg bg-gray-50">
                                <p>Date Range: {scene.date_range.start} to {scene.date_range.end}</p>
                                <p>Indicator: {scene.indicator}</p>
                                <p>Parameters: {JSON.stringify(scene.params)}</p>
                                <button onClick={() => handleRunBacktest(scene.id)} className="mt-4 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600">
                                    Run Backtest
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>
                {backtestResults && (
                    <div className="mt-8">
                        <h3 className="text-xl font-bold mb-4">Backtest Metrics</h3>
                        <p>Return: {backtestResults.return}</p>
                        <p>Number of Trades: {backtestResults.numTrades}</p>
                        <p>Winning Trades: {backtestResults.winningTrades}</p>
                        <p>Losing Trades: {backtestResults.losingTrades}</p>
                        <p>Max Drawdown: {backtestResults.maxDrawdown}</p>
                        <p>Sharpe Ratio: {backtestResults.sharpeRatio}</p>
                        <canvas id="backtestChart" className="mt-6"></canvas>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Dashboard;
