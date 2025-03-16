import os


def get_pdf_files(folder):
    pdf_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files
