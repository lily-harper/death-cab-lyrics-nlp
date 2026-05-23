# Soul Meets Body Meets NLP

```
"Oh come my love and swim with me,
Out in this vast Binary Sea"
- Death Cab for Cutie, Binary Sea
```

**A project by Lily Holmes. Summer 2026**

## Project Overview

> This project uses basic NLP to analyze lyrics and themes in songs from Death Cab for Cutie, The Postal Service, and Benjamin Gibbard's solo work.

Lyrics were collected with the Genius API, cleaned in Python, and analyzed with TF-IDF, truncated SVD components, word counts, and VADER sentiment analysis.

The public dataset in this repository should not include full lyrics. Derived outputs, such as SVD components and sentiment scores, are safer to share than raw or cleaned lyric text.

## Methods

* TF-IDF vectorization
* Truncated SVD for dimensionality reduction and lyric similarity
* VADER lexicon-based sentiment analysis
* Word frequency using basic whitespace tokenization

## Results

Many songs written by Benjamin Gibbard across the three projects I looked at are similar in sentiment and vocabulary.

Work within The Postal Service's album, *Give Up*, is especially lyrically cohesive.

Lyrics across DCFC's discography are predictably more spread out than the other projects with regard to sentiment.

The pipeline produces SVD component datasets for clustering and plotting, plus word-count figures by selected albums.

> Truncated SVD is applied to a TF-IDF matrix to represent songs in lower-dimensional space. Points near each other share similar vocabulary patterns.

## Pipeline

```
Genius API
   |
Raw Lyrics CSV
   |
Cleaning Script
   |
Clean Lyrics Parquet
   |
VADER + TF-IDF + SVD
   |
Processed Parquet Files + Figures
```

## Repository Structure

```
death-cab-lyrics-nlp/
|-- data
|   |-- raw/raw_scrape.csv                 # generated from Genius API
|   |-- clean/clean_lyrics.parquet         # cleaned lyrics, not for public redistribution
|   `-- processed
|       |-- lyrics_clustering.parquet      # VADER + SVD components for clustering
|       `-- lyrics_plotting.parquet        # VADER + 2D SVD components for plotting
|-- docs
|   `-- data_processing_notes.md
|-- reports
|   `-- figures
|       `-- word_counts
|-- src
|   |-- analysis.py
|   |-- albums.py
|   |-- components.py
|   |-- count.py
|   |-- lyric_preprocessing.py
|   |-- paths.py
|   `-- visualizations.py
|-- scripts
|   |-- pull.py
|   |-- clean.py
|   |-- nat_lang.py
|   |-- gen_plots.py
|   `-- pipeline.py
|-- requirements.txt
`-- README.md
```

## Curiosity driven

1. Spotify told me I had listened to **12 hours of Death Cab for Cutie** in one week
2. I wanted to learn some NLP

## Reproducing This Project 

Clone this repository:

```bash
git clone https://github.com/lily-harper/death-cab-lyrics-nlp
cd death-cab-lyrics-nlp
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To pull lyrics from Genius, create a `.env` file with your Genius API token:

```bash
GENIUS_ACCESS_TOKEN=your_token_here
```

Then run:

```bash
PYTHONPATH=. python3 scripts/pull.py
```

This creates the raw data file:

```text
data/raw/raw_scrape.csv
```

After the raw scrape exists, run the local pipeline:

```bash
PYTHONPATH=. python3 scripts/pipeline.py
```

The pipeline:

1. Reads `data/raw/raw_scrape.csv`.
2. Cleans and normalizes the lyric metadata.
3. Saves `data/clean/clean_lyrics.parquet`.
4. Adds VADER sentiment scores.
5. Builds a TF-IDF matrix.
6. Saves SVD components for clustering to `data/processed/lyrics_clustering.parquet`.
7. Saves 2D SVD components for plotting to `data/processed/lyrics_plotting.parquet`.
8. Saves word-count bar charts to `reports/figures/word_counts/`.

Useful options:

```bash
PYTHONPATH=. python3 scripts/pipeline.py --skip-plots
PYTHONPATH=. python3 scripts/pipeline.py --cluster-components 50
PYTHONPATH=. python3 scripts/pipeline.py --raw-data path/to/raw.csv
```

The pipeline uses NLTK resources for stopwords and VADER sentiment. If needed, download them in Python:

```python
import nltk
nltk.download("stopwords")
nltk.download("vader_lexicon")
```

Because the Genius catalog and metadata can change, exact row counts and release-year coverage may vary slightly across runs.

To generate the optional SVD component diagnostic plot:

```bash
PYTHONPATH=. python3 src/components.py
```

## Notes

### On limitations, justifications, and improvements

Limitations:

* Small dataset, about 200 songs after cleaning
* Class imbalance, since most observations are Death Cab for Cutie songs
* Lyrics-only analysis, which ignores sound, instrumentation, production, and other musical context
* Simple models, which are useful for learning but limited in how much context they can understand

### On not infringing copyrights

To respect copyright laws and Death Cab, I avoided including full lyrics in the public version of this project. Included instead are derived values, such as sentiment scores and SVD components.

By running `scripts/pull.py` with your own Genius API token, you can rebuild the raw data locally and then run it through the script-based pipeline.

For current cleaning decisions and data-sharing caveats, see `docs/data_processing_notes.md`.

### On learning and GenAI usage

Still learning. I used resources like YouTube to understand concepts and follow tutorials. **If you have any feedback, please reach out! I would really value more insight.**

I used ChatGPT primarily for code debugging, concept understanding, and learning best practices. All code, even code suggested by ChatGPT, was hand-typed because I wanted to understand every line. For GenAI logs, please see the `docs` folder.

All writing is mine, for better or worse.

## Conclusion

This project was done as a personal dive into NLP on lyrics from bands I enjoy.

The models are simple and the scope is small, but this was an end-to-end project completed by me. The goal was to learn more about the data science and machine learning workflow and to build toward a reproducible pipeline.
