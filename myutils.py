import pandas as pd
import numpy as np
import os


def folderparser(foldername):
    '''
    makes sure a folder exists and if not makes it
    returns a bool for folder
    '''
    if os.path.exists(foldername):
        return foldername
    else:
        old = os.getcwd()
        os.chdir(os.path.dirname(foldername))
        os.system('mkdir %s' % (os.path.basename(foldername)))
        os.chdir(old)
        return foldername
    
def getpathway(filename):
    """
    absolute path
    pathway file format is pathway name and pathway gene id(two columns)
    """
    if filename.endswith('txt'):
        return pd.read_table(filename)
    elif filename.endswith('csv'):
        return pd.read_csv(filename)
    elif filename.endswith('xlsx'):
        return pd.read_excel(filename)
    else:
        raise 'pathway file format error!'
        
def get_gene_info(filename=None):
    """
    gene_information file include two columns,gene id and gene symbol
    """
    if filename:
        if filename.endswith('txt'):
            return pd.read_table(filename)
        elif filename.endswith('csv'):
            return pd.read_csv(filename)
        elif filename.endswith('xlsx'):
            return pd.read_excel(filename)
        else:
            raise 'gene information file format error!'
    else:
        gene_info = pd.read_excel('./data/Homo_sapiens.xlsx')
        return gene_info
    
def write(obj, filename):
    obj.to_excel(filename, index=False)
    
def getgid():
    gid = pd.unique(pd.read_excel('./data/background_gene.xlsx')['GeneID'])
    return gid
