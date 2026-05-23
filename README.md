# Soul Meets Body Meets NLP

```
"Oh come my love and swim with me,
Out in this vast Binary Sea"
- Death Cab for Cutie, Binary Sea
```

## Motivation

1. Spotify told me I had listened to **12 hours of Death Cab for Cutie** in one week
2. I wanted to learn some NLP

## Project Overview

> This project uses basic NLP to analyze lyrics and themes in songs from Death Cab for Cutie, The Postal Service, and Benjamin Gibbard's solo work.

Lyrics were collected with the Genius API, cleaned in Python, and analyzed with TF-IDF, PCA, logistic regression, word counts, and VADER sentiment analysis.

The public dataset in this repository does not include full lyrics. It includes derived values only, such as PCA components and sentiment scores, to avoid redistributing copyrighted lyrics.

## Questions

* How differently did Ben Gibbard write for Death Cab and The Postal Service?
* How does Death Cab for Cutie's tone differ between albums?
* Can we take a song and predict if it was written for Death Cab, The Postal Service, or Benjamin Gibbard's solo work?

## Methods

* TF-IDF vectorization
* PCA for dimensionality reduction and lyric similarity
* Logistic regression for artist classification
* VADER lexicon-based sentiment analysis
* Word frequency using basic whitespace tokenization

## Results

Many songs written by Benjamin Gibbard across the three projects I looked at are similar in sentiment and vocabulary.

Work within The Postal Service's album, *Give Up*, is especially lyrically cohesive.

Lyrics across DCFC's discography are predictably more spread out than the other projects with regard to sentiment.

![PCA on TF-IDF](docs/output.png)

> PCA was applied to a TF-IDF matrix to represent songs in a two-dimensional space. Points near each other share similar vocabulary patterns.

## Pipeline

```
Genius API
   |
Raw Lyrics CSV
   |
Cleaning Notebook
   |
Processed Dataset
   |
NLP Analysis
   |
Visualizations
```

## Repository Structure

```
death-cab-lyrics-nlp/
|-- data
|   |-- n_lyrics.csv              # public derived dataset
|   |-- raw/raw_lyrics.csv        # generated from Genius API, not intended for redistribution
|   `-- clean/lyrics.csv          # cleaned lyrics, not intended for redistribution
|-- docs
|   |-- output.png
|   |-- transatlanticism.png
|   `-- genAI_log_*.pdf
|-- src
|   |-- analysis.py
|   |-- count.py
|   |-- lyric_preprocessing.py
|   |-- pull.py
|   |-- sentiment.py
|   `-- visualizations.py
|-- cleaning.ipynb
|-- analysis.ipynb
|-- requirements.txt
`-- README.md
```

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
python3 src/pull.py
```

The current workflow is notebook-based:

1. Run `src/pull.py` to create `data/raw/raw_lyrics.csv`.
2. Run `cleaning.ipynb` to create `data/clean/lyrics.csv`.
3. Run `analysis.ipynb` to create analysis outputs and the public derived file, `data/n_lyrics.csv`.

The notebooks use NLTK resources for stopwords and VADER sentiment. If needed, download them in Python:

```python
import nltk
nltk.download("stopwords")
nltk.download("vader_lexicon")
```

Because the Genius catalog can change and the train/test split is currently random, exact row counts and model scores may vary slightly across runs.

## Notes

### On limitations, justifications, and improvements

Limitations:

* Small dataset, about 200 songs after cleaning
* Class imbalance, since most observations are Death Cab for Cutie songs
* Lyrics-only analysis, which ignores sound, instrumentation, production, and other musical context
* Simple models, which are useful for learning but limited in how much context they can understand

I include additional brief writing on these topics in `analysis.ipynb`.

### On not infringing copyrights

To respect copyright laws and Death Cab, I avoided including full lyrics in the public version of this project. Included instead are derived values, such as sentiment score and PCA components.

By running `pull.py` with your own Genius API token, you can rebuild the raw data locally and then run it through the `cleaning.ipynb` notebook.

### On learning and GenAI usage

Still learning. I used resources like YouTube to understand concepts and follow tutorials. **If you have any feedback, please reach out! I would really value more insight.**

I used ChatGPT primarily for code debugging, concept understanding, and learning best practices. All code, even code suggested by ChatGPT, was hand-typed because I wanted to understand every line. For GenAI logs, please see the `docs` folder.

All writing is mine, for better or worse.

![Most frequent words in Transatlanticism](docs/transatlanticism.png)

Most frequent words in the Death Cab album, *Transatlanticism*.

## Conclusion

This project was done as a personal dive into NLP on lyrics from bands I enjoy.

The models are simple and the scope is small, but this was an end-to-end project completed by me. The goal was to learn more about the data science and machine learning workflow and to build toward a reproducible pipeline.
