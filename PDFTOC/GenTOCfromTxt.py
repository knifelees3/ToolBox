# %%
from PyPDF2 import PdfReader, PdfWriter
import os
import sys


dir='C:/Users/Lenovo/Documents/Code/ToolBox/PDFTOC/'
sys.path.insert(1, '') # 为了可以让python将当前文件夹加入环境变量

os.chdir(dir)

fileName='QuantumOptics'
filetxt=fileName+'.txt'
filepdf=fileName+'.pdf'
filepdfout=fileName+'WithToc.pdf'

# read lines from txt
with open(filetxt,'r',encoding='utf-8') as f:
    lines = f.read().split(";")


numlines=int(len(lines)/3)

tit_list=[]
level_list=[]
page_list=[]
for l in range(numlines):
    level_list.append(lines[3*l].replace("\t", "").replace("\n", ""))
    tit_list.append(lines[3*l+1].replace("\t", "").replace("\n", ""))
    page_list.append(lines[3*l+2].replace("\t", "").replace("\n", ""))

# re define the pages
page_list_new=[]

for l in range(numlines):
    page_list_new.append(str(int(page_list[l])+17))

# print(level_list)
# print(page_list)
# print(page_list_new)
# # %%
# # generate bookmarks

reader_Main = PdfReader(filepdf)  # open input
writer = PdfWriter()  # open output

n_Main = len(reader_Main.pages)

for i in range(n_Main):
    writer.add_page(reader_Main.pages[i])  # insert page of Main

for l in range(numlines):
    if level_list[l]=='1':
        print(level_list[l])
        par1=writer.add_outline_item(tit_list[l], int(page_list_new[l]), parent=None)
    elif level_list[l]=='2':
        par2=writer.add_outline_item(tit_list[l], int(page_list_new[l]), parent=par1)
    elif level_list[l]=='3':
        par3=writer.add_outline_item(tit_list[l], int(page_list_new[l]), parent=par2)

with open(filepdfout, "wb") as fp:  # creating result pdf JCT
    writer.write(fp)  # writing to result pdf JCT