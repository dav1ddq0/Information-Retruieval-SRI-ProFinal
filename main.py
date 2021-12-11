import pdfRead


def main():
    path = '../PDFs/1.pdf'
    text = pdfRead.extract_text_from_pdf(path)
    newFile = open('pdfText.txt','w')
    newFile.write(text)
    newFile.close()
    print(text)

if __name__ == '__main__':
    main()