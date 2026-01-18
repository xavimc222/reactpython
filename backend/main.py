from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExecuteRequest(BaseModel):
    code: str

@app.post("/execute")
async def execute_code(request: ExecuteRequest):
    try:
        # Path to Python in venv
        python_path = os.path.join(os.path.dirname(__file__), "..", "venv", "bin", "python")

        # Execute the code
        result = subprocess.run(
            [python_path, "-c", request.code],
            capture_output=True,
            text=True,
            timeout=10,  # 10 second timeout
            cwd=os.path.dirname(__file__)  # Run in backend directory
        )

        output = result.stdout + result.stderr
        return {"output": output}

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Code execution timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
