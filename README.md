# Organic Planner Debug

A React frontend with Vite and a Python backend using FastAPI for executing Python code with AWS OpenSearch integration.

## System Dependencies for Linux Debian

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
   # pip install uvicorn; pip install fastapi
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

## In the target machine:

(1) react vite front end server
```
# at /home/ec2-user/code/research/dashboard/frontend
npm run dev
```

(2) python backend server
```
# at /home/ec2-user/code/research/dashboard
source venv/bin/activate
# at /home/ec2-user/code/research/dashboard/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

(3) test aws / opensearch connection
```
# at /home/ec2-user/code/research/dashboard
source venv/bin/activate
python3 test_opensearch.py
```

## start.sh content:

```
# Create webserver dashboard
tmux new-window -t orchestrator -n webserver
tmux send-keys -t orchestrator:webserver "cd ${HOME_DIR}/code/research/dashboard/frontend; npm run dev" C-m

# Create python backend dashboard
tmux new-window -t orchestrator -n backend
tmux send-keys	-t orchestrator:backend	"cd ${HOME_DIR}/code/research/dashboard/; source	venv/bin/activate; cd backend; uvicorn main:app --reload --host 0.0.0.0 --port 8000" C-m

# Create python backend test
tmux new-window -t orchestrator -n backend-test
tmux send-keys -t orchestrator:backend-test "cd ${HOME_DIR}/code/research/dashboard/; source venv/bin/activate; cd backend; python3 test_opensearch.py" C-m
```

# from the localhost machine:
- IP_ADDRESS = "13.204.232.140"
- ssh -i o8-aws/vp-north-worker-arm.pem ec2-user@13.204.232.140 -L 5173:localhost:5173 -L 8000:localhost:8000
- navigate to: "http://localhost:5173"
