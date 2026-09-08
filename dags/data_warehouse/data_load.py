from datetime import date, timedelta
import logging
import json

logger = logging.getLogger(__name__)

def load_data():
    file_path = f'./data/youtube_data_{date.today()}.json'
    try:
        logger.info(f"Processing load file :{file_path}")
        with open(file_path, "r", encoding="utf-8") as raw_data:
            data = json.load(raw_data)
        return data
    except FileNotFoundError as e:
        logger.error(f"Error load file :{file_path}")
        raise e
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file: {file_path}")
        raise e