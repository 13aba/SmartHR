from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from service import *
import os

app = FastAPI(title="Resume Extractor Service")

from config import candidate_config
os.makedirs(candidate_config.UPLOAD_DIR, exist_ok=True)

@app.post("/extract_resume")
async def extract_resume(file: UploadFile = File(...)):
    try:
        # Save file
        file_name = await save_cv_candidate(file)

        # Read CV content
        cv_content = read_cv_candidate(file_name)

        # Analyse with LLM
        analysis = analyse_candidate(cv_content)

        return JSONResponse(
            content={
                "filename": file_name,
                "analysis": analysis,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/extract_job")
async def extract_resume(file: UploadFile = File(...)):
    try:
        # Save file
        file_name = await save_job_listing(file)

        # Read job listing
        job_content = read_job_listing(file_name)

        # Analyse with LLM
        analysis = analyse_job(job_content)

        return JSONResponse(
            content={
                "filename": file_name,
                "analysis": analysis,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))