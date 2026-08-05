# TerraScore (Agri-Scan JP)

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

TerraScore is a full-stack agri-tech web application that visualizes the agricultural potential of any location in Japan. By fetching historical weather data via the Open-Meteo API and evaluating it against specific crop criteria (such as optimal temperatures, required precipitation, and sunshine hours), the system calculates a suitability score (0-100%) for various agricultural styles like rice paddies, orchards, and dairy farming.

## Features

- **Interactive Map (Leaflet):** Click anywhere on the map to select a specific location and fetch real-world climate data instantly.
- **Data-Driven Scoring:** Calculates suitability scores dynamically using Pandas based on annual precipitation, sunshine hours, temperature extremes, and wind gusts.
- **Modern Dashboard UI:** Built with React, Tailwind CSS, and shadcn/ui components for a clean, responsive, and professional user experience.
- **Extensible Crop Criteria:** easily add new crops or environmental requirements using a dictionary-based configuration (`crop_criteria.py`).

## Tech Stack

### Frontend

- **Framework:** React 18 (Vite)
- **Language:** TypeScript
- **Styling:** Tailwind CSS, shadcn/ui
- **Map Integration:** React-Leaflet
- **HTTP Client:** Fetch API

### Backend

- **Framework:** Python 3, Django, Django REST Framework (DRF)
- **Data Processing:** Pandas, NumPy
- **API Integration:** Open-Meteo Archive API (Historical Weather Data)
- **Database:** SQLite (default for development)
