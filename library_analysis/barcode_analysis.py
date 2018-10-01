# parse the Index file, produce a dataframe consisting of read_pair (Index column) and barcode_sequence

from Bio import SeqIO
import pandas as pd

with open('Undetermined_S0_L001_I1_001.fastq') as fastq_file:
    identifier = []
    barcode = []
    for seq_record in SeqIO.parse(fastq_file, 'fastq'):
        identifier.append(seq_record.id[-9:])
        barcode.append(str(seq_record.seq))

s1 = pd.Series(identifier, name='read_pair')
s2 = pd.Series(barcode, name='barcode_sequence')

Index_df = pd.DataFrame(dict(read_pair=s1, barcode_sequence=s2)).set_index(['read_pair'])

# remove # in line 19 to display dataframe

#df = Index_df

# to determine how many barcodes map to the same variant (N = 1650765)

pd.concat(g for _, g in df.groupby("read_pair") if len(g) > 1)

# to determine how many barcodes are repeated in the library (N = 4,111,171)

pd.concat(g for _, g in df.groupby("barcode_sequence") if len(g) > 1)
