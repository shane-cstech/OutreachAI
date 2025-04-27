import pandas as pd
from typing import Generator
from sqlalchemy.orm import Session
from models import Lead
from validators import validate_lead_data
from logger import setup_logger
from config import CHUNK_SIZE, REQUIRED_COLUMNS

logger = setup_logger('csv_processor')

def process_csv_file(file_path: str, db: Session) -> dict:
    """Process CSV file and import leads to database"""
    stats = {"processed": 0, "success": 0, "failed": 0}
    
    try:
        # Read CSV in chunks
        for chunk in pd.read_csv(file_path, chunksize=CHUNK_SIZE):
            # Validate columns
            missing_cols = set(REQUIRED_COLUMNS) - set(chunk.columns)
            if missing_cols:
                logger.error(f"Missing required columns: {missing_cols}")
                return stats
            
            # Process each row
            for _, row in chunk.iterrows():
                stats["processed"] += 1
                lead_data = row.to_dict()
                
                # Validate lead data
                is_valid, errors = validate_lead_data(lead_data)
                
                if is_valid:
                    try:
                        lead = Lead(**lead_data)
                        db.add(lead)
                        db.commit()
                        stats["success"] += 1
                    except Exception as e:
                        logger.error(f"Error saving lead: {str(e)}")
                        db.rollback()
                        stats["failed"] += 1
                else:
                    logger.warning(f"Invalid lead data: {errors}")
                    stats["failed"] += 1
                    
        logger.info(f"CSV import completed. Stats: {stats}")
        return stats
    
    except Exception as e:
        logger.error(f"Error processing CSV file: {str(e)}")
        raise