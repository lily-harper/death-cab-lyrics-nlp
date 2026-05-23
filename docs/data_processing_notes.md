# Data Processing Notes

These notes describe the current cleaning decisions visible in `scripts/clean.py`
and `src/lyric_preprocessing.py`.

## Missing lyrics

Rows are removed if `lyrics` is missing according to pandas `dropna`.

Rows are also removed if the raw `lyrics` string has length `0`.

Needs judgment: this step happens before text normalization, so strings that are
not technically empty but clean to an empty string may remain in the data.

## Covers

Rows are removed when `song_name` exactly matches one of the titles listed in
`remove_covers`.

Needs judgment: this is a manually curated title list. It should be reviewed when
new songs are pulled or when the Genius catalog changes.

Needs judgment: the current list appears to be missing a comma between
`"Sweet and Tender Hooligan (The Smiths cover)"` and `"The Concept"`, which
causes those two strings to be concatenated in Python.

## Duplicate versions

Rows are removed when `song_name_clean` contains any of the version terms listed
in `remove_versions`, including terms such as `demo`, `acoustic`, `remix`,
`live`, `version`, `mix`, `cover`, `kfog`, and `kexp`.

After filtering version terms, duplicate rows are dropped by `song_name_clean`.
This keeps the first remaining row for each cleaned song name.

Needs judgment: this approach depends on the version-term list and may remove
some titles that contain these words for reasons other than being alternate
versions.

## Album name shortening

Album names are converted to pandas string values and stripped of leading and
trailing whitespace.

Trailing parenthetical labels are removed from album names using a regular
expression. For example, an album name ending in a parenthetical edition label is
shortened by dropping that final parenthetical text.

The function supports a `replacements` mapping, but `scripts/clean.py` currently
calls it without any custom replacements.

Needs judgment: the current rule removes any final parenthetical text, not only
edition labels.

## Missing albums

After album shortening and year assignment, missing or blank album names are
filled with the label `Single`.

This happens after album year assignment, so missing album rows are not grouped
together as one album for year imputation.

Needs judgment: `Single` is a convenience label for missing or blank album
values. It does not necessarily mean the song was released only as a single.

## Album year assignment

`release_year` is converted to a numeric value with invalid values coerced to
missing.

For rows with a non-missing album name, every song on the same album is assigned
the most common non-missing `release_year` for that album.

Rows without a usable album name keep their original year value during this
step.

Needs judgment: if an album has a tie for most common year, pandas `mode()` is
used and the first mode is selected.

## Text normalization

`clean_text` returns an empty string for missing text.

Otherwise, text is converted to lowercase, stripped of leading and trailing
whitespace, stripped of non-word and non-whitespace characters, and collapsed so
multiple whitespace characters become one space.

In `scripts/clean.py`, this normalization is used to create `song_name_clean`
from `song_name` and `lyrics_clean` from `lyrics`.

## Copyright/data sharing limitations

The cleaning pipeline saves a cleaned parquet file that includes both `lyrics`
and `lyrics_clean`.

Needs judgment: the code in `scripts/clean.py` does not create a public-safe
dataset that excludes full lyrics. If sharing data publicly, create a separate
export that removes lyric text fields and includes only derived values.
