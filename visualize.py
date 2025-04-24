from dotenv import load_dotenv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
import matplotlib as mpl

# Configure visualization settings
def setup_visualization():
    """Configure matplotlib settings for better visualization of Japanese text"""
    # Use a higher quality figure format and settings
    mpl.rcParams['savefig.dpi'] = 300
    mpl.rcParams['figure.figsize'] = (9, 4.7)  # 1.9:1 ratio
    # Use a cross-platform font that works well with Japanese text
    plt.rcParams['font.family'] = ['Yu Gothic']
    
# Load DB connection from environment variables (reuse main.py logic)
def get_db_url():
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "6000")
    db_name = os.getenv("DB_NAME", "postgres")
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def load_morpheme_table(db_url: str):
    engine = create_engine(db_url)
    with engine.connect() as conn:
        df = pd.read_sql_table("Morpheme", conn)
    return df


def plot_pos_distribution(df: pd.DataFrame):
    """
    Create a bar chart showing the distribution of parts of speech in the dataset.
    
    Args:
        df: DataFrame containing the morpheme data with Part_of_Speech column
    """
    # Create figure using global configuration
    plt.figure()
    
    # Plot with improved visual settings
    sns.countplot(
        y="Part_of_Speech",
        data=df,
        order=df["Part_of_Speech"].value_counts().index,
        hue="Part_of_Speech",
        palette="mako",
        legend=False,
    )
    
    # Add labels and title with better formatting
    plt.title("Distribution of Part of Speech from YOASOBI's songs", fontsize=14, fontweight='bold')
    plt.xlabel("Count", fontsize=12)
    plt.ylabel("Part of Speech", fontsize=12)
    
    # Ensure output directory exists
    os.makedirs("visual_output", exist_ok=True)
    plt.savefig(os.path.join("visual_output", "pos_distribution.png"))
    plt.close()


def plot_top_morphemes(df: pd.DataFrame, top_n: int = 20):
    """
    Create a bar chart showing the most common morphemes in the dataset.
    
    Args:
        df: DataFrame containing the morpheme data
        top_n: Number of top morphemes to display
    """
    # Create figure using global configuration
    plt.figure()
    
    # Get top morphemes
    top = df["Morpheme"].value_counts().head(top_n)
    
    # Create barplot with improved styling
    ax = sns.barplot(x=top.values, y=top.index, palette="viridis")
    
    # Add value labels to the bars
    for p in ax.patches:
        width = p.get_width()
        ax.text(width + 1, p.get_y() + p.get_height()/2, f'{int(width)}', 
                ha='left', va='center', fontsize=9)
    
    # Add labels and title with better formatting
    plt.title(f"Top {top_n} Most Common Morphemes from YOASOBI's songs", fontsize=14, fontweight='bold')
    plt.xlabel("Count", fontsize=12)
    plt.ylabel("Morpheme", fontsize=12)
    
    # Ensure output directory exists
    os.makedirs("visual_output", exist_ok=True)
    plt.savefig(os.path.join("visual_output", "top_morphemes.png"))
    plt.close()


def plot_morpheme_song_heatmap(df: pd.DataFrame, top_n: int = 10):
    """
    Create a heatmap showing the usage frequency of top morphemes across different songs.
    
    Args:
        df: DataFrame containing the morpheme data
        top_n: Number of top morphemes to display
    """
    # Get top morphemes for analysis
    top_morphemes = df["Morpheme"].value_counts().head(top_n).index
    filtered = df[df["Morpheme"].isin(top_morphemes)].copy()
    
    # Ensure Morpheme is a string and 1D (flatten lists/tuples, handle NaN)
    def flatten_morpheme(x):
        if isinstance(x, (list, tuple)):
            return str(x[0]) if len(x) > 0 else ''
        return str(x) if pd.notnull(x) else ''
    
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
    
    # Create figure using global configuration
    plt.figure()
    
    # Create heatmap with improved styling
    sns.heatmap(
        pivot, 
        annot=True, 
        fmt="d", 
        cmap="crest",
        cbar_kws={'label': 'Frequency'},
        linewidths=0.5
    )
    
    # Add labels and title with better formatting
    plt.title(f"Heatmap of Top {top_n} Morphemes Usage by Song from YOASOBI's songs", 
              fontsize=14, fontweight='bold')
    plt.xlabel("Song", fontsize=12)
    plt.ylabel("Morpheme", fontsize=12)
    
    # Rotate x-axis labels for better readability if there are many songs
    plt.xticks(rotation=45, ha='right')
    
    # Ensure output directory exists
    os.makedirs("visual_output", exist_ok=True)
    plt.savefig(os.path.join("visual_output", "morpheme_song_heatmap.png"))
    plt.close()


def main():
    """
    Main function to execute all visualization tasks.
    Loads data from database and generates all plots.
    """
    # Set up visualization environment
    setup_visualization()
    
    # Load data from database
    db_url = get_db_url()
    df = load_morpheme_table(db_url)
    
    # Generate all visualizations
    print("Generating visualizations...")
    plot_top_morphemes(df)
    plot_pos_distribution(df)
    plot_morpheme_song_heatmap(df)
    
    print(
        "✅ Plots saved successfully:\n"
        "  - visual_output/top_morphemes.png\n"
        "  - visual_output/pos_distribution.png\n"
        "  - visual_output/morpheme_song_heatmap.png"
    )


if __name__ == "__main__":
    load_dotenv()
    main()
