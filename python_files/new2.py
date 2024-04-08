from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from textstat import flesch_reading_ease

c = TextBlob("I am not happy").sentiment.polarity
print(c)

if c<0:
  print('Negative')
elif c==0:
  print('Neutral')
else:
  print('Positive')

#The commutator is peculiar, consisting of only three segments of a copper ring, while in the simplest of other continuous current generators several times that number exist, and frequently 120! segments are to be found

a = flesch_reading_ease("So what is a solid? Solids are usually hard be")
print(a)

def complexity(x):
    if x<10:
        return 'Professional'
    elif x>10 and x<=30:
        return 'College graduate(Very Difficult)'
    elif x>30 and x<=50:
        return 'College (Difficult)'
    elif x>50 and x<=60:
        return '10th to 12th grade(Fairly difficult)'
    elif x>60 and x<=70:
        return '8th & 9th grade(Plain English)'
    elif x>70 and x<=80:
        return '7th grade(Fairly easy)'
    elif x>80 and x<=90:
        return '6th grade(Easy to read)'
    elif x>90:
        return '5th grade(Very easy)'

print(complexity(a))