import React from 'react'
import { Link, useNavigate } from 'react-router-dom';

import { useEffect } from 'react';

const HomePage = () => {
    const navigate = useNavigate()
    useEffect(() => {
  
     const token = localStorage.getItem("token");
        if (token) {
            navigate("/dashboard"); // Redirect to dashboard if token exists
        }
    }, [])
  return (
    <>
        <h1>Welcome to the Home Page</h1>
        <button onClick={() =>navigate('/login')}>Get Started</button>
    </>
  )
}

export default HomePage;