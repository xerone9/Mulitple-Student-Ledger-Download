import os, glob
import requests
import webbrowser
from PyPDF2 import PdfFileMerger

stopProgram = False
desktop = os.path.expanduser("~\desktop\\")

print("""

!!! Destroying Old Generate Files From Folder !!!

Bulk Ledger Printing Application (Only For Indus University LMS)
================================================================

First We Need To Obtain The HASH. So,

Open your browser and Login to LMS Account and Open any student Ledger and Click "Simple Ledger Print".
Once the Ledger is opened copy the URL and Paste Below

""")
URL = input("Enter URL: ")
print("")
print("Create Text File on Desktop and Paste IDs in it.")
print("")
getTextFile = input("Enter Text File Name with Extension. Example (ID.txt): ")
deleteFiles = glob.glob('mydir\\*.pdf')

for filePath in deleteFiles:
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file : ", filePath)


def download(url: str, dest_folder: str, id: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = id  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        # print("saving to", os.path.abspath(file_path))
        print("Fetching Ledger... " + filename)
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

file = open(desktop + getTextFile, 'r')
Lines = file.readlines()
for line in Lines:
    id = line.strip()
    modifiedURL = URL[0:len(URL) - 23] + str(id) + "&v_voucher_no="
    try:
        download(modifiedURL, dest_folder="mydir", id=id + ".pdf")
    except requests.exceptions.ConnectionError:
        print("")
        input("!!!! It seems there is a problem with your Internet Connection !!!!\nPress Enter To Exit...")
        stopProgram = True
        break
    except requests.exceptions.MissingSchema:
        print("")
        input("!!!! Invalid URL !!!!\nPress Enter To Exit...")
        stopProgram = True
        break

if stopProgram != True:
    file.close()
    os.chdir("mydir")
    file_dict = {}
    for file in sorted(glob.glob("*.pdf"), key=os.path.getmtime):
        filepath = file
        if filepath.endswith((".pdf", ".PDF")):
            file_dict[file] = filepath
    merger = PdfFileMerger(strict=False)

    for k, v in file_dict.items():
        merger.append(v)
    merger.write("merged.pdf")
    merger.close()

    os.startfile('merged.pdf')
    webbrowser.open("")

