import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/Dashboard.css";
import "../styles/CatalogueBuilder.css";

const Dashboard = () => {
  const navigate = useNavigate();
  const [business, setBusiness] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        console.log("No token found")
        navigate("/login");
        return;
      }

      try {
        // Fetch business information
        const response = await axios.get("http://localhost:5000/api/business", {
          headers: { Authorization: `Bearer ${token}` },
        });
        console.log("Business response:", response.data);
        setBusiness(response.data);
      } catch (err) {
        // Business not set up yet, that's okay
        console.log("Axios error", err.response?.status, err.response?.data)
        setError("Business not set up yet");
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    navigate("/login");
  };

  const username = localStorage.getItem("username");

  return (
    <div className="dashboard-container">
      <nav className="dashboard-navbar">
        <div className="navbar-brand">
          <h2>Flas Bot</h2>
        </div>
        <div className="navbar-actions">
          <span className="user-name">Hello, {username}</span>
          <button className="btn-logout" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </nav>

      <div className="dashboard-content">
        <div className="welcome-section">
          <h1>Welcome to Your Bot Dashboard</h1>
          <p>Manage your WhatsApp business bot from here</p>
        </div>

        {loading ? (
          <div className="loading">Loading...</div>
        ) : business ? (
          <>
            <div className="business-card">
              <div className="card-header">
                <h2>{business.business_name}</h2>
                <span className="badge">{business.business_type}</span>
              </div>
              <div className="card-body">
                <p className="description">{business.description}</p>
                <div className="info-grid">
                  <div className="info-item">
                    <span className="label">Phone:</span>
                    <span className="value">{business.phone}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">Email:</span>
                    <span className="value">{business.email}</span>
                  </div>
                  <div className="info-item">
                    <span className="label">WhatsApp Instance:</span>
                    <span className="value">{business.instance_name}</span>
                  </div>
                </div>
              </div>
              <button
                className="btn-edit"
                onClick={() => navigate("/business-setup")}
              >
                Edit Business Info
              </button>
            </div>

            <div className="actions-grid">
              <div className="action-card">
                <h3>Build Catalogue</h3>
                <p>Create and manage your products/services</p>
                <button
                  className="btn-action"
                  onClick={() => navigate("/catalogueBuilder")}
                >
                  Go to Catalogue Builder
                </button>
              </div>

              <div className="action-card">
                <h3>Knowledge Base</h3>
                <p>Add FAQ and knowledge base for your bot</p>
                <button className="btn-action btn-disabled" disabled>
                  Coming Soon
                </button>
              </div>

              <div className="action-card">
                <h3>Messages</h3>
                <p>View incoming and outgoing messages</p>
                <button className="btn-action btn-disabled" disabled>
                  Coming Soon
                </button>
              </div>

              <div className="action-card">
                <h3>Analytics</h3>
                <p>View bot performance and statistics</p>
                <button className="btn-action btn-disabled" disabled>
                  Coming Soon
                </button>
              </div>
            </div>
          </>
        ) : (
          <div className="no-business">
            <h2>No Business Set Up Yet</h2>
            <p>
              Let's get started! Create your business profile to begin using the
              bot.
            </p>
            <button
              className="btn-primary-large"
              onClick={() => navigate("/business-setup")}
            >
              Set Up Your Business
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
