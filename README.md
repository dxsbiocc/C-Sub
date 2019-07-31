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

## parameter:
### required flags
-i: input file<br>
require:<br>
1.maf folder:<br>
  ..MANIFEST.txt<br>
  ..TCGA-xx-xxxx-01.maf.txt<br>
  ..TCGA-xx-xxxx-01.maf.txt<br>
  ...<br>
2.excel file:<br>
  two column, column 1 is sample ID, column 2 is mutation gene id<br>
-o: output file<br>
### optional flags<br>
-a: pathway and sub-pathway separated, input the pathway result to extract sub-pathway.<br>
-c: The sub-pathway minimum coverage ratio, default=0.6.<br>
-f: the cutoff FDR, default=0.05<br>
-g: gene information file, gene id and gene symbol,default=Homo_sapiens.xlsx, in directory 'data'.<br>
-l: sub-pathway minimum number of nodes, default=3<br>
-m: exeract geneid or symbol from mutation maf file(default=0, extract geneid).<br>
-n: random times<br>
-p: KEGG human normal pathway filename(absolute path), default=pathway_information.xlsx, in directory 'data'.<br>
-s: The maximum number of interval genes allowed between sub-pathway genes, default=1.<br>
