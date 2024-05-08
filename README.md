# BuildSmart-Toolkit

Welcome to the BuildSmart-Toolkit

## Getting Started

These instructions will assist you in running this code on your local machine.

### Prerequisites

Before running the project, make sure you have Python and Node.js installed on your system. You can download them from:

- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/)

### Installing

Follow these steps to set up the backend and frontend of BuildSmart-Toolkit.

#### Backend Setup

Navigate to the backend directory and start the server:

- cd ./backend
python app.py  # or use python3 if python is not configured as Python 3

- If you encounter any missing dependencies, install them using pip:
pip install <package-name>  # or use pip3 if pip is not configured for Python 3

Example CSV files for testing can be found in './backend/uploads'

To set up ChatGPT API key, please perform these steps:

- If on a Unix-based system: export OPENAI_API_KEY='your_api_key'
- If on a Windows system: set OPENAI_API_KEY=your_api_key
If you prefer not to set environment variables: go into './backend/app.py' and set openai.api_key = 'your_api_key'

#### Frontend Setup

Navigate to the frontend directory and start the app:

- cd ./frontend/buildsmart-toolkit
- npm install  # Installs necessary packages
npm start    # Starts the app

