# ReactPython

A React frontend with Vite and a Python backend using FastAPI for executing Python code with AWS OpenSearch integration.

## System Dependencies

Install required system packages:

```bash
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev nodejs npm curl git
```

## Python Setup with pyenv

1. Install pyenv:
   ```bash
   curl https://pyenv.run | bash
   ```

2. Add pyenv to your shell (add these lines to your `~/.bashrc` or `~/.zshrc`):
   ```bash
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init --path)"
   eval "$(pyenv init -)"
   ```

3. Restart your shell or source your rc file:
   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

4. Install Python 3.13.11:
   ```bash
   pyenv install 3.13.11
   ```

5. Set local Python version (the `.python-version` file will be used):
   ```bash
   pyenv local 3.13.11
   ```

6. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Frontend Setup

Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   source ../venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open http://localhost:5173 in your browser.

## Usage

- Enter Python code in the input textarea (default: OpenSearch query example)
- Click "Execute" to run the code on the backend
- View the output in the output textarea

The backend executes the code using the Python interpreter in the virtual environment with access to AWS services (boto3, OpenSearch).
