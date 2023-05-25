# 在此更改文件夹以及文件名
dir='C:/Users/Lenovo/Documents/Dropbox/ProjectPostdoc/02_PulseShapingCavityStucture/Notes/'
fileName = '20230521_基于超表面的光子波包波形整形'
dele=1 # 0代表删除，1代表不删除

from PyPDF2 import PdfReader, PdfWriter
import os
import sys


def genToc(dir,fielName,dele):

    sys.path.insert(1, '') # 为了可以让python将当前文件夹加入环境变量

    os.chdir(dir)


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

    #print(tit_list)
    #print(level_list)
    #print(page_list)


    # generate bookmarks

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
    
    return 0


genToc(dir,fileName,dele)