import React from "react";
import { Link } from "react-router-dom";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!username || !email || !password) {
      alert("Please fill in all fields");
      return;
    }

    const method = "POST";
    const url = "http://localhost:5000/users";
    try {
      const res = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      });
      const data = await res.json();
      if (res.ok) {
        alert("User registered successfully");
        setUsername("");
        setEmail("");
        setPassword("");
        navigate("/login");
      } else {
        alert(data.message || "Registration failed");
      }
    } catch (error) {
      console.error("Error during registration:", error);
      alert("An error occurred during registration. Please try again.");
    }
  };
  return (
    <>
      <h1>Register Page</h1>
      <div className="register-form">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => {
            setUsername(e.target.value);
          }}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
          }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
          }}
        />
        <Link to="/login">
          <button>Already have an account? Login</button>
        </Link>
        <button onClick={handleSubmit}>Register</button>
      </div>
    </>
  );
};

export default Register;
