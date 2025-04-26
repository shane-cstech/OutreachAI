from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from datetime import datetime
from database import get_db
from csv_processor import process_csv_file
from logger import setup_logger
# from fastapi.staticfiles import StaticFiles

app = FastAPI()
logger = setup_logger('main')

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(UPLOAD_DIR, f"leads_{timestamp}.csv")
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the CSV file
        db = next(get_db())
        try:
            stats = process_csv_file(file_path, db)
            
            return JSONResponse(content={
                "message": "CSV processed successfully",
                "filename": file.filename,
                "statistics": stats
            })
        finally:
            db.close()
            # Optionally remove the file after processing
            os.remove(file_path)
            
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# # Mount the static directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/")
# async def read_root():
#     return FileResponse('static/index.html')