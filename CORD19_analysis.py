"""
CORD-19 Basic Analysis Script
Loads metadata.csv, cleans it, and creates figures.
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os

DATA_PATH = "metadata.csv"
OUT_DIR = "."

def load_data(path):
    return pd.read_csv(path)

def basic_explore(df):
    print("Shape:", df.shape)
    print("\nColumns and dtypes:\n", df.dtypes)
    print("\nMissing values per column:\n", df.isnull().sum())

def clean_data(df):
    df = df.copy()
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    df['journal'] = df['journal'].fillna("Unknown")
    df['source_x'] = df['source_x'].fillna("unknown")
    df['abstract'] = df['abstract'].astype(str)
    df['abstract_word_count'] = df['abstract'].apply(lambda x: len(x.split()))
    df['title'] = df['title'].astype(str)
    df['title_word_count'] = df['title'].apply(lambda x: len(x.split()))
    return df

def plot_publications_by_year(df, outpath):
    year_counts = df['year'].value_counts().sort_index()
    fig, ax = plt.subplots()
    year_counts.plot(kind='bar', ax=ax)
    ax.set_title("Publications by Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)

def plot_top_journals(df, outpath, top_n=10):
    top = df['journal'].value_counts().head(top_n)
    fig, ax = plt.subplots()
    top.sort_values().plot(kind='barh', ax=ax)
    ax.set_title(f"Top {top_n} Journals")
    ax.set_xlabel("Count")
    fig.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)

def top_title_words(df, outpath, top_n=20):
    words = []
    for t in df['title']:
        for w in t.lower().split():
            w = ''.join(ch for ch in w if ch.isalpha())
            if len(w) > 2:
                words.append(w)
    counts = Counter(words)
    most = counts.most_common(top_n)
    labels = [w for w, c in most][::-1]
    vals = [c for w, c in most][::-1]
    fig, ax = plt.subplots()
    ax.barh(labels, vals)
    ax.set_title("Top title words")
    fig.tight_layout()
    fig.savefig(outpath)
    plt.close(fig)

def main():
    df = load_data(DATA_PATH)
    basic_explore(df)
    dfc = clean_data(df)
    dfc.to_csv(os.path.join("data", "metadata_cleaned.csv"), index=False)
    plot_publications_by_year(dfc, os.path.join("figures", "pubs_by_year.png"))
    plot_top_journals(dfc, os.path.join("figures", "top_journals.png"))
    top_title_words(dfc, os.path.join("figures", "top_title_words.png"))

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    os.makedirs("figures", exist_ok=True)
    main()
