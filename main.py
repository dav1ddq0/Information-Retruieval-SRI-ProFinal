from Retrieval_handler import Retrieval_handler
import pdfRead
# from UI_streamlit import*
from cran_process import*
from performance import*
def test_main(): ...



def main():
    # make_cran_query_qrel_files()
    handler = Retrieval_handler(load_test_qrel_qry = True)
    qrel = handler.qrel
    qrys = handler.qry

    
    for pos, q in enumerate(qrys):
        for i in range(1,101):
            docs = handler.search_coincidences(q, i)
            print(f"preciosion query:{pos+1}, top:{i}, precisión:{precision(qrel[pos], docs)}")

        
    
    # for q in qrel:
    #     print(q)
    #     print('\n')
    # ui = UIStremlit()
    # ui.update_menu('Prueba')
    # path = '../PDFs/1.pdf'
    # text = pdfRead.extract_text_from_pdf(path)
    # newFile = open('pdfText.txt','w')
    # newFile.write(text)
    # newFile.close()
    # print(text)

if __name__ == '__main__':
    main()