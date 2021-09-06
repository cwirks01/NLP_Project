#!/usr/bin/ python3
"""

Author: Charles Wirks email: cwirks01@gmail.com

"""
import os
import PyPDF2
import json
import en_core_web_sm

import pandas as pd

from Lib.json_util import add_values_to_json, rm_header_dups_json
from Lib import pyanx

ROOT = os.getcwd()


class gui_tkinter:

    def __init__(self):
        from tkinter import filedialog as tk_filedialog
        from tkinter import messagebox as tk_messagebox
        import tkinter as tk

        self.filedialog = tk_filedialog
        self.tk_root = tk.Tk()
        self.messagebox = tk_messagebox
        self.tk_root.withdraw()

    def load_files(self):
        filePathName = self.filedialog.askopenfilenames(parent=self.tk_root,
                                                        title='Open file to read',
                                                        filetypes=(("Text Document", "*.txt"),
                                                                   ("Adobe Acrobat Document", "*.pdf"),
                                                                   ("All Files", "*.*")))
        return filePathName

    def load_jfile(self):
        filePathName = self.filedialog.askopenfilenames(parent=self.tk_root,
                                                        title='Open file to read',
                                                        filetypes=(("Text Document", "*.txt"),
                                                                   ("JSON", "*.json"),
                                                                   ("All Files", "*.*")))
        return filePathName

    def save_file(self):
        file_out = self.filedialog.asksaveasfilename(parent=self.tk_root,
                                                     title='Save-file',
                                                     defaultextension=".csv",
                                                     filetypes=(
                                                         ("Microsoft Excel Comma Separated Values File", "*.csv"),
                                                         ("All Files", "*.*")))
        return file_out

    def message_out(self):
        try:
            answer = self.messagebox.askyesno("Question", "Would you like to load a repository?")
        except RuntimeError as e:
            print(e)
            answer = False
            pass
        return answer


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
    with open("./repo/some2.txt", 'w') as file:
        file.write(str(b))
        file.close()
    return json_data_parser


def analyst_worksheet(df_anb, file_out_path):
    """
    May need to use in the main class if the file saving method is updated with tkinter
    :param df_anb:
    :param file_out_path:
    :return:
    """
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
    file_out_dir = os.path.dirname(file_out_path)
    file_out_name = os.path.basename(file_out_path)
    file_out_name = os.path.splitext(file_out_name)[0]

    chart.create(os.path.join(file_out_dir, file_out_name + ".anx"))
    return


def read_in_pdf(file_path):
    global text_out
    mypdf = open(r'%s' % file_path, mode='rb')
    pdf_document = PyPDF2.PdfFileReader(mypdf)

    for i in range(pdf_document.numPages):
        page_to_print = pdf_document.getPage(i)
        text_out = page_to_print.extractText()
    return text_out


class spacy_sent_connections:

    def __init__(self, gui=False, downloads='downloaded', upload_dir='uploads', repo='repo'):
        self.nlp = en_core_web_sm.load()
        self.text = []
        self.gui = gui
        self.downloads = os.path.join(ROOT, downloads)
        self.uploads = os.path.join(ROOT, upload_dir)
        self.repo = os.path.join(self.uploads, repo)
        if os.path.exists(self.repo):
            self.answer = True
        else:
            self.answer = False

    def load_file(self):
        if self.gui:
            filePathName = gui_tkinter()
            filePathName.load_files()
        else:
            filePathList = []
            for file in os.listdir(self.uploads):
                fp = os.path.join(self.uploads, file)
                filePathList.append(fp)
            filePathName = filePathList
        return filePathName

    def json_repo_load(self):

        if self.answer:
            if self.gui:
                gui_answer = gui_tkinter()
                self.answer = gui_answer.message_out()
                if self.answer:
                    filePathName = gui_tkinter()
                    filePathName.load_jfile()
            else:
                os.makedirs(self.repo, exist_ok=True)
                filePathName = os.listdir(self.repo)[0]

            try:
                with open(filePathName) as json_file:
                    data = json.load(json_file)
            except FileNotFoundError:
                data = {}
        else:
            Exception(" No file loaded. ")
            data = {}

        return data

    def read_file(self):
        json_data = self.json_repo_load()
        filepaths = self.load_file()
        for filepath in filepaths:
            file_basename = os.path.basename(filepath)
            print("Reading " + file_basename)
            base_split = os.path.splitext(file_basename)
            file_extension = base_split[1]
            try:
                if file_extension.endswith('txt'):
                    file = open(filepath, 'r')
                    self.text = self.nlp(file.read())
                elif file_extension.endswith('pdf'):
                    self.text = self.nlp(read_in_pdf(filepath))
                else:
                    pass
                file.close()

            except EOFError as e:
                print(e)

            json_data = sentence_parser(unstruct_text=self.text, json_data_parser=json_data)
            print('Finished processing ' + file_basename)
        self.save_csv_json_file(json_data)

        return

    def save_csv_json_file(self, json_data_save, analyst_notebook=True):
        if self.gui:
            file_out = gui_tkinter()
            file_out.save_file()
        else:
            os.makedirs(self.downloads, exist_ok=True)
            file_out = os.path.join(self.downloads, 'data.csv')

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

        for f in os.listdir(self.uploads):
            filePath = os.path.join(self.uploads, f)
            if os.path.isfile(filePath):
                os.remove(filePath, )
        return
        