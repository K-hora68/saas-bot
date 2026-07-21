import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/BusinessSetup.css";

const BusinessSetup = () => {
  const [formData, setFormData] = useState({
    business_name: "",
    business_type: "",
    description: "",
    phone: "",
    email: "",
    instance_name: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [business, setBusiness] = useState(null);

  const API_URL = "http://localhost:5000/api/business";

  useEffect(() => {
    fetchBusiness();
  }, []);

  const fetchBusiness = async () => {
    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(API_URL, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setBusiness(response.data);
      setFormData(response.data);
    } catch (err) {
      // Business not found, which is okay for new users
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const token = localStorage.getItem("token");
      const config = { headers: { Authorization: `Bearer ${token}` } };

      let response;
      if (business) {
        // Update existing
        response = await axios.put(
          `${API_URL}/${business.id}`,
          formData,
          config,
        );
        setSuccess("Business updated successfully!");
       
      } else {
        // Create new
        response = await axios.post(API_URL, formData, config);
        setBusiness(response.data.business);
        setSuccess("Business created successfully!");
      }

      setFormData(response.data.business || formData);
    } catch (err) {
      console.log(err.response);
      console.log(err.response?.status);
      console.log(err.response?.data);

      setError(err.response?.data?.message || "Error saving business");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="business-setup-container">
      <div className="business-setup-card">
        <h1>{business ? "Update Business" : "Setup Your Business"}</h1>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <form onSubmit={handleSubmit} className="business-form">
          <div className="form-group">
            <label>Business Name *</label>
            <input
              type="text"
              name="business_name"
              value={formData.business_name}
              onChange={handleChange}
              placeholder="Enter your business name"
              required
              maxLength="50"
            />
          </div>

          <div className="form-group">
            <label>Business Type *</label>
            <select
              name="business_type"
              value={formData.business_type}
              onChange={handleChange}
              required
            >
              <option value="">Select a type</option>
              <option value="Retail">Retail</option>
              <option value="Service">Service</option>
              <option value="Food & Beverage">Food & Beverage</option>
              <option value="Healthcare">Healthcare</option>
              <option value="Education">Education</option>
              <option value="Technology">Technology</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label>Business Description</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Describe your business, services, and unique value proposition"
              maxLength="500"
              rows="4"
            />
            <small>{formData.description.length}/500 characters</small>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Phone Number *</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                placeholder="+1234567890"
                required
                maxLength="15"
              />
            </div>

            <div className="form-group">
              <label>Email *</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="business@example.com"
                required
                maxLength="50"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Evolution API Instance Name *</label>
            <input
              type="text"
              name="instance_name"
              value={formData.instance_name}
              onChange={handleChange}
              placeholder="your_whatsapp_instance"
              required
              maxLength="50"
            />
            <small>The WhatsApp instance name from Evolution API</small>
          </div>

          <button type="submit" disabled={loading} className="btn btn-primary">
            {loading
              ? "Saving..."
              : business
                ? "Update Business"
                : "Create Business"}
          </button>
        </form>

        {business && (
          <div className="business-info">
            <h3>Current Business Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Business Name:</label>
                <span>{business.business_name}</span>
              </div>
              <div className="info-item">
                <label>Type:</label>
                <span>{business.business_type}</span>
              </div>
              <div className="info-item">
                <label>Phone:</label>
                <span>{business.phone}</span>
              </div>
              <div className="info-item">
                <label>Email:</label>
                <span>{business.email}</span>
              </div>
              <div className="info-item">
                <label>Instance:</label>
                <span>{business.instance_name}</span>
              </div>
              <div className="info-item full-width">
                <label>Description:</label>
                <span>{business.description || "No description"}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BusinessSetup;
