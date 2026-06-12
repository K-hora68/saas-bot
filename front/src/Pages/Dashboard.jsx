import React from "react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
          return;
        }

        const res = await fetch("http://localhost:5000/is_authenticated", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) {
          navigate("/login");
        }
      } catch (err) {
        navigate("/login");
      }
    };
    checkAuth();
  }, [navigate]);
  return (
    <div>
      <h1>Welcome {localStorage.getItem("username")}</h1>
    </div>
  );
};

export default Dashboard;
