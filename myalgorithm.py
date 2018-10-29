import pandas as pd
import numpy as np


def RSMP(subtype, pathway_gene, gid, nperm=1000, cut_off=0.05):
    """
    Random Significant Mutation Pathway
    subtype : the cancer mutation information include Sample, Mutation gene(Format:pandas DataFrame)
    pathway_gene : KEGG pathway information include pathway name and pathway gene(Format:pandas DataFrame)
    gid : Format: np.array
    nperm : random times
    cut_off : control FDR values less than cut_off, default value is 0.05
    """
    pg = pathway_gene.groupby('pathway name').agg(lambda x: [int(i) for i in x])
    mg = subtype.groupby('Sample').agg(lambda x: [int(i) for i in x])
    T = len(mg)
    MMF = np.zeros((nperm+1,T), dtype=int) # Mutation Frequence Matrix
    MPI = [] # Mutation Pathway Information: pathway, pathway real mutation sample number ,pathway random mutation sample number
    P = [] # p value
    for p in pg.index:
        ppg = pg.loc[p].gene # per pathway gene
        for j, m in enumerate(mg.index):
            smg = mg.loc[m]['Mutation Gene'] # per sample mutation gene
            lsmg = len(smg)
            MMF[0,j] = 1 if set(ppg) & set(smg) else 0
            temp = np.random.randint(len(gid)-1, size=(nperm,lsmg)).reshape(nperm*lsmg)
            rmg = gid[np.ix_(temp)].reshape(nperm,lsmg) # random mutation gene
            MMF[1:,j] = [1 if set(rmg[i,]) & set(ppg) else 0 for i in range(nperm)]
        MF = MMF.sum(1) # Pathway Mutation Frequence
        P.append(len(MF[np.where(MF > MF[0])]) / nperm)
        MPI.append((p, len(ppg), MF[0], np.mean(MF[1:]), MF[0]-np.mean(MF[1:]), MF[0]/T))
    FDR = mafdr(P)
    sig_pathway = [(*MPI[i], f) for i, f in enumerate(FDR) if f <= cut_off and MPI[i][2] != 0]
    sig_pathway = pd.DataFrame(sig_pathway, columns=['Pathway name','gene','mutation number','random mutation number',
                                                     'mutation difference','mutation rate','fdr'])
    return sig_pathway.sort_values(by='mutation difference', ascending=False)

def TSDP(subtype1, subtype2, pathway_info, cut_off=0.05):
    """
    Two Subtype Different Pathway
    calculate significant difference pathway in two different types of cancer
    subtype1 : the first cancer type mutation pandas DataFrame
    subtype2 : the second cancer type mutation pandas DataFrame
    pathway_info : the KEGG pathway information pandas DataFrame,include two columns, the first one is pathway name and the 
                   second one is pathway genes
    cut_off : control FDR values less than cut_off, default value is 0.05
    """
    from scipy.stats import fisher_exact
    a = len(subtype1['Sample'].drop_duplicates()) #the number of subtype1 sample 
    s = len(subtype2['Sample'].drop_duplicates()) #the number of subtype2 sample 
    ad = subtype1.set_index('Mutation Gene')
    sc = subtype2.set_index('Mutation Gene')
    pg = pathway_info.groupby('pathway name').agg(lambda x: [int(i) for i in x])
    pvalue = []
    info = []
    for i in range(pg.shape[0]):
        try:
            ma = len(ad.loc[pg.iloc[i]['gene']].dropna()['Sample'].drop_duplicates())
        except KeyError as e:
            ma = 0
        try:
            ms = len(sc.loc[pg.iloc[i]['gene']].dropna()['Sample'].drop_duplicates())
        except KeyError as e:
            ms = 0
        info.append((ma, ma/a, ms, ms/s, abs(ma/a - ms/s)))
        oddsratio, p = fisher_exact([[a-ma,s-ms],[ma,ms]])
        pvalue.append(p)
    fdr = mafdr(pvalue, correction_type = "Benjamini-Hochberg")
    sig_pathway = [(pg.iloc[i].name, len(pg.iloc[i]['gene']), f, *info[i]) for i, f in enumerate(fdr) if f <= cut_off]
    sig_pathway = pd.DataFrame(sig_pathway, columns=['Pathway name','gene', 'fdr', 'number1',
                                                     'frequence1','number2','frequence2', 'frequency difference'])
    return sig_pathway.sort_values(by='frequency difference', ascending=False)

def mafdr(pvalues, correction_type = "Benjamini-Hochberg"):                
    """
    multiple hypothesis test false positive rate(FDR) p value correction
    mafdr([0.0, 0.01, 0.029, 0.03, 0.031, 0.05, 0.069, 0.07, 0.071, 0.09, 0.1]) 
    """
    from numpy import array, empty                                                                        
    pvalues = array(pvalues) 
    n = pvalues.shape[0]                                                                        
    new_pvalues = empty(n)
    if correction_type == "Bonferroni":                                                                   
        new_pvalues = n * pvalues
    elif correction_type == "Bonferroni-Holm":                                                            
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]                                      
        values.sort()
        for rank, vals in enumerate(values):                                                              
            pvalue, i = vals
            new_pvalues[i] = (n-rank) * pvalue                                                            
    elif correction_type == "Benjamini-Hochberg":                                                         
        values = [ (pvalue, i) for i, pvalue in enumerate(pvalues) ]                                      
        values.sort()
        values.reverse()                                                                                  
        new_values = []
        for i, vals in enumerate(values):                                                                 
            rank = n - i
            pvalue, index = vals                                                                          
            new_values.append((n/rank) * pvalue)                                                          
        for i in range(0, int(n)-1):  
            if new_values[i] < new_values[i+1]:                                                           
                new_values[i+1] = new_values[i]                                                           
        for i, vals in enumerate(values):
            pvalue, index = vals
            new_pvalues[index] = new_values[i]
    else:
        print('correction type error!')
    return new_pvalues
