from simple_salesforce import Salesforce
from typing import Dict, List
from sqlalchemy.orm import Session
from models import Lead
from validators import validate_lead_data
from logger import setup_logger
import os
from dotenv import load_dotenv

load_dotenv()
logger = setup_logger('crm_integration')

class SalesforceIntegration:
    def __init__(self):
        try:
            self.sf = Salesforce(
                username=os.getenv('SALESFORCE_USERNAME'),
                password=os.getenv('SALESFORCE_PASSWORD'),
                security_token=os.getenv('SALESFORCE_SECURITY_TOKEN'),
                domain='login'  # Use 'test' for sandbox environments
            )
            logger.info("Successfully connected to Salesforce")
        except Exception as e:
            logger.error(f"Failed to connect to Salesforce: {str(e)}")
            raise

    def fetch_leads(self, batch_size: int = 100) -> List[Dict]:
        """
        Fetch leads from Salesforce using SOQL query
        """
        try:
            # SOQL query to fetch lead data
            query = """
                SELECT 
                    FirstName, 
                    LastName, 
                    Company, 
                    Email, 
                    Industry, 
                    Status, 
                    Description,
                    City,
                    State,
                    Country
                FROM Lead 
                WHERE Email != NULL
            """
            
            # Execute query
            result = self.sf.query_all(query)
            leads = []

            for record in result['records']:
                lead = {
                    'first_name': record.get('FirstName', ''),
                    'last_name': record.get('LastName', ''),
                    'company_name': record.get('Company', ''),
                    'email': record.get('Email', ''),
                    'industry': record.get('Industry', ''),
                    'lead_stage': record.get('Status', ''),
                    'interests': record.get('Description', ''),
                    'location': f"{record.get('City', '')}, {record.get('State', '')}, {record.get('Country', '')}"
                }
                leads.append(lead)

            logger.info(f"Successfully fetched {len(leads)} leads from Salesforce")
            return leads

        except Exception as e:
            logger.error(f"Error fetching leads from Salesforce: {str(e)}")
            raise

    def create_lead(self, lead_data: Dict) -> bool:
        """
        Create a new lead in Salesforce
        """
        try:
            # Map our data to Salesforce fields
            sf_lead = {
                'FirstName': lead_data.get('first_name'),
                'LastName': lead_data.get('last_name'),
                'Company': lead_data.get('company_name'),
                'Email': lead_data.get('email'),
                'Industry': lead_data.get('industry'),
                'Status': lead_data.get('lead_stage'),
                'Description': lead_data.get('interests'),
            }
            
            # Create lead in Salesforce
            result = self.sf.Lead.create(sf_lead)
            
            if result.get('success'):
                logger.info(f"Successfully created lead in Salesforce: {lead_data['email']}")
                return True
            else:
                logger.error(f"Failed to create lead in Salesforce: {result.get('errors')}")
                return False

        except Exception as e:
            logger.error(f"Error creating lead in Salesforce: {str(e)}")
            return False

def import_leads_from_salesforce(db: Session) -> Dict:
    """
    Main function to import leads from Salesforce to database
    """
    stats = {"processed": 0, "success": 0, "failed": 0}
    
    try:
        # Initialize Salesforce integration
        sf = SalesforceIntegration()
        
        # Fetch leads from Salesforce
        leads = sf.fetch_leads()
        
        # Process each lead
        for lead_data in leads:
            stats["processed"] += 1
            
            # Validate lead data
            is_valid, errors = validate_lead_data(lead_data)
            
            if is_valid:
                try:
                    # Create new lead in database
                    lead = Lead(**lead_data)
                    db.add(lead)
                    db.commit()
                    stats["success"] += 1
                    logger.info(f"Successfully imported lead: {lead_data['email']}")
                except Exception as e:
                    db.rollback()
                    stats["failed"] += 1
                    logger.error(f"Error saving lead {lead_data.get('email')}: {str(e)}")
            else:
                stats["failed"] += 1
                logger.warning(f"Invalid lead data: {errors}")
        
        logger.info(f"Salesforce import completed. Stats: {stats}")
        return stats
    
    except Exception as e:
        logger.error(f"Salesforce import failed: {str(e)}")
        raise

# Example usage in main.py:
"""
from crm_integration import import_leads_from_salesforce

try:
    db = next(get_db())
    stats = import_leads_from_salesforce(db)
    print(f"Import completed. Stats: {stats}")
except Exception as e:
    print(f"Import failed: {str(e)}")
"""