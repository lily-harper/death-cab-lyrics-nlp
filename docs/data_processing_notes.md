# Data Processing Notes

These notes describe the current cleaning decisions visible in `scripts/clean.py`
and `src/lyric_preprocessing.py`.

Choices made, especially during the preprocessing stage, impact the analysis so I included these notes for transparency. I wanted to document where I made choices and judgement calls. 

## Missing lyrics

Rows are removed if `lyrics` is missing according to pandas `dropna`.

Rows are also removed if the raw `lyrics` string has length `0`.

## Covers

Rows are removed when `song_name` exactly matches one of the titles listed in
`remove_covers`.

Judgement: this is a manually curated title list. It should be reviewed when
new songs are pulled or when the Genius catalog changes.


## Duplicate versions

Rows are removed when `song_name_clean` contains any of the version terms listed
in `remove_versions`, including terms such as `demo`, `acoustic`, `remix`,
`live`, `version`, `mix`, `cover`, `kfog`, and `kexp`.

After filtering version terms, duplicate rows are dropped by `song_name_clean`.
This keeps the first remaining row for each cleaned song name.

Limitation: This may remove some titles that contain these words for reasons other than being alternate versions. 


## Missing albums

After album shortening and year assignment, missing or blank album names are
filled with the label `Single`.

This happens after album year assignment, so missing album rows are not grouped
together as one album for year imputation.

Judgment: `Single` is a convenience label for missing or blank album
values and does not necessarily mean the song was released only as a single.

## Text normalization

`clean_text` returns an empty string for missing text.

Otherwise, text is converted to lowercase, stripped of leading and trailing
whitespace, stripped of non-word and non-whitespace characters, and collapsed so
multiple whitespace characters become one space.

In `scripts/clean.py`, this normalization is used to create `song_name_clean`
from `song_name` and `lyrics_clean` from `lyrics`.
