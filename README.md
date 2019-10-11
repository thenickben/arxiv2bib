[//]: # (Image References)

[logo]: https://github.com/pytrainai/pearl/blob/master/assets/logo.png

# ArXiv2Bib: Automatic generation of .bib files and .tex file with abstracts and citations!

## PyTrain team

![logo]


### Getting Started

1. Clone this repo and install all the requirements 

2. Download papers (pdf format) from ArXiv and (if possible, it also works fine otherwise but higher running time due pdf parsing) save them as REF.XXXX.YYYY, where REF is your custom reference name, and XXXX.YYYYY is the ArXiv code.

3. Run 

```
>> python run.py -p 'your/folder/path'
```

where `'your/folder/path'` is the path containing the pdfs.

4. Find the results in ./results folder. Also, if for any reason (e.g. the pdf wasn't downloaded from ArXiv) the pdf cannot be added to .bib file, you'll see this in the log file and also in the "failed" files folder.

### Roadmap

Next versions are planned to include:

 - setup
 - docker
 - other sources than ArXiv, e.g. NIPS, ICML, etc


### Collaboration and cites

You are more than welcome to colaborate! Please feel free to reach me out at pytrainteam@gmail.com. If you modify this code or use it don't forget to cite ;)
