from os import chdir, getcwd, listdir, path
from lxml.html import fromstring
import pandas as pd
import numpy as np
import requests
import time


def select_no_cancer_pathway():
    """
    extract KEGG pathway from website http://www.genome.jp/kegg/pathway.html except cancer relate pathway
    """
    url = 'http://www.genome.jp/kegg/pathway.html'
    r = requests.get(url)
    tree = fromstring(r.text.encode())
    B = [b for b in tree.cssselect('b') if b.text[0].isdigit() and b.text[2].isdigit()]
    pathway_name = []
    for b in B:
        if float(b.text[:3]) < 6 or float(b.text[:3]) > 7:
            div = b.getnext()
            pathway_name.extend([a.text for a in div.cssselect('a')])
    return pd.DataFrame(pathway_name, columns=['pathway name'])

def select_normal_pathway_gene():
    """
    use KEGG API extract normal pathway info, include pathway name and pathway gene
    """
    url = 'http://rest.kegg.jp/link/hsa/pathway'
    r = requests.get(url)
    text = r.text.replace('path:','').replace('hsa:','').strip()
    pathway = [[line.split('\t')[0], int(line.split('\t')[1])] for line in text.split('\n')]
    pathway_gene = pd.DataFrame(pathway, columns=['hsa','gene'])
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    pathway_name = select_no_cancer_pathway()
    hsa_pwn = select_human_pathway()
    hsa_pathway_name = pd.merge(hsa_pwn, pathway_name, on='pathway name')
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    a = pd.merge(hsa_pathway_name, pathway_gene, on='hsa')
    normal_pathway_gene = a.drop('hsa', axis=1)
    return normal_pathway_gene

def select_pathway_info(pid, mut=None):
    url = 'http://rest.kegg.jp/get/{}/kgml'.format(pid)
    n = 1
    while 1:
        try:
            r = requests.get(url,timeout=10)
            time.sleep(1)
        except:
            print('Pathway ' + str(pid) + ' Reconnection! n = ' + str(n))
            n = n + 1
            if n > 10:
                break
        else:
            break
    tree = fromstring(r.text)
    if isinstance(mut, pd.DataFrame):
        gid = pd.unique(mut['Mutation Gene'])
        entry = {int(e.get('id')) : [int(g) for g in e.get('name').replace('hsa:','').split() if int(g) in gid] 
                 for e in tree.cssselect('entry[type=gene]')}
    else:
        entry = {int(e.get('id')) : [int(g) for g in e.get('name').replace('hsa:','').split()] 
                 for e in tree.cssselect('entry[type=gene]')}
    relation = {(int(r.get('entry1')),int(r.get('entry2'))) : ','.join([i.get('name') for i in r.cssselect('subtype')]) for r in 
                tree.cssselect('relation') if int(r.get('entry1')) in entry.keys() and int(r.get('entry2')) in entry.keys()}
    return entry, relation
    
def select_mutation_gene(path1, symbol=0):
    old_path = getcwd()
    mutgene = []
    if path.isfile(path1):
        Mutation_Gene = pd.read_excel(path1)
    else:
        if symbol:
            #gi = pd.read_excel(old_path + '/data/Homo_sapiens.xlsx')
            gi = pd.read_excel('./data/Homo_sapiens.xlsx')
            chdir(path1)
            for file in listdir()[1:]: 
                gene_info = gi.set_index('Symbol')
                d = pd.read_table(file, sep='\t',encoding='utf-8')
                d = d.iloc[np.where(d.Variant_Classification != 'Silent')]
                g = gene_info.loc[d['Hugo_Symbol']]['GeneID'].dropna().values
                s = [file.split('.')[0]]*len(g)
                p = pd.DataFrame(list(zip(s,g)))
                mutgene.append(p)
        else:
            chdir(path1)
            for file in listdir()[1:]:
                d = pd.read_table(file, sep='\t',encoding='utf-8')
                g = pd.DataFrame(list(d.loc[(d.Variant_Classification != 'Silent') & (d.Entrez_Gene_Id != 0), 
                                                              'Entrez_Gene_Id'])).dropna()
                s = pd.DataFrame([file.split('.')[0]]*len(g.index))
                p = pd.concat([s,g], axis=1, join_axes=[s.index])
                mutgene.append(p)
        Mutation_Gene = pd.concat(mutgene)
        Mutation_Gene.columns = ['Sample','Mutation Gene']
        chdir(old_path)
    return Mutation_Gene

def select_human_pathway():
    """
    extract all human pathway from KEGG. 
    DataFrame format is: hsaXXXXX, pathway name
    """
    url = 'http://rest.kegg.jp/list/pathway/hsa'
    r = requests.get(url)
    text = r.text.replace('path:','').replace(' - Homo sapiens (human)','').strip()
    pathway = [line.split('\t') for line in text.split('\n')]
    hsa_pwn = pd.DataFrame(pathway, columns=['hsa','pathway name'])
    return hsa_pwn
