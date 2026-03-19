
from nltk.sentiment.vader import SentimentIntensityAnalyzer 

def vader(df, text_col): 
    analyzer = SentimentIntensityAnalyzer()

    df["sentiment"] = df[text_col].apply(
        lambda x: analyzer.polarity_scores(x)["compound"]
    )

    return df 