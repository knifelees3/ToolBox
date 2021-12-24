import pdfx
pdf = pdfx.PDFx(
    "C:\\Users\\xiail\\Downloads\\PDF\\PhysRevA.101.063816.pdf")
metadata = pdf.get_metadata()
references_list = pdf.get_references()
references_dict = pdf.get_references_as_dict()
pdf.download_pdfs("./")
