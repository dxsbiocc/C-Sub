# C-Sub
the candidate Sub-Pathway method


## packages：

numpy、pandas、networkx、xlrd、scipy、lxml、cssselect、requests、openpyxl

## run：

```
cd C-Sub/

# common pathway and sub-pathway analysis
python C-Subs.py -i input None -o result.xlsx

# subtype-specific pathway and sub-pathway analysis
python C-Subs.py -i subtype1 subtype2 -o result.xlsx
```

##parameter:
### required flags
-i: input file
require:
1.maf folder:
  ..MANIFEST.txt
  ..TCGA-xx-xxxx-01.maf.txt
  ..TCGA-xx-xxxx-01.maf.txt
  ...
2.excel file:
  two column, column 1 is sample ID, column 2 is mutation gene id
-o: output file
### optional flags
-a: pathway and sub-pathway separated, input the pathway result to extract sub-pathway.
-c: The sub-pathway minimum coverage ratio, default=0.6.
-f: the cutoff FDR, default=0.05
-g: gene information file, gene id and gene symbol,default=Homo_sapiens.xlsx, in directory 'data'.
-l: sub-pathway minimum number of nodes, default=3
-m: exeract geneid or symbol from mutation maf file(default=0, extract geneid).
-n: random times
-p: KEGG human normal pathway filename(absolute path), default=pathway_information.xlsx, in directory 'data'.
-s: The maximum number of interval genes allowed between sub-pathway genes, default=1.
