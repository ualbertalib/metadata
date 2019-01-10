from pdf2image import convert_from_bytes
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from os import listdir
import sys

for folder in ['A', 'B', 'C', 'D']:
	for file in listdir(folder):
		if file.endswith('.pdf'):
			input_file = folder + '/' + file
			inp = PdfFileReader((input_file), "rb")
			pages = inp.getNumPages()
			for p in range(0, pages):
				page = inp.getPage(p)

				wrt = PdfFileWriter()
				wrt.addPage(page)

				r = io.BytesIO()
				wrt.write(r)

				images = convert_from_bytes(r.getvalue())
				name = input_file.split('.')[0]
				images[0].save(name+'_'+"{0:0=4d}".format(p)+".jpg")
				print(folder, p)
				r.close()