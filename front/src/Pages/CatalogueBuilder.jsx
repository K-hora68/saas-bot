import React, { useState } from "react";


const CatalogueBuilder = () => {
  const [services, setServices] = useState([
    {
      name: "",
      description: "",
      price: "",
      image: null
    }
  ]);

  const [active, setActive] = useState(0);

  const syncField = (field, value) => {
    const updated = [...services];
    updated[active][field] = value;
    setServices(updated);
  };

  const addService = () => {
    if (services.length >= 10) return;

    setServices([
      ...services,
      {
        name: "",
        description: "",
        price: "",
        image: null
      }
    ]);

    setActive(services.length);
  };

  const removeService = () => {
    if (services.length === 1) return;

    const updated = services.filter(
      (_, index) => index !== active
    );

    setServices(updated);
    setActive(0);
  };

  const handleImage = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.onload = (event) => {
      const updated = [...services];
      updated[active].image = event.target.result;
      setServices(updated);
    };

    reader.readAsDataURL(file);
  };

  const finishAll = async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await fetch(
        "http://localhost:5000/api/services",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
             "Authorization": `Bearer ${token}`,
          },
          body: JSON.stringify(services)
        }
      );

      const data = await response.json();
      if(!response.ok){
        console.error("Server error:", data)
      return;
      }

      console.log(data);
      
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="shell">
      <div className="sidebar">
        <div className="sidebar-title">
          Services Added
        </div>

        <div id="tabs">
          {services.map((service, index) => (
            <button
              key={index}
              className={`service-tab ${
                active === index ? "active" : ""
              }`}
              onClick={() => setActive(index)}
            >
              <span className="num">
                {index + 1}
              </span>

              <span className="label">
                {service.name || "Unnamed"}
              </span>
            </button>
          ))}
        </div>

        <button
          className="add-btn"
          onClick={addService}
        >
          Add Service
        </button>
      </div>

      <div className="main">
        <h1>Enter Business</h1>

        <input
          type="text"
          placeholder="Service Name"
          value={services[active].name}
          onChange={(e) =>
            syncField("name", e.target.value)
          }
        />

        <textarea
          placeholder="Description"
          value={services[active].description}
          onChange={(e) =>
            syncField(
              "description",
              e.target.value
            )
          }
        />

        <input
          type="number"
          placeholder="Price"
          value={services[active].price}
          onChange={(e) =>
            syncField("price", e.target.value)
          }
        />

        <input
          type="file"
          accept="image/*"
          onChange={handleImage}
        />

        {services[active].image && (
          <img
            src={services[active].image}
            alt="preview"
            style={{
              width: "200px",
              marginTop: "10px"
            }}
          />
        )}

        <div className="actions">
          <button onClick={removeService}>
            Remove
          </button>

          <button onClick={finishAll}>
            Finish
          </button>
        </div>
      </div>
    </div>
  );
};

export default CatalogueBuilder;