import logging
from typing import Optional, Dict, Any, Union, cast
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sqlalchemy import create_engine
import os
import matplotlib as mpl
from morphemes_extractor.logger_config import setup_logger

# Set up logger
logger: logging.Logger = setup_logger(__name__, logging.INFO)

# Constants to avoid magic numbers/strings
DEFAULT_FONT_SIZES: Dict[str, float] = {
    "title": 14.0,
    "label": 12.0,
    "tick": 10.0,
    "annotation": 9.0,
    "legend": 10.0,
}
DEFAULT_DB_CONFIG = {
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "6000",
    "name": "postgres",
}


def setup_visualization(font_scale: float = 1.0) -> Dict[str, float]:
    """
    Configures matplotlib for Japanese text and returns font sizes.
    """
    logger.info(f"Setting up visualization environment with font scale: {font_scale}")
    font_sizes = {k: v * font_scale for k, v in DEFAULT_FONT_SIZES.items()}
    mpl.rcParams["savefig.dpi"] = 300
    mpl.rcParams["figure.figsize"] = (12, 7)
    plt.rcParams["font.size"] = font_sizes["tick"]
    plt.rcParams["axes.titlesize"] = font_sizes["title"]
    plt.rcParams["axes.labelsize"] = font_sizes["label"]
    plt.rcParams["xtick.labelsize"] = font_sizes["tick"]
    plt.rcParams["ytick.labelsize"] = font_sizes["tick"]
    plt.rcParams["legend.fontsize"] = font_sizes["legend"]
    plt.rcParams["font.family"] = ["Noto Sans CJK JP"]
    plt.rcParams["figure.autolayout"] = True
    return font_sizes


def get_db_url() -> str:
    """
    Returns PostgreSQL connection URL from environment variables.
    """
    db_user = os.getenv("DB_USER", DEFAULT_DB_CONFIG["user"])
    db_password = os.getenv("DB_PASSWORD", DEFAULT_DB_CONFIG["password"])
    db_host = os.getenv("DB_HOST", DEFAULT_DB_CONFIG["host"])
    db_port = os.getenv("DB_PORT", DEFAULT_DB_CONFIG["port"])
    db_name = os.getenv("DB_NAME", DEFAULT_DB_CONFIG["name"])
    logger.info(f"Connecting to PostgreSQL database: {db_name} on {db_host}:{db_port}")
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def load_morpheme_table(db_url: str) -> pd.DataFrame:
    """
    Loads morpheme data from the database.
    """
    logger.info("Loading morpheme data from database...")
    engine = create_engine(db_url)
    try:
        with engine.connect() as conn:
            df = pd.read_sql_table("Morpheme", conn)
        logger.info(f"Successfully loaded {len(df)} morpheme records from database")
        return df
    except pd.errors.DatabaseError as e:
        logger.error(f"Pandas database error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading data from database: {e}")
        raise


def plot_pos_distribution(
    df: pd.DataFrame, font_sizes: Optional[Dict[str, float]] = None
) -> None:
    """
    Plots the distribution of parts of speech in the dataset.
    """
    logger.info("Creating part of speech distribution chart...")
    if font_sizes is None:
        font_sizes = DEFAULT_FONT_SIZES
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.countplot(
        y="Part_of_Speech",
        data=df,
        order=df["Part_of_Speech"].value_counts().index,
        hue="Part_of_Speech",
        palette="mako",
        legend=False,
        ax=ax,
    )
    ax.set_title(
        "Distribution of Part of Speech from YOASOBI's songs",
        fontsize=font_sizes["title"],
        fontweight="bold",
    )
    ax.set_xlabel("Count", fontsize=font_sizes["label"])
    ax.set_ylabel("Part of Speech", fontsize=font_sizes["label"])
    ax.tick_params(axis="both", which="major", labelsize=font_sizes["tick"])
    plt.tight_layout(pad=2.0)
    os.makedirs("visual_output", exist_ok=True)
    output_path = os.path.join("visual_output", "pos_distribution.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Part of speech distribution chart saved to {output_path}")


def plot_top_morphemes(
    df: pd.DataFrame, font_sizes: Optional[Dict[str, float]] = None, top_n: int = 20
) -> None:
    """
    Plots the most common morphemes in the dataset.
    """
    logger.info(f"Creating chart for top {top_n} morphemes...")
    if font_sizes is None:
        font_sizes = DEFAULT_FONT_SIZES
    fig, ax = plt.subplots(figsize=(14, 10))
    top = df["Morpheme"].value_counts().head(top_n)
    ax = sns.barplot(
        x=top.values, y=top.index, hue=top.index, palette="viridis", legend=False, ax=ax
    )
    for p in ax.patches:
        rect = cast(mpatches.Rectangle, p)
        width = rect.get_width()
        ax.text(
            width + 1,
            rect.get_y() + rect.get_height() / 2,
            f"{int(width)}",
            ha="left",
            va="center",
            fontsize=font_sizes["annotation"],
        )
    ax.set_title(
        f"Top {top_n} Most Common Morphemes from YOASOBI's songs",
        fontsize=font_sizes["title"],
        fontweight="bold",
    )
    ax.set_xlabel("Count", fontsize=font_sizes["label"])
    ax.set_ylabel("Morpheme", fontsize=font_sizes["label"])
    ax.tick_params(axis="both", which="major", labelsize=font_sizes["tick"])
    plt.tight_layout(pad=3.0)
    os.makedirs("visual_output", exist_ok=True)
    output_path = os.path.join("visual_output", "top_morphemes.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    logger.info(f"Top morphemes chart saved to {output_path}")


def plot_morpheme_song_heatmap(
    df: pd.DataFrame,
    font_sizes_or_top_n: Union[Optional[Dict[str, float]], int] = None,
    top_n_param: int = 10,
) -> None:
    """
    Plots a heatmap showing the usage frequency of top morphemes across songs.
    """
    if isinstance(font_sizes_or_top_n, dict):
        font_sizes = font_sizes_or_top_n
        top_n = top_n_param
    elif isinstance(font_sizes_or_top_n, int):
        top_n = font_sizes_or_top_n
        font_sizes = None
    else:
        font_sizes = None
        top_n = top_n_param
    logger.info(f"Creating morpheme-song heatmap for top {top_n} morphemes...")
    if font_sizes is None:
        font_sizes = DEFAULT_FONT_SIZES
    top_morphemes = df["Morpheme"].value_counts().head(top_n).index
    filtered = df[df["Morpheme"].isin(top_morphemes)].copy()

    def flatten_morpheme(x: Any) -> str:
        # Simplified: always return string or empty string, avoid pd.notnull on non-scalars
        if isinstance(x, (list, tuple)) and x:
            return str(x[0])
        if x is None:
            return ""
        return str(x)

    filtered["Morpheme"] = filtered["Morpheme"].apply(flatten_morpheme)
    filtered["Song"] = filtered["Song"].astype(str)
    filtered["Count"] = 1
    pivot = pd.pivot_table(
        filtered,
        index="Morpheme",
        columns="Song",
        values="Count",
        aggfunc="sum",
        fill_value=0,
    )
    plt.figure(figsize=(16, 10))
    sns.heatmap(
        pivot,
        annot=True,
        fmt="d",
        cmap="crest",
        cbar_kws={"label": "Frequency"},
        linewidths=0.5,
        annot_kws={"size": 10},
    )
    plt.title(
        f"Heatmap of Top {top_n} Morphemes Usage by Song from YOASOBI's songs",
        fontsize=font_sizes["title"],
        fontweight="bold",
        pad=20,
    )
    plt.xlabel("Song", fontsize=font_sizes["label"], labelpad=10)
    plt.ylabel("Morpheme", fontsize=font_sizes["label"], labelpad=10)
    plt.xticks(rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.25)
    os.makedirs("visual_output", exist_ok=True)
    output_path = os.path.join("visual_output", "morpheme_song_heatmap.png")
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0.5)
    plt.close()
    logger.info(f"Morpheme-song heatmap saved to {output_path}")
