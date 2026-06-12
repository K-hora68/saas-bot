import React from 'react'
import { Link } from 'react-router-dom';
import { Navigate } from 'react-router-dom';

const HomePage = () => {
    useEffect(() => {

     const token = localStorage.getItem("token");
        if (token) {
            navigate("/dashboard"); // Redirect to dashboard if token exists
        }
    }, [])
  return (
    <>
        <h1>Welcome to the Home Page</h1>
        <Link to="/register"><button>Register</button></Link>
    </>
  )
}

export default HomePage;