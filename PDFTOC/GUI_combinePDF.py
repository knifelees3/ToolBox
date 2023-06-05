from PyPDF2 import PdfReader, PdfWriter
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# Function to select files
def select_file():
    global filename

    filetypes = (
        ('text files', '*.pdf'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )


# Function to generate file name
def genToc():

    sys.path.insert(1, '') # 为了可以让python将当前文件夹加入环境变量
    dir=os.path.dirname(filename)
    fileName_Pur=os.path.basename(filename)
    fileName=fileName_Pur[:-4]
    print(fileName)
    os.chdir(dir)

    dele=select.get()
    filetxt=fileName+'.txt'
    filepdf=fileName+'.pdf'
    filepdfTOC=fileName+'Toc.pdf'
    filepdfout=fileName+'WithToc.pdf'

    # read lines from txt
    with open(filetxt,'r',encoding='utf-8') as f:
        lines = f.read().split(";")


    numlines=int(len(lines)/3)

    tit_list=[]
    level_list=[]
    page_list=[]
    for l in range(numlines):
        tit_list.append(lines[3*l].replace("\t", "").replace("\n", ""))
        level_list.append(lines[3*l+1].replace("\t", "").replace("\n", ""))
        page_list.append(lines[3*l+2].replace("\t", "").replace("\n", ""))



    # Generate bookmarks
    reader_Main = PdfReader(filepdf)  # open input
    reader_Toc = PdfReader(filepdfTOC)  # open input
    writer = PdfWriter()  # open output

    n_Main = len(reader_Main.pages)
    n_Toc = len(reader_Toc.pages)

    for i in range(n_Toc):
        writer.add_page(reader_Toc.pages[i])  # insert page of TOC

    for i in range(n_Main):
        writer.add_page(reader_Main.pages[i])  # insert page of Main

    for l in range(numlines):
        if level_list[l]=="1":
            par1=writer.add_outline_item(tit_list[l], int(page_list[l]), parent=None)
        elif level_list[l]=="2":
            par2=writer.add_outline_item(tit_list[l], int(page_list[l]), parent=par1)
        elif level_list[l]=="3":
            par3=writer.add_outline_item(tit_list[l], int(page_list[l]), parent=par2)

    with open(filepdfout, "wb") as fp:  # creating result pdf JCT
        writer.write(fp)  # writing to result pdf JCT

    if dele==0:
        # Delete the mid files
        os.remove(filepdf)
        os.remove(filepdfTOC)
        os.remove(filetxt)
    
    showinfo(
        title='TOC for selected PDF has been generated in the following file:',
        message=os.path.basename(filename),
    )
    
    return 0


filename = "" # global variabl


explanation = """Author: Zhaohua Tian
Email: knifelees3@gmail.com
Web: knifelees3@github.io
This is to generate TOC for pdf files 
exported from Mathematica. Corresponding 
helping files should be prepared.
Further information can be found in 
my personal blog.
Posted on: 2023-06-05"""



root = tk.Tk()
root.wm_title("Generate TOC for PDF fiels")
root.resizable(False, False)
root.geometry('300x300')

lbl_1 = tk.Label(root, text=explanation)
lbl_1.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# open button
open_button = ttk.Button(
    root,
    text='Open the main pdf exported from Mathematica',
    command=select_file
)
open_button.pack(expand=True)

select = tk.IntVar()
select.set(1)  # initializing the choice, i.e. Python
rad_delete = tk.Radiobutton(root,text='Delete helping files', value=0,variable=select)
rad_delete.pack()
rad_keep = tk.Radiobutton(root,text='Keep helping files', value=1,variable=select)
rad_keep.pack()


# the selected choic
tk.Button(root, text='Generate TOC for PDF', command=genToc).pack()

# run the application
root.mainloop()


