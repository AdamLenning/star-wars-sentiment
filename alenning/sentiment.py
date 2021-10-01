import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from afinn import Afinn
from textblob import TextBlob
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

#Initialize Spark Session
spark = SparkSession \
            .builder \
                .appName("Python Spark SQL basic example") \
                    .master("spark://10.28.53.201:7077") \
                        .getOrCreate()

# Read txt files into (spark) df
ep4 = spark.read.csv('SW_EpisodeIV.txt', header=True,sep=" ")
ep4 = ep4.withColumn('movie', F.lit("Episode 4")) 

ep5 = spark.read.csv('SW_EpisodeV.txt', header=True,sep=" ")
ep5 = ep5.withColumn('movie', F.lit("Episode 5"))

ep6 = spark.read.csv('SW_EpisodeVI.txt', header=True,sep=" ")
ep6 = ep6.withColumn('movie', F.lit("Episode 6"))

# Union to 1 DataFrame
df = ep4.union(ep5)
df = df.union(ep6)

# Vader Sentiment
# It is a human-validated sentiment analysis method developed for Twitter and social media contexts
analyzer = SentimentIntensityAnalyzer()
analyzer_udf = F.udf(lambda dialogue: analyzer.polarity_scores(dialogue)['compound'])
df = df.withColumn('vader', analyzer_udf(df.dialogue))
df.show(10)

# # Afinn Sentiment
# # Builds a Twitter based sentiment Lexicon including Internet slangs and obscene words
# afinn = Afinn()
# for i, row in df.iterrows():
#     df.at[i,'afinn'] = afinn.score(str(df.at[i, 'dialogue']))

# # TextBlob Sentiment
# for i, row in df.iterrows():
#     df.at[i,'textBlob'] = TextBlob(str(df.at[i, 'dialogue'])).sentiment.polarity

# # aggregate stats based on all characters
# mean_all = df.groupby(['character', 'movie']).mean().sort_values(by="vader")
# print(mean_all)

# # Stats for nth most verbose characters
# counts = df.groupby('character').size().nlargest(10)
# comp = df[df['character'].isin(counts.index)].groupby(['character', 'movie']).mean().sort_values(by="character")
# print(comp)

# # Movie Stats
# movie = df.groupby(['movie']).mean()
# print(movie)


# # Perform Logistic Regression
# lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
# lrModel = lr.fit(df)

# print("Coefficients: \n" + str(lrModel.coefficientMatrix))
# print("Intercept: " + str(lrModel.interceptVector))

# trainingSummary = lrModel.summary
