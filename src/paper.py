from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import re
import datetime

class Paper:
    def __init__(self, code, bibtex_name, source = 'arxiv', url = None):
        self.code = code
        self.source = source
        self.url = url
        self.bibtex_name = bibtex_name
        self.abstract_filename = bibtex_name.split('.')[0]+'_abstract.tex'
        
        #get soup
        if self.source == 'arxiv':
            self.url = 'https://arxiv.org/abs/'+self.code
        headers = requests.utils.default_headers()
        req = requests.get(self.url, headers)
        self.soup = BeautifulSoup(req.content, 'html.parser')
        
        #get bib fields
        self.author = self.get_authors()
        self.title = self.get_title()
        self.year, self.month = self.get_date()
        self.url = self.get_url()
        self.abstract = self.get_abstract()
        self.comments = self.get_comment_v2()
        
        self.soup.clear()

    def print_soup(self):
        print(self.soup.prettify())

    def get_authors(self):
        field = "citation_author"
        response = self.soup.find_all("meta", {"name":field})
        authors = []
        if len(response)>1:
            for i, field in enumerate(response):
                author = str(response[i]).split("content=")[1].split(" name")[0].split("\"")[1]
                authors.append(author)
            
            authors_formatted = []
            for author in authors:
                name = author.split(",")[1]
                surname = author.split(",")[0]
                authors_formatted.append(name+" "+surname)

            authors_=''
            for i in range(len(authors_formatted)-1):
                authors_ += authors_formatted[i]+" and"
            authors = authors_ + authors_formatted[len(authors_formatted)-1]

        else:
            authors.append(self.soup.find("meta", {"name":field}).get('content')) 
        return authors

    def get_title(self):
        return self.soup.find("meta", property="og:title").get('content')

    def get_date(self):
        field = "citation_date"
        date = self.soup.find("meta", {"name":field}).get('content')
        date = date.split("/")
        date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))

        year = date.year
        month = date.strftime("%B")
        return year, month

    def get_url(self):
        field = "citation_pdf_url"
        return self.soup.find("meta", {"name":field}).get('content')

    def get_abstract(self):
        return self.soup.find("meta", property="og:description").get('content').replace("\n", " ")

    def get_comment_v1(self):
        tds = self.soup.find_all('td')
        comment = None
        for td in tds:
            if str(td).find('mathjax') != -1:
                comment = str(td).split('>')[1].split('<')[0]
        return comment

    def get_comment_v2(self):
        return str(self.soup.find_all('td')[1]).split('>')[1].split('<')[0]
    
    def print_bib(self, ref):
        print("@article{"+ref+",")
        #authors ----------
        print("author = {",  self.author,"},")
        #title ----------
        print("title = {", self.title,"},")
        #year ----------
        print("year = {", self.year,"},")
        #month ----------
        print("month = {", self.month,"},")
        #url ----------
        print("notes = {", self.comments,"},")
        #url ----------
        print("url = {", self.url,"},")
        #-----------
        print("}")
        
    def add_bib(self, ref):
        with open(self.bibtex_name,"a+") as b:
            b.write("\n")
            b.write("\n")
            line = "@article{"+ref+","+"\n"
            b.write(line)
            #authors ----------
            line = "author = {"+self.author+"},"+"\n"
            b.write(line)
            #title ----------
            line = "title = {"+self.title+"},"+"\n"
            b.write(line)
            #year ----------
            line = "year = {"+str(self.year)+"},"+"\n"
            b.write(line)
            #month ----------
            line = "month = {"+self.month+"},"+"\n"
            b.write(line)
            #notes ----------
            line = "notes = {"+self.comments+"},"+"\n"
            b.write(line)
            #journal ----------
            line = "journal = { arXiv preprint arXiv:"+self.code+"},"+"\n"
            b.write(line)
            #url ----------
            line = "url = {"+self.url+"},"+"\n"
            b.write(line)
            #-----------            
            b.write("} \n")
            b.write("\n")
            b.close()
    
    def add_abstract(self, ref):
        with open(self.abstract_filename,"a+") as abs:
            abs.write("\n")
            abs.write("\n")
            line = "\\subsection{"+self.title+ " (\\cite{"+ref+"})} \n"
            abs.write(line)
            if self.comments is not '\n':
                line = "\\textit{Notes}: "+self.comments + "\n"
                abs.write(line)
                abs.write('\\\ \n')
                abs.write('\\\ \n')
            abs.write("\\textbf{Abstract}:")
            abs.write(self.abstract)
            abs.write('\n')
            abs.write('\\\ \n')
            abs.write('\\\ \n')
            abs.write('\\textbf{\\textit{Comments and Discussion}}: \\\\')
            abs.write('\\bigskip \n')
            abs.write('\\bigskip \n')
            abs.write('\\bigskip \n')
