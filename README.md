# ReactPython

A React frontend with Vite and a Python backend using FastAPI for executing Python code.

## Setup

1. Ensure Python virtual environment is set up:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn python-multipart
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open http://localhost:5173 in your browser.

## Usage

- Enter Python code in the input textarea (default: `print('Hello, World!')`)
- Click "Execute" to run the code on the backend
- View the output in the output textarea

The backend executes the code using the Python interpreter in the virtual environment.
