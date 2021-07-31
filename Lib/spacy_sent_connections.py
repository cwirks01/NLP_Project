import spacy
import os
import tkinter
import tkinter.filedialog as filedialog
import PyPDF2
import en_core_web_sm
import json

import pandas as pd

from spacy import displacy

nlp = en_core_web_sm.load()


def load_file():
    root = tkinter.Tk()
    root.withdraw()
    filePathName = filedialog.askopenfilename(parent=root,
                                              title='Open file to read',
                                              filetypes=(("Text Document", "*.txt"),
                                                         ("Adobe Acrobat Document", "*.pdf"),
                                                         ("All Files", "*.*")))
    return filePathName


def read_in_pdf(file_path):
    mypdf = open(r'%s' % file_path, mode='rb')
    pdf_document = PyPDF2.PdfFileReader(mypdf)

    text = []
    for i in range(pdf_document.numPages):
        page_to_print = pdf_document.getPage(i)
        text = page_to_print.extractText()
    return text


def sentence_parser(text, json_data=None, file_path=os.getcwd(), file_out='Demo.txt'):
    """
    parses out sentences and counts the amount of times objects/places/currency/dates
    are in the same sentence. Output in dataframe format with names and number.

    sentence_parser will create a csv file with statistics on the amount of times nouns
    appear in the same sentence.


    :param file_path:
    :param file_out:
    :param json_data:
    :param text:
    :return:
    """
    list_sent = list(text.sents)

    two_items = list_sent

    json_data = json_data
    filepath = file_path
    file_out = file_out

    json_stats = json_data_search(two_items, json_data)

    return


def json_data_search(text, data):
    """
    json data will return with dataframe of statistics of the amount of times a
    noun has appeared with another noun.
    :param text:
    :param data:
    :return pandas.dataFrame:
    """


    return data


def json_repo_load(file_path):
    base = os.path.basename(file_path)
    dir_name = os.path.dirname(file_path)
    base_split = os.path.splitext(base)
    file_name = base_split[0] + '.json'
    new_file_path = os.path.join(dir_name, file_name)
    try:
        with open(new_file_path) as json_file:
            data = json.load(json_file)
    except:
        data = {}

    return data


def read_file(file_out="Demo.html"):
    global json_data, text
    filepath = load_file()
    base = os.path.basename(filepath)
    base_split = os.path.splitext(base)
    file_extension = base_split[1]
    try:
        json_data = json_repo_load(filepath)
        if file_extension == '.txt':
            file = open(filepath, 'r')
            text = nlp(file.read())
        elif file_extension == '.pdf':
            text = nlp(read_in_pdf(filepath))
        else:
            pass

    except EOFError as e:
        print(e)

    sentence_parser(text, json_data=json_data, filepath=filepath, file_out=file_out)

    return
