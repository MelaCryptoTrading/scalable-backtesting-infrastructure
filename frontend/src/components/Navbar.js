import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';

function Navbar() {
  return (
    <nav className="bg-white border-gray-200 dark:border-gray-600 dark:bg-gray-900 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex justify-between space-x-4 px-3 py-2 rounded">
            <Link to="/">
            <img src={logo} alt="Logo" className="h-8" />
            </Link>
            <h1 className='text-white'>Mela</h1>
        </div>
        <div className="space-x-4">
          <Link to="/" className="text-white hover:bg-gray-700 px-3 py-2 rounded">
            Home
          </Link>
          <Link to="/register" className="text-white hover:bg-gray-700 px-3 py-2 rounded">
            Sign Up
          </Link>
          <Link to="/login" className="text-white hover:bg-gray-700 px-3 py-2 rounded">
            Sign In
          </Link>
          <Link to="/dashboard" className="text-white hover:bg-gray-700 px-3 py-2 rounded">
            Dashboard
          </Link>
          <Link to="/index-fund" className="text-white hover:bg-gray-700 px-3 py-2 rounded">
            Index Fund
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
