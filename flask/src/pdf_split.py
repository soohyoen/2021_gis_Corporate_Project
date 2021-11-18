from PyPDF2 import PdfFileReader, PdfFileWriter
import io

class PDFSplit:
    def __init__(self, data):
        self._data = io.BytesIO(data.read())

    def page_split(self):
        bytes_list = []

        pdf_reader = PdfFileReader(self._data)

        for page_num in range(pdf_reader.getNumPages()):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(page_num))

            tmp = io.BytesIO()
            pdf_writer.write(tmp)
            tmp.seek(0)
            
            bytes_list.append(tmp)
        
        return bytes_list