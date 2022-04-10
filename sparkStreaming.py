import findspark
findspark.init()
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def is_positive(tweet):
    """True if tweet has positive compound sentiment, False otherwise."""
    print(sia.polarity_scores(tweet))
    if(sia.polarity_scores(tweet)['compound'] > 0):
        return 1
    elif(sia.polarity_scores(tweet)['compound'] < 0):
        return -1
    else:
        return 0


if __name__ == "__main__":
    lst = []
    sc = SparkContext("local[2]",appName="sample_data")
    ssc = StreamingContext(sc,3)
    lines = ssc.socketTextStream("localhost",9999)
    lines.pprint()
    data = lines.map(lambda line: is_positive(line))
    data.pprint()
    ssc.start()
    ssc.awaitTermination()