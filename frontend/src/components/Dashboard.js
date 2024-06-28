import React, { useState } from 'react';
import axios from 'axios';

function Dashboard() {
    const [dateRange, setDateRange] = useState({ start: '', end: '' });
    const [initialCapital, setInitialCapital] = useState('');
    const [backtestResults, setBacktestResults] = useState(null);

    const handleBacktest = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/backtest', {
                start_date: dateRange.start,
                end_date: dateRange.end,
                initial_capital: initialCapital
            });
            alert(response.data.message);
            setBacktestResults(response.data);
        } catch (error) {
            console.error("Error executing backtest:", error);
            alert(error.response? error.response.data.error : 'An error occurred');
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="max-w-4xl w-full bg-white shadow-md rounded-lg p-8">
                <h2 className="text-2xl font-bold mb-6 text-center">Run Backtest</h2>
                <form onSubmit={handleBacktest} className="mb-6">
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <input
                            type="date"
                            value={dateRange.start}
                            onChange={(e) => setDateRange({...dateRange, start: e.target.value })}
                            placeholder="Start Date"
                            className="w-full px-3 py-2 border rounded-lg"
                            required
                        />
                        <input
                            type="date"
                            value={dateRange.end}
                            onChange={(e) => setDateRange({...dateRange, end: e.target.value })}
                            placeholder="End Date"
                            className="w-full px-3 py-2 border rounded-lg"
                            required
                        />
                        <input
                            type="number"
                            value={initialCapital}
                            onChange={(e) => setInitialCapital(e.target.value)}
                            placeholder="Initial Capital"
                            className="w-full px-3 py-2 border rounded-lg my-4"
                            required
                        />
                    </div>
                    <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 mt-4">
                        Run Backtest
                    </button>
                </form>
                {backtestResults && (
                    <div className="mt-8">
                        <h3 className="text-xl font-bold mb-4">Backtest Results</h3>
                        <p>Final Portfolio Value: {backtestResults.final_portfolio_value}</p>
                        <p>Final Return: {backtestResults.final_return}</p>
                        <p>Number of Trades: {backtestResults.num_trades}</p>
                        <p>Winning Trades: {backtestResults.winning_trades}</p>
                        <p>Losing Trades: {backtestResults.losing_trades}</p>
                        <p>Max Drawdown: {backtestResults.max_drawdown}</p>
                        <p>Sharpe Ratio: {backtestResults.sharpe_ratio}</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Dashboard;