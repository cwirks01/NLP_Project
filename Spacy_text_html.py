import spacy
import os
import tkinter
import tkinter.filedialog as filedialog
import webbrowser
import en_core_web_sm

from spacy import displacy

nlp = en_core_web_sm.load()


def load_file():
    root = tkinter.Tk()
    root.withdraw()
    filePathName = filedialog.askopenfilename(parent=root, title='Open file to encrypt')

    return filePathName


def render_text_html(text, filepath, file_out="Demo.html"):
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
    os.system('start %s' % url)
    # webbrowser.open(url, new=new_type)
    return


def main():
    read_html()
    return


if __name__ == '__main__':
    main()
