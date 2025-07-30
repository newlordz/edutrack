import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log environment information
logger.info(f"Python version: {sys.version}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Environment variables: DATABASE_URL={os.environ.get('DATABASE_URL', 'Not set')}")

try:
    logger.info("Attempting to import app...")
    from app import app
    logger.info("✓ App imported successfully")
    
    # Test database connection
    try:
        with app.app_context():
            from sqlalchemy import text
            from database import db
            db.session.execute(text('SELECT 1'))
            logger.info("✓ Database connection successful")
    except Exception as db_error:
        logger.error(f"✗ Database connection failed: {db_error}")
        # Continue anyway - the app might still work
        
except Exception as e:
    logger.error(f"✗ App import failed: {e}")
    logger.error(f"Error type: {type(e).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    sys.exit(1)

# Vercel handler
handler = app

# Test the app
if __name__ == "__main__":
    try:
        logger.info("Starting Flask development server...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"Error running app: {e}")
        sys.exit(1)
