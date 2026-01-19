# backend/main.py

import uvicorn
from fastapi import FastAPI, Request
from config import HOST, PORT
from routers import jobs, resumes, interview, evaluate
from logger import logger

app = FastAPI(title="Recruiter AI Backend")

# --- MIDDLEWARE (The Magic Part) ---
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    # 1. Log the incoming request
    logger.info(f"RECEIVED: {request.method} {request.url.path}")
    
    # 2. Process the request
    try:
        response = await call_next(request)
        
        # 3. Log the response status
        logger.info(f"SENT: Status {response.status_code}")
        return response
    except Exception as e:
        # 4. Log Crashes
        logger.error(f"CRITICAL ERROR: {str(e)}")
        raise e

# Include Routers
app.include_router(jobs.router)
app.include_router(resumes.router)
app.include_router(interview.router)
app.include_router(evaluate.router)

if __name__ == "__main__":
    logger.info("System Starting up...")
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)