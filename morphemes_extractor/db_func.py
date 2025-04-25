import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from morphemes_extractor.logger_config import setup_logger

# Set up logger
logger: logging.Logger = setup_logger(__name__)


def save_to_db(df: pd.DataFrame, db_url: str) -> None:
    """
    Save a DataFrame to a database using SQLAlchemy.
    :param df: DataFrame containing the morpheme data to be saved
    :param db_url: SQLAlchemy database URL
    :return: None
    This function connects to a database specified by db_url and appends
    the data from the provided DataFrame to a table named 'Morpheme'. If the
    table doesn't exist, it will be created.
    """
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            df.to_sql("Morpheme", conn, if_exists="replace", index=False)
            conn.commit()
        logger.info("DataFrame saved to database")
    except OperationalError as e:
        logger.error(f"OperationalError saving DataFrame to database: {e}")
        raise
    except SQLAlchemyError as e:
        logger.error(f"Error saving DataFrame to database: {e}")
        conn.rollback()
        raise
    except UnboundLocalError as e:
        logger.error(f"UnboundLocalError saving DataFrame to database: {e}")
        raise
