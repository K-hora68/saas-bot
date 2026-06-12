import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './Pages/HomePage'
import Register from './Pages/Register'
import Login from './Pages/Login'
import Dashboard from './Pages/Dashboard'

const App = () => {
  return (

        <Routes>
          <Route path='/' element={<HomePage/>}/>
          <Route path='/register' element={<Register/>}/>
          <Route path='/login' element={<Login/>}/> 
          <Route path='/dashboard' element={<Dashboard/>}/>
        </Routes>
  )
}

export default App;
