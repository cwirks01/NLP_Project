import os
from io import BytesIO
import base64

import matplotlib.pyplot as plt
from pandas.io.json import json_normalize

from pymongo import MongoClient
from wordcloud import WordCloud

MONGO_DB_USERNAME = os.environ['MONGO_DB_USERNAME']
MONGO_DB_PASSWORD = os.environ['MONGO_DB_PASSWORD']
MONGO_HOST = "mongodb"
MONGO_PORT = "27017"

# DEBUGING
# MONGO_DB_USERNAME = "root"
# MONGO_DB_PASSWORD = "password"
# MONGO_HOST = "23.23.40.32"
# MONGO_PORT = "27019"

MONGO_NLP_DB = "NLP_db"
MONGODB_NLP_URI = 'mongodb://%s:%s@%s:%s/%s?authSource=admin'% (MONGO_DB_USERNAME,
                                                                MONGO_DB_PASSWORD,
                                                                MONGO_HOST,
                                                                MONGO_PORT,
                                                                MONGO_NLP_DB)

NLP_db = MongoClient(MONGODB_NLP_URI)

def cloud_app(username=None, db=NLP_db):
    
    user_db = db.NLP_db.users.find({"username":username})
    text = user_db[0]['repository'][0]['text']

    new_text = json_normalize(text).transpose()
    new_text = new_text.reset_index()
    new_text = new_text.rename({new_text.columns[0]:"item",new_text.columns[1]:"values"},axis='columns')
    new_text['len_list'] = new_text["values"].str.len()
    new_text = new_text.sort_values("len_list", ascending=False)
    new_text = new_text.reset_index(drop=True)

    temp_wordCloudList = new_text['item'].apply(lambda x: x.split(" - ")[0])
    new_text['newItem'] = temp_wordCloudList

    d={}
    for index, i in new_text.iterrows():
        d[i['newItem']] = int(i['len_list'])

    wordcloud = WordCloud(background_color="white", width=800, height=400).generate_from_frequencies(d)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    # plt.figure(figsize=(15,10))
    plt.axis("off")
    plt.tight_layout(pad=0)
    
    data = BytesIO()
    plt.savefig(data, format='png')
    plt.close()
    data.seek(0)
    plot_url = base64.b64encode(data.getvalue()).decode('utf8')

    # return render_template("index.html", plot_url=plot_url, main_app=False)
    return plot_url


# if __name__=="__main__":
#     app.run()