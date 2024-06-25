import React, { useState } from 'react';

function Dashboard() {
    const [dateRange, setDateRange] = useState({ start: '', end: '' });
    const [indicator, setIndicator] = useState('');
    const [params, setParams] = useState('');
    const [scenes, setScenes] = useState([
        // Mock data for display purposes
        { id: 1, date_range: { start: '2024-01-01', end: '2024-01-10' }, indicator: 'Example Indicator', params: { key: 'value' } }
    ]);

    const handleCreateScene = (e) => {
        e.preventDefault();
        // Mock new scene creation
        const newScene = {
            id: scenes.length + 1,
            date_range: { start: dateRange.start, end: dateRange.end },
            indicator,
            params: JSON.parse(params)
        };
        setScenes([...scenes, newScene]);
        alert('Scene created successfully');
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="max-w-4xl w-full bg-white shadow-md rounded-lg p-8">
                <h2 className="text-2xl font-bold mb-6 text-center">Dashboard</h2>
                <form onSubmit={handleCreateScene} className="mb-6">
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <input
                            type="text"
                            value={dateRange.start}
                            onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                            placeholder="Start Date"
                            className="w-full px-3 py-2 border rounded-lg"
                            required
                        />
                        <input
                            type="text"
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
                        Create Scene
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
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
