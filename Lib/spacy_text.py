import spacy
import os
import tkinter
import tkinter.filedialog as filedialog
import PyPDF2
import en_core_web_sm

from spacy import displacy

nlp = en_core_web_sm.load()


def export_file():
    root = tkinter.Tk()
    root.withdraw()
    filePathName = filedialog.asksaveasfilename(parent=root,
                                                title='Save-file',
                                                defaultextension=".html",
                                                filetypes=(("HTML Document", "*.html"), ("All Files", "*.*")))
    print(filePathName)
    return filePathName


def load_file():
    root = tkinter.Tk()
    root.withdraw()
    filePathName = filedialog.askopenfilename(parent=root,
                                              title='Open file to read',
                                              filetypes=(("Text Document", "*.txt"),
                                                         ("Adobe Acrobat Document", "*.pdf"),
                                                         ("All Files", "*.*")))
    return filePathName


def render_text_html(text, filepath, file_out="Demo.html"):
    dirName = os.path.dirname(filepath)
    '''
    file_out_path = os.path.join(dirName, file_out)
    f = open(file_out_path, "w")
    '''
    file_out_path = export_file()
    f = open(file_out_path, "w")
    doc_rendered = displacy.render(text, style='ent', jupyter=False)
    f.write(doc_rendered)
    f.close()
    return file_out_path


def read_in_pdf(file_path):
    mypdf = open(r'%s' % file_path, mode='rb')
    pdf_document = PyPDF2.PdfFileReader(mypdf)

    text = []
    for i in range(pdf_document.numPages):
        page_to_print = pdf_document.getPage(i)
        text = page_to_print.extractText()
    return text


def read_file(file_out="Demo.html"):
    filepath = load_file()
    base = os.path.basename(filepath)
    base_split = os.path.splitext(base)
    file_name = base_split[0]
    file_extension = base_split[1]
    try:
        if file_extension == '.txt':
            file = open(filepath, 'r')
            text = nlp(file.read())
        elif file_extension == '.pdf':
            text = nlp(read_in_pdf(filepath))
        else:
            pass

    except EOFError as e:
        print(e)

    outfile = render_text_html(text, filepath, file_out=file_out)
    return outfile


def read_html(new_type=2, file_out="Demo.html", open_in_browser=False):
    url = read_file(file_out=file_out)

    if open_in_browser:
        os.system('start %s' % url)
    # webbrowser.open(url, new=new_type)
    return


def download_html(file_out="demo.html", open_in_browser=False):
    read_html(file_out=file_out, open_in_browser=open_in_browser)
    return
