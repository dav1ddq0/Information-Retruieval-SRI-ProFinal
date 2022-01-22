from Retrieval_handler import Retrieval_handler
import pdfRead
# from UI_streamlit import*
# from cran_process import*
from performance import*
from system_docs_processing import*
# from text_preprocessing import*
from dummy_vectorial_model import*
# from fuzzy_model import*

def main():
    # make_cran_query_qrel_files()
    # preprocess = text_preprocessing(text= "There are 3 balls in this 4 bag, and 12 in the other one.",
    # lowercase = True,
    # convert_numbers= True,
    # remove_punctuation=True,
    # remove_stopwords=True,
    # lemmatize=True)
    # print(preprocess)
    # x = text_to_lowercase("There are 3 balls in this 4 bag, and 12 in the other one.")
    # a = convert_number_into_word(x)
    # b = remove_punctuation_marks(a)
    # r = text_remove_stopword(b)
    # s = stem_words(r)
    # l = lemmatize_words(r)
    # print(s)
    # print(l)
    # handler = Retrieval_handler(load_test_qrel_qry = True)
    # qrel = handler.qrel
    # qrys = handler.qry
    # filter_text('./system_docs')

    # convert_plane_text_to_pdf('./system_docs/1')
    # compute_and_save_corpus_data()
    # compute_and_save_vectorial_data()
    # d_vectors = unpick_pickle_file('./preprocessed/d_vectors.pickle')
    # idf = unpick_pickle_file('./preprocessed/idf.pickle')
    # print('\o/')
    # compute_matriz_degree_for_all()
    max_precision = 0
    max_sim = 0
    precision_promedio = 0
    d  =get_search_results(query = 'what similarity laws must be obeyed when constructing aeroelastic models\nof heated high speed aircraft')
    print('\o/')
    # q1 = qrys[0]
    # d_vectors, idf = compute_weight()
    # results = get_search_results(q1, d_vectors, idf)
    # # # print(results[:20])

    # p =precision(qrel[0],[doc for doc,_ in  results] )
    # print(f'Precisión ++ {p}')
    # r = recall(qrel[0], [doc for doc,_ in  results] )
    # print(f'Recobrado ++ {r}')
    # f1m = f1(qrel[0], [doc for doc,_ in  results])
    # print(f'Medida f1 {f1m}')
    # f = fallout(qrel[0], [doc for doc,_ in  results], docs_keys)
    # print(f'Fallout {f}')

    # p_promedio = 0
    # r_promedio = 0
    # f1_promedio = 0
    # fallout_promedio = 0
    # not_relevant_documents_recovered = 0
    # not_documents_recovered = 0
    
    # for pos, q in enumerate(qrys):
    #     results = get_search_results(q)
    #     if not results:
    #         not_documents_recovered +=1
        
    #     docs = [doc for doc,_ in  results]
    #     if all( d not in qrel[pos] for d in docs):
    #         not_relevant_documents_recovered +=1
        
    #     p_promedio += precision(qrel[pos], docs)
    #     r_promedio += recall(qrel[pos], docs)
    #     f1_promedio += f1(qrel[pos], docs)
    #     fallout_promedio += fallout(qrel[pos], docs, docs_terms)

    # p_promedio = p_promedio/len(qrys)
    # r_promedio = r_promedio/len(qrys)
    # f1_promedio = f1_promedio/len(qrys)
    # fallout_promedio = fallout_promedio/len(qrys)

    # print('Evaluación general:')
    # print(f'Ningún documento recuperado:{not_documents_recovered} ')
    # print(f'Ningún documento relevante recuperado :{not_relevant_documents_recovered} ')
    # print(f'Precisión  promedio: {p_promedio}')
    # print(f'Recobrado promedio: {r_promedio}')
    # print(f'Medida f1 promedio: {f1_promedio}')
    # print(f'Fallout  promedio: {f1_promedio}')
    # for pos, q in enumerate(qrys):
    #     results = get_search_results(q, d_vectors, idf)
    #     print(results)

    # print(p)
    # for pos, q in enumerate(qrys):
    #     # for i in range(1,101):
    #     # print(f"------QUERY----{pos}:")
    #     doc, sim = get_search_results(q)
    #     # for d in range(len(docs)):
    #     #     max_sim = max(max_sim, sim[d])
    #     #     print(f"Documento:.{docs[d].name}, Similitud:{sim[d]}\n")
    #     precision_promedio += precision(qrel[pos], docs)
        # max_precision = max(max_precision, prec)
        # print(f"precisión query:{pos+1}, top:{50}, precisión:{prec}")

    # print(f"---SIMILITUD MÁXIMA---{max_sim}")
    # print(f"---PRECISIÓN PROMEDIO---{precision_promedio/len(qrys)}")
    
    # handler = Retrieval_handler(load_test_qrel_qry = True)
    # qrel = handler.qrel
    # qrys = handler.qry

   
    # precision_promedio = 0

    # for pos, q in enumerate(qrys):
    #     # for i in range(1,101):
    #     # print(f"------QUERY----{pos}:")
    #     docs, sim = handler.search_coincidences(q, 100)
    #     # for d in range(len(docs)):
    #     #     max_sim = max(max_sim, sim[d])
    #     #     print(f"Documento:.{docs[d].name}, Similitud:{sim[d]}\n")
    #     precision_promedio += precision(qrel[pos], docs)
    #     # max_precision = max(max_precision, prec)
    #     # print(f"precisión query:{pos+1}, top:{50}, precisión:{prec}")

    # # print(f"---SIMILITUD MÁXIMA---{max_sim}")
    # print(f"---PRECISIÓN PROMEDIO---{precision_promedio/len(qrys)}")
    
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