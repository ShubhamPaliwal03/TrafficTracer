# TrafficTracer 📦🔍
A web application for botnet detection using Machine Learning - XGBoost, from the csv file containing network packet flows, captured using CICFlowMeter Tool.

**TrafficTracer** allows users to upload CSV files containing extracted network flow data and instantly receive detection results indicating whether the traffic is normal or part of a botnet. The system processes the uploaded file, runs it through a pre-trained machine learning model, and visualizes the output using intuitive charts and tables for easy interpretation.

To assist users in generating flow-based CSV files, a downloadable `.jar` file of **CICFlowMeter** is also provided along with usage instructions, enabling users to perform local packet capture and feature extraction before uploading to the web app.

---

### Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Backend:** FastAPI (Python), XGBoost model
- **Deployment:** Vercel (Frontend), Render.com (Backend API)

---

This app is designed for simplicity and quick analysis, making botnet detection accessible to users without deep technical expertise.
