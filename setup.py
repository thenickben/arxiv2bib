from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='arxiv2bib',
      version='1.0',
      description='Generates .bib and .tex files from pdf files in a folder',
      url='https://github.com/pytrainai',
      author='pytrainai',
      author_email='pytrainteam@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      license='MIT',
      zip_safe=False)