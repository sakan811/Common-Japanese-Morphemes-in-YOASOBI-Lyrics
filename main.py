import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from morphemes_extractor.data_extractor import get_morphemes_from_songs
from morphemes_extractor.db_func import save_to_db
from morphemes_extractor.json_utils import find_json_files
from morphemes_extractor.logger_config import setup_logger
from visualize import (
    load_morpheme_table,
    plot_morpheme_song_heatmap,
    plot_pos_distribution,
    plot_top_morphemes,
    setup_visualization,
)

# Set up logger
logger: logging.Logger = setup_logger(__name__, logging.WARNING)

app = FastAPI()


class MainRequest(BaseModel):
    json_dir: str | None = None


def get_db_url() -> str:
    """
    Construct the database URL from environment variables.
    """
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "6000")
    db_name = os.getenv("DB_NAME", "postgres")
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


@app.post("/extract-morphemes/")
def extract_morphemes_api(request: MainRequest):
    """
    Extract morphemes from JSON files and save to database.
    """
    db_url = get_db_url()
    json_dir = request.json_dir or os.getenv("JSON_DIR")
    if not json_dir:
        logger.error("JSON_DIR not provided.")
        raise HTTPException(status_code=400, detail="JSON_DIR must be provided.")

    json_file_path_list = find_json_files(json_dir)
    if not json_file_path_list:
        logger.warning("No JSON files found in the specified directory.")
        raise HTTPException(
            status_code=404, detail="No JSON files found in the specified directory."
        )

    df = get_morphemes_from_songs(json_file_path_list)
    if df.empty:
        logger.warning("No morphemes found in the JSON files.")
        raise HTTPException(
            status_code=404, detail="No morphemes found in the JSON files."
        )

    save_to_db(df, db_url)
    return {
        "message": "Morphemes extracted and saved to database.",
        "rows_saved": len(df),
    }


@app.post("/visualize/")
def make_visualizations(font_scale: float = 2.0):
    """
    Generate and save visualizations from morpheme data in the database.
    Returns a JSON response with the output file paths.
    """
    font_sizes = setup_visualization(font_scale)
    db_url = get_db_url()
    df = load_morpheme_table(db_url)
    logger.info(f"Generating visualizations with font scale: {font_scale}...")
    plot_top_morphemes(df, font_sizes)
    plot_pos_distribution(df, font_sizes)
    plot_morpheme_song_heatmap(df, font_sizes_or_top_n=font_sizes)
    logger.info(
        "✅ Plots saved successfully:\n"
        "  - visual_output/top_morphemes.png\n"
        "  - visual_output/pos_distribution.png\n"
        "  - visual_output/morpheme_song_heatmap.png"
    )
    return {
        "message": "Plots saved successfully.",
        "output_files": [
            "visual_output/top_morphemes.png",
            "visual_output/pos_distribution.png",
            "visual_output/morpheme_song_heatmap.png",
        ],
    }
