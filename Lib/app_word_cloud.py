#!/usr/bin/ python3
import os
import matplotlib

import pandas as pd
import matplotlib.pyplot as plt
from base64 import b64encode
from io import StringIO, BytesIO

from wordcloud import WordCloud

matplotlib.use('TKAgg')

def appWordCloud(text):

    # Create and generate a word cloud image:
    wordcloud = WordCloud(background_color="white").generate(",".join(text['words'].tolist()))
    plt.figure()
    fig = plt.gcf()
    
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    imgdata = StringIO()
    imgdata_byte = BytesIO()
    fig.savefig(imgdata_byte, format='png')
    imgdata.seek(0)  # rewind the data

    encoded = imgdata_byte
    mime = "image/png"
    uri = "data:%s;base64,%s" % (mime, encoded)

    return uri

if __name__=="__main__":
    file_path="C:\\Users\\cwirk\\Documents\\git_projects\\wordcloud.csv"
    file_path=os.path.join(file_path)

    text = pd.read_csv(file_path)
    appWordCloud(text)