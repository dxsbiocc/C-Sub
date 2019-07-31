from myselect import select_pathway_info
from scipy.stats import fisher_exact
from lxml.html import fromstring
from itertools import product
from os import path, mkdir
import networkx as nx
import pandas as pd
import numpy as np
import requests
import shutil
import time


def entry2gid(entry,relation):
    """
    transform KEGG pathway information to dataframe
    """
    _a = pd.DataFrame(list(relation.keys()))
    _r = set(_a[0]) | set(_a[1])
    _nodege = []
    for k in entry.keys():
        if entry.get(k) and k in _r:
            _nodege.extend(list(product([k], entry.get(k))))
    if _nodege:
        _nodege = pd.DataFrame(_nodege).set_index(0)
    else:
        _nodege = None
    return _nodege

def gene_mut_num(g, idx_mut, entry):
    """
    caculate the number of sample with gene g was mutation
    """
    try:
        _m = idx_mut.loc[entry.get(g)].drop_duplicates().count()['Sample']
    except:
        _m = 0
    return _m

def get_mut_freq(sub, gidx, _nodege):
    try:
        gmf = gidx.loc[_nodege.loc[sub][1]].drop_duplicates().count()['Sample']
    except:
        gmf = 0
    return gmf

def added_mut_freq(sub, k, gidx, _nodege):
    try:
        amf = gidx.loc[_nodege.loc[list(set(sub) | set([k]))][1]].drop_duplicates().count()['Sample']
    except:
        amf = 0
    return amf

def component(peculiar, subG):
    try:
        pec = peculiar.loc[list(subG.node)].dropna()
    except:
        pec = None
    return pec

def get_title(n, entry, to, itos, _node_mut_diff=None, gidx=None):
    if to == 'one':
        gs = ','.join([str(gid) + '(' + itos.loc[gid]['Symbol'] + ')' for gid in entry.get(n)])
        title = gs + '\nMutation Number: %s' % gene_mut_num(n, gidx, entry)
    else:
        try:
            gs = ','.join([str(gid) + '(' + itos.loc[gid]['Symbol'] + ')' for gid in entry.get(n)])
        except:
            gs = 'None'
        try:
            gnn = {'ad': _node_mut_diff.loc[n]['nm1'], 'sc': _node_mut_diff.loc[n]['nm2']}
        except:
            gnn = {'ad': 0, 'sc': 0}
        title = gs + '\nMutation Number: [%(ad)s,%(sc)s]' % gnn
    return title

def write_map_one(name, all_subpathway, gidx, relation, entry, itos, folder):
    sub_path = [i for s in all_subpathway for i in s]
    seed = [s[0] for s in all_subpathway]
    elements = {
        'nodes':[],
        'edges':[],
        'title':name
    }
    all_gene = set(pd.DataFrame(list(relation.keys()))[0]) | set(pd.DataFrame(list(relation.keys()))[1])
    for n in all_gene:
        node = {
            'data':{ 
                'id': str(n), 
                'type': 'Non-mutation', 
                'title': get_title(n, entry, 'one', itos, None, gidx)
            }
        }
        if entry.get(n):
            node['data']['type'] = 'Mutation'
        if n in sub_path:
            node['data']['type'] = 'SubPathway Member'
        if n in seed:
            node['data']['label'] = 'Seed'
        elements['nodes'].append(node)
    for s, t in relation.keys():
        edge = {
            'data': {'source': str(s), 'target':str(t), 'type': 'activation'}
        }
        if relation[(s, t)].find('inhibition') != -1:
            edge['data']['type'] = 'inhibition'
        elements['edges'].append(edge)
    network = path.join(folder, 'network')
    if not path.exists(network):
        mkdir(network)
    filename = network + '\\' + name.replace('/','1') + '.html'
    open(filename,'w').write(open('./data/template.html','r').read() % elements)
    
def SubPathwayOne(name, relation, mut, entry, gene_info, folder, step, minsize):
    itos = gene_info.set_index('GeneID') 
    gidx = mut.set_index('Mutation Gene')
    _ls = mut['Sample'].drop_duplicates().shape[0] #sample size
    _nodege = entry2gid(entry, relation)
    if not isinstance(_nodege, pd.DataFrame): return None
    G = nx.Graph()
    G.add_edges_from(relation.keys())
    all_subpathway = [] #sub-pathway entry id
    for subG in nx.connected_component_subgraphs(G):
        if len(subG.nodes()) > minsize and set(subG.node) & set(_nodege.index):
            _seed = _nodege.loc[list(subG.node)].dropna().groupby(by=0).apply(lambda x : gidx.loc[x[1]].drop_duplicates().count()).idxmax()['Sample']
            sub_path = [_seed]
            visited = [_seed]
            _mutfreq = gidx.loc[_nodege.loc[sub_path][1]].drop_duplicates().count()['Sample']
            _adj_node = {a:0 for a in list(subG.adj[_seed])}
            while 1:
                _addgmf = pd.DataFrame([(g,added_mut_freq(sub_path, g, gidx, _nodege))
                                        for g in _adj_node.keys()]).sort_values(by=1,ascending=False)
                for n in _addgmf.values[:,0]:
                    visited.append(n)
                    f = added_mut_freq(sub_path, n, gidx, _nodege)
                    if f > _mutfreq:
                        _adj_node[n] = 0
                        sub_path.append(n)
                        _mutfreq = f
                    else:
                        _adj_node[n] = _adj_node.get(n) + 1
                _temp_adj_node = {a: _adj_node.get(i) for i in dict(sorted(_adj_node.items(), key = lambda x : x[1], reverse=True)).keys() 
                                  for a in list(subG.adj[i]) if a not in visited and _adj_node.get(i) <= 1}
                _adj_node = _temp_adj_node
                if not _adj_node: break
            all_subpathway.append(sub_path)
    #plot
    if all_subpathway:
        write_map_one(name, all_subpathway, gidx, relation, entry, itos, folder)
    _tmg = _nodege[1].drop_duplicates().shape[0] #the total number of mutation gene
    _tmf = gidx.loc[_nodege[1]].drop_duplicates().count()['Sample']/_ls #the total mutation frequency
    _mg,_mf,_nmg = [],[],[]
    all_subpathway_info = []
    for sub_path in all_subpathway:
        _mg = list(itos.loc[_nodege.loc[sub_path][1].dropna()]['Symbol']) #sub-pathway mutaion gene
        _mf = gidx.loc[_nodege.loc[sub_path][1]].drop_duplicates().count()['Sample']/_ls #the mutation frequency of sub-pathway
        _nmg = len(_mg) #the number of sub-pathway gene
        all_subpathway_info.append([_nmg, _mf, _tmg, _tmf, _mg])
    return all_subpathway_info

def write_map_two(name, ad_path, sc_path, _node_mut_diff, relation, entry, itos, folder):
    if ad_path:
        adpath = [i for a in ad_path for i in a]
        adseed = [a[0] for a in ad_path]
    else:
        adpath = []
        adseed = []
    if sc_path:
        scpath = [i for s in sc_path for i in s]
        scseed = [s[0] for s in sc_path]
    else:
        scpath = []
        scseed = []
    elements = {
        'nodes':[],
        'edges':[],
        'title':name
    }
    all_mut_gene = set(pd.DataFrame(list(relation.keys()))[0]) | set(pd.DataFrame(list(relation.keys()))[1])
    for n in all_mut_gene:
        node = {
            'data':{ 
                'id': str(n),
                'type': 'Non-mutation', 
                'title': get_title(n, entry, 'two', itos, _node_mut_diff)
            }
        }
        if entry.get(n):
            node['data']['type'] = 'Mutation'
        if n in adpath:
            node['data']['type'] = 'Type1 SubPathway Member'
        if n in scpath:
            node['data']['type'] = 'Type2 SubPathway Member'
        if n in adseed:
            node['data']['label'] = 'Type1 Seed'
        if n in scseed:
            node['data']['label'] = 'Type2 Seed'
        elements['nodes'].append(node)
    for s, t in relation.keys():
        edge = {
            'data': {'source': str(s), 'target':str(t), 'type': 'activation'}
        }
        if relation[(s, t)].find('inhibition') != -1:
            edge['data']['type'] = 'inhibition'
        elements['edges'].append(edge)
    network = path.join(folder, 'network')
    if not path.exists(network):
        mkdir(network)
    filename = network + '\\' + name.replace('/','1') + '.html'
    open(filename,'w').write(open('./data/template.html','r').read() % elements)
    
def get_Subpathway_Node(peculiar_nodege, _nodege, gidx1, gidx2, G, subtype, step):
    _seed = peculiar_nodege['diff'].idxmax()
    _maxdiff = peculiar_nodege['diff'].max()
    sub = [_seed]
    visited = [_seed]
    _adj_node = {a:0 for a in list(G.adj[_seed])}
    if subtype == 1:
        order = lambda sub,g,gidx1,gidx2,_nodege: added_mut_freq(sub,g,gidx1,_nodege) - added_mut_freq(sub,g,gidx2,_nodege)
    else:
        order = lambda sub,g,gidx1,gidx2,_nodege: added_mut_freq(sub,g,gidx2,_nodege) - added_mut_freq(sub,g,gidx1,_nodege)
    while 1:
        _addgmf = pd.DataFrame([(g, order(sub,g,gidx1,gidx2,_nodege)) for g in _adj_node.keys()]).sort_values(by=1,ascending=False)
        for n in _addgmf[0]:
            visited.append(n)
            f = order(sub,n,gidx1,gidx2,_nodege)
            if f > _maxdiff:
                _adj_node[n] = 0
                sub.append(n)
                _maxdiff = f
            else:
                _adj_node[n] = _adj_node.get(n) + 1
        _temp_adj_node = {a: _adj_node.get(i) for i in dict(sorted(_adj_node.items(), key = lambda x : x[1], reverse=True)).keys()
                          for a in list(G.adj[i]) if a not in visited and _adj_node.get(i) <= step}
        _adj_node = _temp_adj_node
        if not _adj_node: break
    return sub

def SubPathwayTwo(name, relation, mut, entry, gene_info, folder, step, minsize):
    itos = gene_info.set_index('GeneID')
    gidx1 = mut[0].set_index('Mutation Gene')
    len1 = gidx1['Sample'].drop_duplicates().shape[0]
    gidx2 = mut[1].set_index('Mutation Gene')
    len2 = gidx2['Sample'].drop_duplicates().shape[0]
    _node_mut_diff = []
    for k in entry.keys():
        _mad = gene_mut_num(k, gidx1, entry)
        _msc = gene_mut_num(k, gidx2, entry)
        if _mad != 0 or _msc != 0:
            _node_mut_diff.append((k, _mad, _msc, _mad - _msc))
    _node_mut_diff = pd.DataFrame(_node_mut_diff, columns=['nid', 'nm1', 'nm2', 'diff']).set_index('nid')
    for k in list(entry.keys()):
        if k not in _node_mut_diff.index:
            entry.pop(k)
    ad_peculiar = _node_mut_diff.loc[_node_mut_diff['diff'] > 0,['diff']]
    sc_peculiar = _node_mut_diff.loc[_node_mut_diff['diff'] < 0,['diff']].apply(abs)
    G = nx.Graph()
    G.add_edges_from(relation.keys())
    _nodege = entry2gid(entry,relation)
    if not isinstance(_nodege, pd.DataFrame): return None, None
    SC_subpathway = []
    AD_subpathway = []
    AD_path = []
    SC_path = []
    for subG in nx.connected_component_subgraphs(G):
        if len(subG.nodes()) > minsize:
            ad_pec = component(ad_peculiar, subG)
            if isinstance(ad_pec,pd.DataFrame):
                adpath = get_Subpathway_Node(ad_pec, _nodege, gidx1, gidx2, subG, 1, step)
                _ad = get_mut_freq(adpath, gidx1, _nodege)
                _sc = get_mut_freq(adpath, gidx2, _nodege)
                _g = list(itos.loc[_nodege.loc[adpath][1].dropna()]['Symbol'])
                oddsratio, p = fisher_exact([[len1-_ad,len2-_sc],[_ad,_sc]])
                if p <= 0.05 and len(_g) >= minsize:
                    AD_path.append(adpath)
                    AD_subpathway.append([len(_g), int(_ad), _ad/len1, int(_sc), _sc/len2, abs(_ad/len1-_sc/len2), p, _g])
            sc_pec = component(sc_peculiar, subG)
            if isinstance(sc_pec,pd.DataFrame):
                scpath = get_Subpathway_Node(sc_pec, _nodege, gidx1, gidx2, subG, 2, step)
                _ad = get_mut_freq(scpath, gidx1, _nodege)
                _sc = get_mut_freq(scpath, gidx2, _nodege)
                oddsratio, p = fisher_exact([[len1-_ad,len2-_sc],[_ad,_sc]])
                _g = list(itos.loc[_nodege.loc[scpath][1].dropna()]['Symbol'])
                if p <= 0.05 and len(_g) >= minsize:
                    SC_path.append(scpath)
                    SC_subpathway.append([len(_g), int(_ad), _ad/len1, int(_sc), _sc/len2, abs(_ad/len1-_sc/len2), p, _g])
    if AD_path or SC_path:
        write_map_two(name, AD_path, SC_path, _node_mut_diff, relation, entry, itos, folder)
    return AD_subpathway, SC_subpathway

def post_filter(subg, gidx1, gidx2, stoi, len1, len2):
    gid = list(stoi.loc[subg]['GeneID'])
    gmn1 = gidx1.loc[gid].groupby(level=0).apply(lambda x : x.drop_duplicates().count())
    gmn2 = gidx2.loc[gid].groupby(level=0).apply(lambda x : x.drop_duplicates().count())
    gmn = pd.concat([gmn1,gmn2],join='inner',axis=1)
    gmn.columns=['S1','S2']
    mg = list(gmn.loc[gmn.apply(sum, axis=1) != 0].index)
    remain = set(mg) - {gmn.apply(lambda x: abs(x[0] - x[1]), axis=1).idxmax()}
    try:
        _ad = gidx1.loc[remain]['Sample'].drop_duplicates().count()
    except:
        _ad = 0
    try:
        _sc = gidx2.loc[remain]['Sample'].drop_duplicates().count()
    except:
        _sc = 0
    oddsratio, p = fisher_exact([[len1-_ad,len2-_sc],[_ad,_sc]])
    return mg, p

def HighCoverSub(mut, gene_info, sig_pathway, hsa, folder, step=1, minsize=3):
    if not path.exists(path.join(folder,'js')):
        shutil.copytree('./data/js/',path.join(folder,'js'))
    sub_pathway = []
    for i in sig_pathway.index:
        name = sig_pathway.loc[i][0]
        pid = hsa.loc[name]['hsa']
        entry, relation = select_pathway_info(pid, mut)
        if not relation: 
            print('Pathway ' + name + "\tNone interaction!")
            continue
        temp = SubPathwayOne(name, relation, mut, entry, gene_info, folder, step, minsize)
        if not isinstance(temp, list):
            print('Pathway ' + name + "\tNo Result!")
            continue
        for i,t in enumerate(temp):
            t.insert(0, name + "_" + str(i+1))
            sub_pathway.append(t)
        print(name)
    sub_pathway = pd.DataFrame(sub_pathway, columns=['subPathway Name', 'mutGene', 'mutFreq', 'all mutGene', 'totalFreq', 'Gene'])
    return sub_pathway.sort_values(by='mutFreq',ascending=False)

def DistinctSub(mut, gene_info, sig_pathway, hsa, folder, step=1, minsize=3):
    if not path.exists(path.join(folder,'js')):
        shutil.copytree('./data/js/',path.join(folder,'js'))
    stoi = gene_info.set_index('Symbol')
    itos = gene_info.set_index('GeneID')
    gidx1 = mut[0].set_index('Mutation Gene')
    gidx2 = mut[1].set_index('Mutation Gene')
    len1 = gidx1['Sample'].drop_duplicates().shape[0]
    len2 = gidx2['Sample'].drop_duplicates().shape[0]
    sub_pathway = []
    for i in sig_pathway.index:
        name = sig_pathway.loc[i][0]
        pid = hsa.loc[name]['hsa']
        entry, relation = select_pathway_info(pid)
        if not relation: continue
        tempA,tempB = SubPathwayTwo(name, relation, mut, entry, gene_info, folder, step, minsize)
        if not isinstance(tempA, list) and not isinstance(tempB, list):
            print('Pathway ' + name + "\tNo Result!")
            continue
        for i,ta in enumerate(tempA):
            ta.insert(0, name + '_subtype1_' + str(i+1))
            #ta[-1],p = post_filter(ta[-1], gidx1, gidx2, stoi, len1, len2)
            #ta.insert(-1,list(itos.loc[ta[-1]]['Symbol']))
            #if p < 0.05:
            sub_pathway.append(ta)
        for i,tb in enumerate(tempB):
            tb.insert(0, name + '_subtype2_' + str(i+1))
            #tb[-1],p = post_filter(tb[-1], gidx1, gidx2, stoi, len1, len2)
            #tb.insert(-1,list(itos.loc[tb[-1]]['Symbol']))
            #if p < 0.05:
            sub_pathway.append(tb)
        print(name)
    sub_pathway = pd.DataFrame(sub_pathway, columns=['Pathway Name', 'gene number', 'type1', 'freq1', 'type2', 'freq2', 'freq_diff', 'PValue','Symbol'])
    return sub_pathway.sort_values(by='freq_diff',ascending=False)
