from wordcloud import WordCloud
from matplotlib import pyplot as plt

a = "aaa"


def create_wordcloud():
    if len(data) == 0:
        print "Dataset empty."
        return [go.Scatter( x = [] , y = [] )]

    wordcloud = WordCloud(max_font_size=40).generate(a)

    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
