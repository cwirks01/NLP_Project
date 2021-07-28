import spacy
import os
import numpy as np
import tkinter
import tkinter.filedialog as filedialog
import webbrowser

from spacy.matcher import DependencyMatcher
from spacy import displacy
from tkinter import *

nlp = spacy.load("en_core_web_sm")


def load_file():
    root = tkinter.Tk()
    root.withdraw()
    filePathName = filedialog.askopenfilename(parent=root, title='Open file to encrypt')

    return filePathName


def render_text_html(text, filepath, file_out="newTest.html"):
    dirName = os.path.dirname(filepath)
    file_out_path = os.path.join(dirName, file_out)
    f = open(file_out_path, "w")
    doc_rendered = displacy.render(text, style='ent', jupyter=False)
    f.write(doc_rendered)
    f.close()
    return file_out_path


def read_file():
    filepath = load_file()
    base = os.path.basename(filepath)
    base_split = os.path.splitext(base)
    file_name = base_split[0]
    file_extension = base_split[1]
    try:
        if file_extension == '.txt':
            file = open(filepath, 'r')
            text = nlp(file.read())
        else:
            pass

    except EOFError as e:
        print(e)

    outfile = render_text_html(text, filepath)
    return outfile


def read_html(new_type=2):
    url = read_file()
    webbrowser.get('chrome').open(url, new=new_type)
    return


def show_ents(doc):
    if doc.ents:
        for ent in doc.ents:
            print(ent.text + ' - ' + ent.label_ + ' - ' + str(spacy.explain(ent.label_)))
        else:
            print('No entities found')


def main():
    read_html()
    return


if __name__ == '__main__':
    main()

'''
master = Tk()
variable = StringVar(master)
variable.set("one")  # default value
w = OptionMenu(master, variable, "one", "two", "three")
w.pack()
mainloop()

filepath = os.getcwd()
filePathList = os.listdir(os.getcwd())
file_idx = np.where([x.__contains__("txt") for x in filePathList])[0][0]
fileName = filePathList[file_idx]
filePathName = os.path.join(filepath, fileName)
print(filePathName, os.path.exists(filePathName))

doc_rendered = displacy.render(about, style='ent', jupyter=False)
f = open("newTest.html", "w")
f.write(doc_rendered)
f.close()

matcher = DependencyMatcher(nlp.vocab)
pattern = [{"RIGHT_ID": "founded_id",
            "RIGHT_ATTRS": {"ORTH": "founded"}}]
matcher.add("FOUNDED", [pattern])

matches = matcher(about)
'''
