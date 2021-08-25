"""

Author: Charles Wirks email: cwirks01@gmail.com

"""
import os
import tkinter
import tkinter.filedialog as filedialog
import PyPDF2
import en_core_web_sm
import json
import pyanx

import pandas as pd

from Lib.json_util import add_values_to_json, rm_header_dups_json
from tkinter import messagebox

nlp = en_core_web_sm.load()


def load_file():
    root = tkinter.Tk()
    root.withdraw()
    filePathName = filedialog.askopenfilenames(parent=root,
                                               title='Open file to read',
                                               filetypes=(("Text Document", "*.txt"),
                                                          ("Adobe Acrobat Document", "*.pdf"),
                                                          ("All Files", "*.*")),
                                               )
    return filePathName


def json_repo_load():
    root = tkinter.Tk()
    root.withdraw()
    answer = messagebox.askokcancel("Question", "Press ok to load repository. "
                                                "\nPress cancel to start new repository.")
    if answer:
        filePathName = filedialog.askopenfilenames(parent=root,
                                                   title='Open file to read',
                                                   filetypes=(("JSON File", "*.json"),
                                                              ("All Files", "*.*")),
                                                   )
        try:
            with open(filePathName) as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}
    else:
        Exception(" No file loaded. ")
        data = {}

    return data


def read_in_pdf(file_path):
    mypdf = open(r'%s' % file_path, mode='rb')
    pdf_document = PyPDF2.PdfFileReader(mypdf)

    text = []
    for i in range(pdf_document.numPages):
        page_to_print = pdf_document.getPage(i)
        text = page_to_print.extractText()
    return text


def read_file():
    global text
    json_data = json_repo_load()
    filepaths = load_file()
    for filepath in filepaths:
        file_basename = os.path.basename(filepath)
        print("Reading " + file_basename)
        base_split = os.path.splitext(file_basename)
        file_extension = base_split[1]
        try:
            if file_extension.endswith('txt'):
                file = open(filepath, 'r')
                text = nlp(file.read())
            elif file_extension.endswith('pdf'):
                text = nlp(read_in_pdf(filepath))
            else:
                pass

        except EOFError as e:
            print(e)

        json_data = sentence_parser(unstruct_text=text, json_data_parser=json_data)
        print('Finished processing ' + file_basename)
    save_csv_json_file(json_data)

    return


def sentence_parser(unstruct_text, json_data_parser=None):
    """
    parses out sentences and counts the amount of times objects/places/currency/dates
    are in the same sentence. Output in dataframe format with names and number.

    sentence_parser will create a csv file with statistics on the amount of times nouns
    appear in the same sentence.


    :param unstruct_text:
    :param json_data_parser:
    :return:
    """

    if json_data_parser is None:
        json_data_parser = {}
    list_sent = list(unstruct_text.sents)
    b = []
    for items in list_sent:
        a = []
        for item in items.ents:
            a.append(item.text + " - " + item.label_)
            if "%s" % (item.text + " - " + item.label_) == "Bradley - PERSON":
                b.append(items)

        json_data_parser = add_values_to_json(json_data_parser, a)
        json_data_parser = rm_header_dups_json(json_data_parser)
    with open("../repo/some2.txt", 'w') as file:
        file.write(str(b))
        file.close()
    return json_data_parser


def analyst_worksheet(df_anb, file_out_path):
    root = tkinter.Tk()
    root.withdraw()
    chart = pyanx.Pyanx()
    df_anb_count = df_anb.value_counts(subset=['name', 'value'])
    df_anb_count = df_anb_count.reset_index()
    df_anb_count = df_anb_count.rename(columns={df_anb_count.columns[0]: 'name',
                                                df_anb_count.columns[1]: 'value',
                                                df_anb_count.columns[2]: 'occurrence'})

    df_anb_count = df_anb_count[df_anb_count['occurrence'] >= 2]

    type_of = ['PERSON', 'GPE', 'NORP', 'ORG']
    for index, row in df_anb_count.iterrows():
        ents_split = row['name'].split(' - ')
        entitys_name = ents_split[0]
        entitys_type = ents_split[1]
        val_split = row['value'].split(' - ')
        val_name = val_split[0]
        value_type = val_split[1]
        max_occurences = df_anb_count.occurrence.max()
        if entitys_type in type_of:
            chart_node1 = chart.add_node(entity_type=entitys_type, label=entitys_name)
            chart_node2 = chart.add_node(entity_type=value_type, label=val_name)
            linewidth = (float(row['occurrence']) / max_occurences) * 5
            chart.add_edge(chart_node1, chart_node2,
                           label="Occurence amount %s" % row['occurrence'],
                           linewidth=linewidth)
    # file_out = filedialog.asksaveasfilename(parent=root,
    #                                         title='Save-file',
    #                                         defaultextension=".anx",
    #                                         filetypes=(("ANX File", "*.anx"),
    #                                                    ("All Files", "*.*")))
    file_out_dir = os.path.dirname(file_out_path)
    file_out_name = os.path.basename(file_out_path)
    file_out_name = os.path.splitext(file_out_name)[0]

    chart.create(os.path.join(file_out_dir, file_out_name + ".anx"))
    return


def save_csv_json_file(json_data_save, analyst_notebook=True):
    root = tkinter.Tk()
    root.withdraw()
    file_out = filedialog.asksaveasfilename(parent=root,
                                            title='Save-file',
                                            defaultextension=".csv",
                                            filetypes=(("Microsoft Excel Comma Separated Values File", "*.csv"),
                                                       ("All Files", "*.*")))

    df_data = pd.DataFrame(pd.json_normalize(json_data_save).squeeze().reset_index())
    df_data = df_data.rename(columns={df_data.columns[0]: "name", df_data.columns[1]: "value"})
    df_data = df_data.explode("value").reset_index(drop=True)
    df_data.to_csv(os.path.join(file_out), index=False)

    if analyst_notebook:
        analyst_worksheet(df_data, file_out)

    json_file_path = os.path.splitext(os.path.basename(file_out))[0]
    json_file_path = os.path.join(os.path.dirname(file_out), json_file_path + '.json')
    with open(json_file_path, "w") as write_file:
        json.dump(json_data_save, write_file, indent=4)
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

