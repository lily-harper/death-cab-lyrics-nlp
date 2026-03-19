from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords 

def count_words(df, album = None, n = 20, col="slategray"):
    """ count words, remove stopwords
    """
    if album is None:
        filter_df = df.copy()
    else:
        filter_df = df[df["album"] == album]

    custom_stops = {"bop", "bah"} # sorry to the sound of settling
    stop_words = set(stopwords.words("english")).union(custom_stops)

    tokens = " ".join(filter_df["lyrics_clean"]).split()
    tokens = [word for word in tokens if word not in stop_words]

    word_counts = Counter(tokens)
    top_words = word_counts.most_common(n)

    words, counts = zip(*top_words)

    words = words[::-1] # make the top words be top 
    counts = counts[::-1]

    plt.barh(words, counts, color = col)

    if album is None:
        plt.title("Most Frequent Words in Ben Gibbard's Lyrics")
    else:
        plt.title(f"Most Frequent Words in the Album: {album}")
        

    plt.xticks(rotation = 45, ha = "right")
    plt.ylabel("Frequency")
    plt.figure(figsize=(5,3))
    plt.show()