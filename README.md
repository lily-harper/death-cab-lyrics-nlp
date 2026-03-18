# Soul Meets Body (meets NLP)

## Motivation 

This project started after Spotify told me I had listened to **12 hours of Death Cab for Cutie** in one week, which felt like a good excuse to explore their lyrics while learning NLP. 

## Project overview (tl;dr)

> This project uses basic NLP to analyze lyrics and themes in songs from Death Cab for Cutie, The Postal Service, and Benjamin Gibbard's solo work.  

Data was pulled using the Genius API. 

Lyrics written by Benjamin Gibbard. 
Data was cleaned, preprocessed and analzyed by me. 

### Questions (?)

* How does Ben Gibbard write differently for Death Cab and the Postal Service? 
* How does Death Cab for Cuties lexicon develop or shift through time? 
* Can we take a song and predict if it was written for Death Cab or the Postal Service?

### Results (!)

placehold

### Pipeline 
```
Genius API
   ↓
Raw Lyrics CSV
   ↓
Cleaning Script
   ↓
Processed Dataset
   ↓
NLP Analysis
   ↓
Visualizations
```

## Repository Structure

```
project/
│
├── data
│   ├── raw
│   └── processed
│
├── src
│   ├── pull.py
│   ├── lyric_preprocessing.py
│   └── analysis.py
│
├── analysis.ipynb
├── requirements.txt
└── README.md
```

### Reproducibility 

Please run this if you want

Clone this repository: 

git clone https://github.com/lily-harper/death-cab-lyrics-nlp 

Create environment: 
```bash
pip install -r requirements.txt
```

```python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```markdown
![Python](https://img.shields.io/badge/python-3.11-blue)
![Pandas](https://img.shields.io/badge/pandas-data%20cleaning-green)
```