import argparse
import glob
from Bio import SeqIO


parser = argparse.ArgumentParser(description='Merge and filter FASTA files.')
parser.add_argument('filenames', nargs='+', help='Input FASTA files')
parser.add_argument('--suffix', type=str, default="filtered", help='file suffix')

args = parser.parse_args()

filenames = []
for pattern in args.filenames:
    filenames.extend(glob.glob(pattern))

print(filenames)


def filter_common_fasta_files(filenames):
    
    common_ids = set()
    for filename in filenames:
        print(filename)
        # Read the file
        with open(filename, 'r') as file:
            current_ids = set()
               
            for record in SeqIO.parse(file, 'fasta'):
                current_id = record.id
                current_ids.add(current_id)
            
            if common_ids:
                common_ids.intersection_update(current_ids)
            else:
                common_ids = current_ids
            
    common_ids = list(common_ids)
    print(common_ids)
    
    for filename in filenames:
        with open(filename, 'r') as file:
           
            current_sequences = {}
            for record in SeqIO.parse(file, 'fasta'):
                current_id = record.id
                if record.id in common_ids:
                    current_sequences[current_id] = record
                
            index_map = {v: i for i, v in enumerate(common_ids)}
            print("index map", (index_map))
            current_sequences = dict(sorted(current_sequences.items(), key=lambda pair: index_map[pair[0]]))
                
            SeqIO.write(current_sequences.values(), f'{filename}_{args.suffix}', "fasta")
                    

filter_common_fasta_files(filenames)