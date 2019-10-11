import arxivbib as bib
import os
import shutil
import argparse

def generate_all(path): 
    root = path
    done_path = os.path.join(root, 'done')
    failed_path = os.path.join(root, 'failed')
    results_path = os.path.join(root, 'results')
    if not os.path.isdir(done_path): os.mkdir(done_path)
    if not os.path.isdir(failed_path): os.mkdir(failed_path)
    if not os.path.isdir(results_path): os.mkdir(results_path)

    bib_name = root.split('/')[len(root.split('/'))-1]+".bib"
    bib.make_files(bib_name, root)
    bib.add_papers_from_path(bib_name, root)
    bib.make_latex(bib_name, root)
    bib.move_files(bib_name, root)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-p', '--path', default = "./", help='path with pdfs')
    args = parser.parse_args()
    if args.path == "./":
        path = os.getcwd()
    else:
        path = args.path
    generate_all(path)

