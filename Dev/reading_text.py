import PyPDF2
import os
import re

def read_in_pdf(file_path):
    global text_out
    mypdf = open(r'%s' % file_path, mode='rb')
    pdf_document = PyPDF2.PdfFileReader(mypdf)


    all_text_list = []
    for i in range(pdf_document.numPages):
        page_to_print = pdf_document.getPage(i)
        text_out = page_to_print.extractText()
        
        # text_out = "".join(text_out)
        text_out = text_out.replace("\n", "").replace("\\", "")
        text_out = re.sub(r'\n\s*\n', '\n', text_out)
        text_out = text_out.strip()
        text_out = re.sub(r'[ ]{3,}', '\n', text_out)
        
        all_text_list.append(text_out)
    
    all_text = "\n".join(all_text_list)

    return all_text


if __name__=='__main__':
    DEA6_Test_File ="C:\\Users\\wirksc\\NTC Tools\\DEA 6 (FOR DEV PURPOSE ONLY)\\2015-02-26 CS DEBRIEFING OF CS-09-130228 ON FEBRUARY 26, 2015 - 1.PDF"
    file_path = os.path.join(DEA6_Test_File)
    
    pdf_text = read_in_pdf(file_path)
    
    fp_output = "C:\\Users\\wirksc\\NTC Tools\\NLP_Project\\repo"
    fp_name_output = os.path.join(fp_output, 'test_pdf.txt')
    
    with open(fp_name_output, 'w') as fp:
        fp.write(pdf_text)
        fp.close()
    
    