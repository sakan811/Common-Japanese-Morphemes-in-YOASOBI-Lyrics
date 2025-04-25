from typing import Optional, Dict, List, Tuple, Any, Union, cast
from dotenv import load_dotenv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sqlalchemy import create_engine
import os
import matplotlib as mpl


# Configure visualization settings
def setup_visualization(font_scale: float = 1.0) -> Dict[str, float]:
    """
    Configure matplotlib settings for better visualization of Japanese text

    Args:
        font_scale: Scale factor for all text sizes (default=1.0)
        
    Returns:
        Dict[str, float]: Dictionary of font sizes for various elements
    """
    # Define standard font sizes
    FONT_SIZES = {
        "title": 14 * font_scale,
        "label": 12 * font_scale,
        "tick": 10 * font_scale,
        "annotation": 9 * font_scale,
        "legend": 10 * font_scale,
    }

    # Use a higher quality figure format and settings
    mpl.rcParams["savefig.dpi"] = 300
    mpl.rcParams["figure.figsize"] = (12, 7)  # Increased figure size for better fitting

    # Set font sizes globally
    plt.rcParams["font.size"] = FONT_SIZES["tick"]
    plt.rcParams["axes.titlesize"] = FONT_SIZES["title"]
    plt.rcParams["axes.labelsize"] = FONT_SIZES["label"]
    plt.rcParams["xtick.labelsize"] = FONT_SIZES["tick"]
    plt.rcParams["ytick.labelsize"] = FONT_SIZES["tick"]
    plt.rcParams["legend.fontsize"] = FONT_SIZES["legend"]

    # Use a cross-platform font that works well with Japanese text
    plt.rcParams["font.family"] = ["Yu Gothic"]

    # Improve spacing automatically
    plt.rcParams["figure.autolayout"] = True

    return FONT_SIZES


# Load DB connection from environment variables (reuse main.py logic)
def get_db_url() -> str:
    """
    Get database connection URL from environment variables
    
    Returns:
        str: PostgreSQL connection URL
    """
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "6000")
    db_name = os.getenv("DB_NAME", "postgres")
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def load_morpheme_table(db_url: str) -> pd.DataFrame:
    """
    Load morpheme data from the database
    
    Args:
        db_url: Database connection string
        
    Returns:
        pd.DataFrame: DataFrame containing morpheme data
    """
    engine = create_engine(db_url)
    with engine.connect() as conn:
        df = pd.read_sql_table("Morpheme", conn)
    return df


def plot_pos_distribution(
    df: pd.DataFrame, font_sizes: Optional[dict[str, float]] = None
) -> None:
    """
    Create a bar chart showing the distribution of parts of speech in the dataset.

    Args:
        df: DataFrame containing the morpheme data with Part_of_Speech column
        font_sizes: Dictionary with font size settings
    """
    # Use default font sizes if none provided
    if font_sizes is None:
        font_sizes = {
            "title": 14,
            "label": 12,
            "tick": 10,
            "annotation": 9,
            "legend": 10,
        }

    # Create figure using global configuration
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot with improved visual settings
    sns.countplot(
        y="Part_of_Speech",
        data=df,
        order=df["Part_of_Speech"].value_counts().index,
        hue="Part_of_Speech",
        palette="mako",
        legend=False,
        ax=ax,
    )

    # Add labels and title with better formatting
    ax.set_title(
        "Distribution of Part of Speech from YOASOBI's songs",
        fontsize=font_sizes["title"],
        fontweight="bold",
    )
    ax.set_xlabel("Count", fontsize=font_sizes["label"])
    ax.set_ylabel("Part of Speech", fontsize=font_sizes["label"])

    # Set tick font sizes
    ax.tick_params(axis="both", which="major", labelsize=font_sizes["tick"])

    # Ensure all text fits
    plt.tight_layout(pad=2.0)

    # Ensure output directory exists
    os.makedirs("visual_output", exist_ok=True)
    plt.savefig(
        os.path.join("visual_output", "pos_distribution.png"), bbox_inches="tight"
    )
    plt.close()


def plot_top_morphemes(
    df: pd.DataFrame, font_sizes: Optional[dict[str, float]] = None, top_n: int = 20
) -> None:
    """
    Create a bar chart showing the most common morphemes in the dataset.

    Args:
        df: DataFrame containing the morpheme data
        font_sizes: Dictionary with font size settings
        top_n: Number of top morphemes to display
    """
    # Use default font sizes if none provided
    if font_sizes is None:
        font_sizes = {
            "title": 14,
            "label": 12,
            "tick": 10,
            "annotation": 9,
            "legend": 10,
        }

    # Create figure using global configuration with adjusted size for proper text display
    fig, ax = plt.subplots(figsize=(14, 10))  # Larger figure for better text display

    # Get top morphemes
    top = df["Morpheme"].value_counts().head(top_n)

    # Create barplot with improved styling (fixed to avoid deprecation warning)
    ax = sns.barplot(
        x=top.values, y=top.index, hue=top.index, palette="viridis", legend=False, ax=ax
    )    # Add value labels to the bars
    for p in ax.patches:
        # Cast patch to Rectangle to make mypy happy
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

    # Add labels and title with better formatting
    ax.set_title(
        f"Top {top_n} Most Common Morphemes from YOASOBI's songs",
        fontsize=font_sizes["title"],
        fontweight="bold",
    )
    ax.set_xlabel("Count", fontsize=font_sizes["label"])
    ax.set_ylabel("Morpheme", fontsize=font_sizes["label"])

    # Set tick font sizes
    ax.tick_params(axis="both", which="major", labelsize=font_sizes["tick"])

    # Add more horizontal space for count labels
    plt.tight_layout(pad=3.0)

    # Ensure output directory exists
    os.makedirs("visual_output", exist_ok=True)
    plt.savefig(os.path.join("visual_output", "top_morphemes.png"), bbox_inches="tight")
    plt.close()


def plot_morpheme_song_heatmap(
    df: pd.DataFrame, 
    font_sizes_or_top_n: Union[Optional[Dict[str, float]], int] = None, 
    top_n_param: int = 10
) -> None:
    """
    Create a heatmap showing the usage frequency of top morphemes across different songs.

    Args:
        df: DataFrame containing the morpheme data
        font_sizes_or_top_n: Dictionary with font size settings or top_n value (optional)
        top_n_param: Number of top morphemes to display (used if font_sizes_or_top_n is a dict)
    """
    # Handle parameters based on type
    if isinstance(font_sizes_or_top_n, dict):
        # First parameter is font_sizes
        font_sizes = font_sizes_or_top_n
        top_n = top_n_param
    elif isinstance(font_sizes_or_top_n, int):
        # First parameter is actually top_n
        top_n = font_sizes_or_top_n
        font_sizes = None
    else:
        # Default case: None was passed
        font_sizes = None
        top_n = top_n_param
    
    # Set default font sizes
    if font_sizes is None:
        font_sizes = {
            "title": 14,
            "label": 12,
            "tick": 10,
            "annotation": 9,
            "legend": 10,
        }

    # Get top morphemes for analysis
    top_morphemes = df["Morpheme"].value_counts().head(top_n).index
    filtered = df[df["Morpheme"].isin(top_morphemes)].copy()    # Ensure Morpheme is a string and 1D (flatten lists/tuples, handle NaN)
    def flatten_morpheme(x: Any) -> str:
        if isinstance(x, (list, tuple)):
            return str(x[0]) if len(x) > 0 else ""
        return str(x) if pd.notnull(x) else ""

    # Clean and prepare data
    filtered["Morpheme"] = filtered["Morpheme"].apply(flatten_morpheme)
    filtered["Song"] = filtered["Song"].astype(str)
    filtered["Count"] = 1  # Add a count column for aggregation

    # Create pivot table for heatmap
    pivot = pd.pivot_table(
        filtered,
        index="Morpheme",
        columns="Song",
        values="Count",
        aggfunc="sum",
        fill_value=0,
    )

    # Create figure using global configuration with expanded size
    plt.figure(figsize=(16, 10))  # Much larger figure to accommodate all labels

    # Create heatmap with improved styling
    sns.heatmap(
        pivot,
        annot=True,
        fmt="d",
        cmap="crest",
        cbar_kws={"label": "Frequency"},
        linewidths=0.5,
        annot_kws={"size": 10},  # Slightly larger annotation text
    )

    # Use font_sizes for title and labels
    plt.title(
        f"Heatmap of Top {top_n} Morphemes Usage by Song from YOASOBI's songs",
        fontsize=font_sizes["title"],
        fontweight="bold",
        pad=20,
    )  # Add padding above title
    plt.xlabel(
        "Song", fontsize=font_sizes["label"], labelpad=10
    )  # Add padding below x-axis label
    plt.ylabel(
        "Morpheme", fontsize=font_sizes["label"], labelpad=10
    )  # Add padding to the right of y-axis label

    # Rotate x-axis labels for better readability with more space
    plt.xticks(rotation=45, ha="right")

    # Adjust the bottom margin to make room for the rotated x labels
    plt.subplots_adjust(bottom=0.25)

    # Ensure output directory exists
    os.makedirs("visual_output", exist_ok=True)
    plt.savefig(
        os.path.join("visual_output", "morpheme_song_heatmap.png"),
        bbox_inches="tight",  # This ensures all elements are included in the saved figure
        pad_inches=0.5,
    )  # Add extra padding around the figure
    plt.close()


def main(font_scale: float = 2.0) -> None:
    """
    Main function to execute all visualization tasks.
    Loads data from database and generates all plots.

    Args:
        font_scale: Scale factor for all text sizes (default=1.0)
    """
    # Set up visualization environment with font scaling
    font_sizes = setup_visualization(font_scale)

    # Load data from database
    db_url = get_db_url()
    df = load_morpheme_table(db_url)    # Generate all visualizations with consistent font settings
    print(f"Generating visualizations with font scale: {font_scale}...")
    plot_top_morphemes(df, font_sizes)
    plot_pos_distribution(df, font_sizes)
    plot_morpheme_song_heatmap(df, font_sizes_or_top_n=font_sizes)

    print(
        "✅ Plots saved successfully:\n"
        "  - visual_output/top_morphemes.png\n"
        "  - visual_output/pos_distribution.png\n"
        "  - visual_output/morpheme_song_heatmap.png"
    )


if __name__ == "__main__":
    load_dotenv()
    main()
