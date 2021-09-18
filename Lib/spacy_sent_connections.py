#!/usr/bin/ python3
"""

Author: Charles Wirks email: cwirks01@gmail.com

"""
import multiprocessing
import os
import hashlib
import random
import PyPDF2
import json
import en_core_web_sm
import datetime

import pandas as pd

from Lib.json_util import add_values_to_json, rm_header_dups_json
from Lib import pyanx
from spacy import displacy

from Lib.spacy_library_loader import load_lib

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

    for items in list_sent:
        a = []
        for item in items.ents:
            a.append(item.text + " - " + item.label_)

        json_data_parser = add_values_to_json(json_data_parser, a)
        json_data_parser = rm_header_dups_json(json_data_parser)

    return json_data_parser


def analyst_worksheet(df_anb, file_out_path):
    """
    May need to use in the main class if the file saving method is updated with tkinter
    :param df_anb:
    :param file_out_path:
    :return:
    """
    chart = pyanx.Pyanx()
    try:
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
    except Exception as e:
        print("%s \nmoving on" % e)
        pass
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
    def __init__(self, gui=False, downloads=None, upload_dir=None, repo=None, viz=True, inBrowser=False, user_dir=None,
                 username=None, password=None, answer=None, root_dir=os.getcwd()):
        self.username = username
        self.password = password
        self.nlp = en_core_web_sm.load()
        self.text = []
        self.all_text = []
        self.gui = gui
        self.viz = viz
        self.inBrowser = inBrowser
        self.answer = answer
        self.downloads = downloads
        self.uploads = upload_dir
        self.repo = repo
        self.user_dir = user_dir
        self.root_dir = root_dir
        self._user_dir()  # This assigns username and directory name to class
        self.user_root_dir_path = os.path.join(self.root_dir, 'data', self.user_dir)
        self.multiprocessing = multiprocessing

    def _user_dir(self):
        if self.username is None:
            self.username = str(random.randint(10, 10 ** 9))

        if self.user_dir is None:
            self.user_dir = hashlib.sha256(bytes('%s' % self.username, 'ascii')).hexdigest()

        self.username = self.username
        self.user_dir = self.user_dir

    def create_env_dir(self):
        # file Upload
        if self.uploads is None or self.repo is None or self.downloads is None:
            UPLOAD_FOLDER = os.path.join(self.user_root_dir_path, 'uploads')
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            self.uploads = UPLOAD_FOLDER

            # file repository
            REPO_FOLDER = os.path.join(UPLOAD_FOLDER, 'repo')
            os.makedirs(REPO_FOLDER, exist_ok=True)
            self.repo = REPO_FOLDER

            # file Download
            DOWNLOAD_FOLDER = os.path.join(self.user_root_dir_path, 'downloaded')
            os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
            self.downloads = DOWNLOAD_FOLDER

            return UPLOAD_FOLDER, REPO_FOLDER, DOWNLOAD_FOLDER

        else:
            return self.uploads, self.repo, self.downloads

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

        try:
            repo_list = os.listdir(self.repo)
            if self.gui:
                gui_answer = gui_tkinter()
                self.answer = gui_answer.message_out()
                if self.answer:
                    filePathName = gui_tkinter()
                    filePathName.load_jfile()
            else:
                filePathName = repo_list
                if len(filePathName) > 1:
                    filePathName = filePathName[0]
                elif len(filePathName) == 1:
                    filePathName = filePathName
                else:
                    filePathName = ''

                filePathName = os.path.join(self.repo, filePathName)
            try:
                with open(filePathName) as json_file:
                    data = json.load(json_file)
            except FileNotFoundError:
                data = {}
        except:
            Exception(" No library loaded. ")
            data = {}

        return data

    def read_file(self):

        json_data = load_lib(repoDir=self.repo)  # Loading in a library of previous runs in json
        filepaths = self.load_file()
        for filepath in filepaths:
            try:
                file_basename = os.path.basename(filepath)
            except Exception as e:
                print("%s \nPassing to next file" % e)
                pass
            print("Reading " + file_basename)
            base_split = os.path.splitext(file_basename)
            file_extension = base_split[1]
            try:
                if file_extension.endswith('txt'):
                    file = open(filepath, 'r')
                    self.text = file.read()
                    nlp_loaded = self.nlp(self.text)
                    file.close()
                elif file_extension.endswith('pdf'):
                    self.text = read_in_pdf(filepath)
                    nlp_loaded = self.nlp(self.text)
                elif os.path.isdir(filepath):
                    self.text = " "
                    nlp_loaded = None
                    pass
                else:
                    self.text = " "
                    nlp_loaded = None
                    pass

                if nlp_loaded is not None:
                    json_data = sentence_parser(unstruct_text=nlp_loaded, json_data_parser=json_data)
                    self.save_csv_json_file(json_data)

            except EOFError as e:
                print("%s Starting without files" % e)

            self.all_text.append(self.text)
            print('Finished processing ' + file_basename)

        # if self.viz:
        all_text_for_viz = " ".join(self.all_text)
        self.text_viz(all_text_for_viz)

        return

    def save_csv_json_file(self, json_data_save, analyst_notebook=True):
        if self.gui:
            file_out = gui_tkinter()
            file_out.save_file()
        else:
            os.makedirs(self.downloads, exist_ok=True)
            file_out = os.path.join(self.downloads, 'data.csv')

        if len(json_data_save) > 1:
            df_data = pd.DataFrame(pd.json_normalize(json_data_save).squeeze().reset_index())
            df_data = df_data.rename(columns={df_data.columns[0]: "name", df_data.columns[1]: "value"})
            df_data = df_data.explode("value").reset_index(drop=True)
        else:
            df_data = pd.DataFrame(json_data_save)

        df_data.to_csv(file_out, index=False)

        if analyst_notebook:
            analyst_worksheet(df_data, file_out)

        json_file_path = os.path.splitext(os.path.basename(file_out))[0]
        json_file_path = os.path.join(os.path.dirname(file_out), json_file_path + '.json')
        with open(json_file_path, "w") as write_file:
            json.dump(json_data_save, write_file, indent=4)

        for f in os.listdir(self.uploads):
            filePath = os.path.join(self.uploads, f)
            if os.path.isfile(filePath):
                os.remove(filePath)
        return

    def text_viz(self, text_in):

        text_in = self.nlp(text_in)
        html = displacy.render(text_in, style="ent", page=True)
        os.makedirs(self.downloads, exist_ok=True)
        output_path = os.path.join(self.downloads, "data.html")
        with open(output_path, "w", encoding="utf-8") as outputFile:
            outputFile.write(html)
            outputFile.close()

        return

    def remove_old_files(self):
        '''
        Remove all files in downloads/uploads/repos for all users that are older than 10 days
        '''
        if datetime.datetime.fromtimestamp(os.stat(self.user_root_dir_path).st_mtime) + datetime.timedelta(
                days=10) > datetime.datetime.now():
            os.remove(self.downloads)
        return

    def run(self):
        processes = []
        for i in range(2):
            p = self.multiprocessing.Process(target=self.read_file(), args=(i,))
            processes.append(p)

        [x.start() for x in processes]
