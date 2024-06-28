import React from 'react';
import { Link } from 'react-router-dom';
import hero from "../assets/hero.png"

function App() {
 return (
   <div className="w-screen h-screen text-white" style={{
     background: "linear-gradient(90deg, rgba(131, 126, 226, 1) 24%, rgba(114, 114, 226, 1) 58%, rgba(0, 212, 255, 1) 100%)"
   }}>
     <div className="container mx-auto flex px-5 py-24 items-center justify-center">
       <img className="lg:w-2/6 md:w-3/6 w-5/6 mb-10 object-cover object-center" alt="hero" src={hero} />
       <div className="text-center lg:w-5/12 w-full">
         <h1 className="my-4 text-5xl font-bold leading-tight">
           Welcome to Mela Crypto Trading
         </h1>
         <p className="text-2xl mb-8">
            Run backtests on your crypto trading strategies with ease
         </p>
         <div className="flex justify-center mx-auto space-x-4">
            <Link to="/register" className="bg-blue-800 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
              Sign Up
            </Link>
            <Link to="/login" className="bg-gray-400 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-200">
              Sign In
            </Link>
         </div>
       </div>
     </div>
   </div >
 );
}

export default App