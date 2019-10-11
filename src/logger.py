import re
import os
from os import listdir
from os.path import isfile, join

def log_bib(bibtex_name, paper_ref, status, path = None):
    if not path:
        path = './'
    biblog = bibtex_name.split('.')[0]+'_log.txt'
    blog = open(biblog,"a+")
    lines = blog.readlines()
    refs = []
    for line in lines:
        ref = line.split(',')[0]
        refs.append(ref)
    if refs.count(paper_ref) != 0:
        print("Paper already logged")
    else:
        line_to_log = paper_ref+","+status+"\n"
        blog.write(line_to_log)

def check_ref(bibtex_name, paper_ref, path = None):
    if not path:
        path = './'
    biblog = bibtex_name.split('.')[0]+'_log.txt'
    blog = open(biblog,"r")
    lines = blog.readlines()
    add_new = True
    for line in lines:
            ref = line.split(',')[0]
            if ref == paper_ref:
                add_new = False
    return add_new

def show_logs(bibtex_name, path = None):
    if not path:
        path = './'
    biblog = bibtex_name.split('.')[0]+'_log.txt'
    blog = open(biblog,"r")
    lines = blog.readlines()
    for line in lines:
        line = line.split(',')
        ref = line[0]
        status = line[1]#.split('\n')[0]
        print("Ref: ",ref, "Status:",status)    

