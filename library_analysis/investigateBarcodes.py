import pickle

pickle_path = 'data/asyn_consensus_barcode_dictionary_180404.pkl'

with open(pickle_path, 'rb') as handle:
    barcode_dict = pickle.load(handle)

for key, val in barcode_dict.items():
    print(key + '\t' + str(val))

print(len(barcode_dict))
