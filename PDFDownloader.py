# giving a pdf url, download the pdf file and save it to the local disk
import requests
import os

def Download_PDF(pdf_url, pdf_path):
    # check if the file already exists
    if os.path.exists(pdf_path):
        print(f"File {pdf_path} already exists")
        return

    # download the pdf file
    r = requests.get(pdf_url)
    with open(pdf_path, 'wb') as f:
        f.write(r.content)

    print(f"File {pdf_path} downloaded")

# Example usage
# Download_PDF("https://rchiips.org/nfhs/NFHS-5Reports/National%20Report%20Volume%20II.pdf", "Reports/NFHS2.pdf")
