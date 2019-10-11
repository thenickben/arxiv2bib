from paper import Paper
import PyPDF2 
import re
import os
from os import listdir
from os.path import isfile, join
import logger
import shutil

def get_arxiv_code(filename, path = None):
    if not path:
        path = './'
    root = path
    pdfFileObj = open(os.path.join(root, filename), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    arxiv = str(pageObj.extractText())
    found = re.search('arXiv:(.+?) ', arxiv)
    if found is None:
        code = None
    #generates arxiv code
    else:
        found = found.group(1)
        first = found.split(".")[0]
        second = found.split(".")[1].split("v")[0]
        code = first + "." + second
    return code

def add_paper(filename_, bibtex_name, path = None):
    if not path:
        path = './'
    root = path
    done_path = os.path.join(root, 'done')
    failed_path = os.path.join(root, 'failed')

    filename = filename_.split(".")
    if len(filename[1])==4 and len(filename[2])==5:
        ref = filename[0]
        code = filename[1]+"."+filename[2]
    else:
        code = get_arxiv_code(filename_, root)
        ref = 'ADD_REF'

    if code is not None:
    # If code is provided by filename OR pdf was downloaded from ArXiv:
        paper = Paper(code = code, 
                    bibtex_name = bibtex_name)

        add_new = logger.check_ref(bibtex_name, ref)
        if add_new:
            paper.add_bib(ref) 
            paper.add_abstract(ref)
            shutil.move(os.path.join(root, filename_), done_path)
            print(filename_, " paper added to", bibtex_name)
            status = 'ok'
        else:
            print(filename_, " paper already exists in", bibtex_name)
            status = 'repeated'
    else:
        print(filename_, 'paper was not able to being added')
        shutil.move(os.path.join(root, filename_), failed_path)
        status = 'fail'
    return status, ref

def add_papers_from_path(bibtex_name, path = None):
    if not path:
        path = './'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    pdfs = [i for i in files if ".pdf" in i] 
    if len(pdfs) == 0:
        print("No pdf files found")
    else:
        for pdf in pdfs:
            status, ref = add_paper(pdf, bibtex_name, path)
            if status == 'fail':
                ref = str(pdf)
            if status is not 'repeated':
                logger.log_bib(bibtex_name,ref,status)
                

def show_bibs(path = None):
    if not path:
        path = './'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    bibs = [i for i in files if ".bib" in i]
    if len(bibs) == 0:
        print("No bib files found")
    else:
        print(" Path contains a total of", len(bibs), " bib files:")
        for i, file in enumerate(bibs):
            print(i, ".", file)

def get_bibs(path = None):
    if not path:
        path = './'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    bibs = [i for i in files if ".bib" in i]
    return bibs

def show_pdfs(path = None):
    if not path:
        path = './'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    pdfs = [i for i in files if ".pdf" in i]
    if len(pdfs) == 0:
        print("No pdf files found")
    else:
        print(" Path contains a total of", len(pdfs), " bib files:")
        for i, file in enumerate(pdfs):
            print(i, ".", file)

def show_files(path = None):
    if not path:
        path = './'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    print(" Path contains a total of", len(files), "files:")
    for i, file in enumerate(files):
        print(i, ".", file)


def get_paper_number(number, path = None):
    if not path:
        path = './'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    pdfs = [i for i in files if ".pdf" in i]
    if len(pdfs) < number:
        print("The number of pdf files is", len(pdfs), ", please choose another number")
    else:
        return pdfs[number]

def get_bibtex_number(number, path = None):
    if not path:
        path = './'
    files = [f for f in listdir(path) if isfile(join(path, f))]
    bibs = [i for i in files if ".bib" in i]
    if len(bibs) < number:
        print("The number of pdf files is", len(bibs), ", please choose another number")
    else:
        return bibs[number]

def show_bib_file(bibtex_name, path = None):
    if not path:
        path = './'
    with open(bibtex_name,"r") as bib:
        for line in bib:
            print(line)

def make_files(bibtex_name, path = None):
    if not path:
        path = './'
    bibs = get_bibs()
    if (bibtex_name) not in bibs:
        filenames = []
        filenames.append(bibtex_name)
        bibname = bibtex_name.split('.')[0]
        filenames.append(bibname + "_log.txt")
        filenames.append(bibname + "_abstract.tex")
        filenames.append(bibname + "_latex.tex")
        for file in filenames:
            bib = open(file,"x")
            bib.close
        #init abstract section
        section_title = "\\section{"+bibname+"} \n"
        abstract = open(bibname + "_abstract.tex", "a+")
        abstract.write(section_title)
    else:
        print("bibtex name already exists!")

def move_files(bibtex_name, path = None):
    if not path:
        path = './'
    results_path = os.path.join(path, 'results')
    filenames = []
    filenames.append(bibtex_name)
    bibname = bibtex_name.split('.')[0]
    filenames.append(bibname + "_log.txt")
    filenames.append(bibname + "_abstract.tex")
    filenames.append(bibname + "_latex.tex")
    #move files to ./results
    for file in filenames:
        shutil.move(file, results_path)
    #copy nips.sty
    shutil.copy('nips_2018.sty', results_path)

def make_latex(bibtex_name, path = None):
    if not path:
        path = './'
    latex_init = 'latex_init.tex'
    latex_file = bibtex_name.split('.')[0]+"_latex.tex" #output file
    abstract_file = bibtex_name.split('.')[0]+"_abstract.tex" #input file
    
    #first: copy latex_init
    with open(latex_init) as f:
        with open(latex_file, "w") as f1:
            for line in f:
                f1.write(line) 
    
    #second: copy abstracts into latex_file
    with open(abstract_file) as f:
        with open(latex_file, "a+") as f1:
            for line in f:
                f1.write(line) 
    
    #third: write references section
    with open(latex_file, "a+") as f:
        f.write("\\medskip \n")
        f.write("\\small \n")
        f.write("\\bibliographystyle{apalike} \n")
        f.write("\\bibliography{"+bibtex_name.split('.')[0] +"} \n")
        f.write("\\end{document} \n")

    



