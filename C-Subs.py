import pandas as pd
import myalgorithm
import SubPathway
import myselect
import myutils
import time
import os


def main():
    
    from optparse import OptionParser
    usage = "usage: %prog [options] -i [INPUT_MAF_FILE_FOLDER] -o [OUTPUT_FOLDER] [OPTIONAL_FLAGS]"
    parser = OptionParser(usage = usage)
    # required flags
    parser.add_option("-i","--i", dest="input",nargs = 2, default=None,
                      help = "Enter mutation maf files path,if cancer vs normal the second arg is None.")
    parser.add_option("-o","--out", dest="out",nargs = 1, default=None,
                      help = "Enter an output folder.")
    # optional flags
    parser.add_option("-f","--fdr", dest="fdr",nargs = 1, default=0.05,
                      help = "FDR cut off")
    parser.add_option("-s","--step", dest="step",nargs = 1, default=1,
                      help = "The maximum number of interval genes allowed between Sub-pathway genes.")
    parser.add_option("-c","--minsize", dest="minsize",nargs = 1, default=3,
                      help = "Sub-pathway minimum number of nodes.")
    parser.add_option("-p","--pathway", dest="pathway",nargs = 1, default=None,
                      help = "KEGG human normal pathway filename(absolute path).")
    parser.add_option("-g","--gene", dest="gene",nargs = 1, default=None,
                      help = "gene information file, gene id and gene symbol,default is NCBI human_gene_info.")
    parser.add_option("-n","--nperm", dest="nperm",nargs = 1, default=1000,
                      help = "random times")
    parser.add_option("-m","--symbol", dest="symbol",nargs = 1, default=0,
                      help = "input 1:mutation maf file geneid is 0 but have symbol.")
    parser.add_option("-a","--sub", dest="sub",nargs = 1, default=None,
                      help = "Determine whether subpath extraction is performed separately.File absolute path.")
    # RETRIEVING FLAGS
    (options,args) = parser.parse_args()
    
    if not options.input or not options.out:
        print('hi there')
        parser.print_help()
        exit()
    # making the out folder if it doesn't exist
    outfolder = myutils.folderparser(options.out)
    
    #get pathway information
    if not options.pathway:
        pathway_info = myselect.select_normal_pathway_gene()
    else:
        pathway_info = myutils.getpathway(options.pathway)
    
    # get sample mutation infromation
    mut = []
    for t in options.input:
        if t != 'None':
            mut.append(myselect.select_mutation_gene(t, int(options.symbol)))
    # get gene information
    if not options.gene:
        gene_info = myutils.get_gene_info()
    else:
        gene_info = myutils.get_gene_info(options.gene)
    # run
    gid = myutils.getgid()
    hsa = myselect.select_human_pathway().set_index('pathway name')
    begin = """
    **********************************************************************
    *                               BEGIN                                *
    **********************************************************************
    """
    end = """
    **********************************************************************
    *                                END                                 *
    **********************************************************************
    """
    if len(mut) == 1:
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #                                             高覆盖通路                                              #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if not options.sub:
            tb = time.time()
            print('-' * 10, 'Non-Random Mutation-High-Cover Pathway', '-' * 10)
            print(begin)
            sig_pathway = myalgorithm.RSMP(mut[0], pathway_info, gid, int(options.nperm), float(options.fdr))
            myutils.write(sig_pathway, os.path.join(outfolder, 'sig_pathway.xlsx'))
            te = time.time()
            print('Spend %.2f minute!' %((te-tb)/60))
            print(end)
        else:
            sig_pathway = pd.read_excel(options.sub)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #                                        common sub-pathways                                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        te = time.time()
        print('-' * 10, 'Mutation-High-Cover Sub-Pathway', '-' * 10)
        print(begin)
        Sub_Pathway = SubPathway.HighCoverSub(mut[0], gene_info, sig_pathway, hsa, outfolder, int(options.step), int(options.minsize))
        myutils.write(Sub_Pathway, os.path.join(outfolder, 'Sub_Pathway.xlsx'))
        print('Spend %.2f minute' %((time.time()-te)/60))
        print(end)
    else:
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #                                       subtype-specific pathways                                     #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if not options.sub:
            tb = time.time()
            print('-' * 15, 'Subtype Specificity Pathway', '-' * 15)
            print(begin)
            sig_pathway = myalgorithm.TSDP(mut[0], mut[1], pathway_info, cut_off=float(options.fdr))
            myutils.write(sig_pathway, os.path.join(outfolder, 'sig_pathway.xlsx'))
            te = time.time()
            print('Spend %.2f minute!' %((te-tb)/60))
            print(end)
        else:
            sig_pathway = pd.read_excel(options.sub)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #                                      subtype-specific sub-pathways                                  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        te = time.time()
        print('-' * 15, 'Subtype Specificity Sub-Pathway', '-' * 15)
        print(begin)
        Specific_Sub_Pathway = SubPathway.DistinctSub(mut, gene_info, sig_pathway, hsa, outfolder, int(options.step), int(options.minsize))
        myutils.write(Specific_Sub_Pathway, os.path.join(outfolder, 'Specific_Sub_Pathway.xlsx'))
        print('Spend %.2f minute' %((time.time()-te)/60))
        print(end)
    
if __name__ == '__main__':
    main()
