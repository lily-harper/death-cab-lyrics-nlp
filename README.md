# Soul Meets Body (meets NLP)

```
"Out in this Binary Sea 
Zeros and ones patterns appear
- Death Cab for Cutie, Binary Sea
```

## Motivation 

1. Spotify told me I had listened to **12 hours of Death Cab for Cutie** in one week
2. I wanted to learn some NLP  

## Project overview (tl;dr)

> This project uses basic NLP to analyze lyrics and themes in songs from Death Cab for Cutie, The Postal Service, and Benjamin Gibbard's solo work.  

Data was pulled using the Genius API. 

Lyrics written by Benjamin Gibbard. 
Data preprocessed and analzyed by me. 

### Questions (?)

* How differently did Ben Gibbard write for Death Cab and the Postal Service? 
* How does Death Cab for Cutie's tone differ between albums?
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
│   └── clean
|
├── docs 
│   ├── genAI_logs.pdf
|
├── src
│   ├── pull.py
│   ├── lyric_preprocessing.py
|   ├── modeling.py
│   └── analysis.py
│
├── analysis.ipynb
├── requirements.txt
└── README.md
```

### Reproducibility 

Please run this if you want

Clone this repository: 

```
git clone https://github.com/lily-harper/death-cab-lyrics-nlp 
```

Create environment: 

```bash
pip install -r requirements.txt
```

```python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
