from typing import Optional, Dict, Any, Union, cast
from dotenv import load_dotenv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sqlalchemy import create_engine
import os
import matplotlib as mpl
import logging


def setup_logger() -> logging.Logger:
    """
    Returns a configured logger instance for this module.
    """
    logger = logging.getLogger("visualize")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


logger = setup_logger()


def setup_visualization(font_scale: float = 1.0) -> Dict[str, float]:
    """
    Configures matplotlib for Japanese text and returns font sizes.
    """
    logger.info(f"Setting up visualization environment with font scale: {font_scale}")
    FONT_SIZES = {
        "title": 14 * font_scale,
        "label": 12 * font_scale,
        "tick": 10 * font_scale,
        "annotation": 9 * font_scale,
        "legend": 10 * font_scale,
    }
    mpl.rcParams["savefig.dpi"] = 300
    mpl.rcParams["figure.figsize"] = (12, 7)
    plt.rcParams["font.size"] = FONT_SIZES["tick"]
    plt.rcParams["axes.titlesize"] = FONT_SIZES["title"]
    plt.rcParams["axes.labelsize"] = FONT_SIZES["label"]
    plt.rcParams["xtick.labelsize"] = FONT_SIZES["tick"]
    plt.rcParams["ytick.labelsize"] = FONT_SIZES["tick"]
    plt.rcParams["legend.fontsize"] = FONT_SIZES["legend"]
    plt.rcParams["font.family"] = ["Yu Gothic"]
    plt.rcParams["figure.autolayout"] = True
    return FONT_SIZES


def get_db_url() -> str:
    """
    Returns PostgreSQL connection URL from environment variables.
    """
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "6000")
    db_name = os.getenv("DB_NAME", "postgres")
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
    except Exception as e:
        logger.error(f"Error loading data from database: {e}")
        raise


def plot_pos_distribution(
    df: pd.DataFrame, font_sizes: Optional[dict[str, float]] = None
) -> None:
    """
    Plots the distribution of parts of speech in the dataset.
    """
    logger.info("Creating part of speech distribution chart...")
    if font_sizes is None:
        font_sizes = {
            "title": 14,
            "label": 12,
            "tick": 10,
            "annotation": 9,
            "legend": 10,
        }
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
    df: pd.DataFrame, font_sizes: Optional[dict[str, float]] = None, top_n: int = 20
) -> None:
    """
    Plots the most common morphemes in the dataset.
    """
    logger.info(f"Creating chart for top {top_n} morphemes...")
    if font_sizes is None:
        font_sizes = {
            "title": 14,
            "label": 12,
            "tick": 10,
            "annotation": 9,
            "legend": 10,
        }
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
        font_sizes = {
            "title": 14,
            "label": 12,
            "tick": 10,
            "annotation": 9,
            "legend": 10,
        }
    top_morphemes = df["Morpheme"].value_counts().head(top_n).index
    filtered = df[df["Morpheme"].isin(top_morphemes)].copy()

    def flatten_morpheme(x: Any) -> str:
        if isinstance(x, (list, tuple)):
            return str(x[0]) if len(x) > 0 else ""
        return str(x) if pd.notnull(x) else ""

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


def main(font_scale: float = 2.0) -> None:
    """
    Loads data and generates all visualizations.
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


if __name__ == "__main__":
    load_dotenv()
    logger.info("Starting visualization process...")
    main()
    logger.info("Visualization process completed successfully.")
