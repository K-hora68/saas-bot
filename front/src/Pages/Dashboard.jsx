import React, { useEffect } from "react";
import { href, useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
        return;
      }

      try {
        const res = await fetch("http://localhost:5000/is_authenticated", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await res.json();
        console.log("Response:", data);
        console.log("Status:", data);

        if (!res.ok) {
          navigate("/login");
        }
      } catch (error) {
        console.error(error);
        navigate("/login");
      }
    };

    checkAuth();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    navigate("/login");
  };

  return (
    <>
      <div>
        <h1>Welcome {localStorage.getItem("username")}</h1>
        <button onClick={handleLogout}>Logout</button>
      </div>

      <div className="hero-cnt">
        <h1>Hello Welcome to your dashboard.</h1>
        <button onClick={() => navigate("/CatalogueBuilder")}>
          Continue Building Your Bot
        </button>
      </div>
    </>
  );
};

export default Dashboard;
