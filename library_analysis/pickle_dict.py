import pickle
import numpy as np
from matplotlib import use
use('Agg')
from matplotlib import pyplot as plt
from multiprocessing import Pool
from functools import partial
import csv

#Functions used
def loadPickle(picklePath, printDict=True):
    with open(picklePath, 'rb') as handle:
        barcodeDict = pickle.load(handle)
    if printDict:
        for keys,values in barcodeDict.items():
            print(keys, values)
    return barcodeDict

def hamming_dist(main_list,sub_list):
    distances = []

    while len(sub_list) != 0:
        s1 = sub_list.pop()
        for s2 in main_list:
            if len(s1) != len(s2):
                raise ValueError('Undefined for sequences of unequal length.')
            if s1 is s2:
                continue
            distances.append(sum(nue1 != nue2 for nue1, nue2 in zip(s1,s2)))

    return(distances)

def parralellize_me_capt(full_list,split_num):
    #Take a list of arbitrary length and some given split number.
    #If the split number is stupid, throw a fit
    #----
    #If the list length is not divisable by the split num, add null values
    #until it does...
    #----
    #Return a split list
    list_len = len(full_list)

    #Sanity Check
    if list_len <= split_num:
        raise ValueError('Split number is higher than number of elements to split!')

    #List fill in to make divisable by split

    while list_len%split_num != 0:
        full_list.append(None)
        list_len = list_len = len(full_list)

    #Split and return listsss
    split_lists = []
    block_size = int(list_len/split_num)
    for i in range(0,list_len,block_size):
        block = full_list[i:i+block_size]
        split_lists.append(block)

    final_list = split_lists.pop()
    split_lists.append([x for x in final_list if x is not None])

    return split_lists, block_size

def splice_pickle_file(picklePath_temp,test_length):
    #This section was used to create a 'slice' of 10 entries from the original dictionary
    #Wrote to a new smaller pickle file called test.picklePath
    plasmidDict = loadPickle(picklePath_temp, printDict=False)

    i = 0
    test_dict = {}
    for key, value in plasmidDict.items():
        test_dict[key] = value
        if i == test_length-1:
            break
        i += 1

    with open(r"test.pickle", "wb") as output_file:
        pickle.dump(test_dict, output_file)

    return 'test.pickle'


if __name__ == '__main__':
    #Load first slice file to reduce problem for local calculations

    picklePath = 'asyn_consensus_barcode_dictionary_180404.pkl'

    #Testing controls
    split_length = 100
    sub_proccess_num = 45

    #Spliting function for testing
    #picklePath = splice_pickle_file(picklePath,split_length)

    plasmidDict = loadPickle(picklePath, printDict=False)

    #Sanity check
    print('Length of total list: ' + str(len(plasmidDict)))

    #Convert barcode keys to a to list
    sequences_all = list(plasmidDict.keys())
    barcode_distances = []
    #Break up into # sub-lists for parrallel processing!
    sub_lists, block_size = parralellize_me_capt(sequences_all,sub_proccess_num)
    sequences_all = [x for x in sequences_all if x is not None]
    print('Number of sub-lists: ' + str(len(sub_lists)))
    print('Length of sub-list 2: ' + str(len(sub_lists[1])))

    #Need to find a way to identify barcodes that are within a ceritan threshold barcode_distances
    #Maybe check each distance then record i,j values for later recall?

    #Parrallel calculations

    #Needs documentation!
    #print(sub_lists)
    #print(sequences_all)
    pool = Pool(sub_proccess_num)
    locked_func = partial(hamming_dist,sequences_all)
    split_results = pool.map(locked_func,sub_lists)
    #output = [p.get() for p in results]
    pool.close()
    pool.join()

    barcode_distances = [x for sub in split_results for x in sub]
    print('Results generated:' + str(len(barcode_distances)))
    print('---')
    #print('Saving results for plotting...')

    """
    with open('hamming_distances_test.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(barcode_distances)
    """




    #Plotting?
    #barcode_distances_filtered = list(filter(lambda x: x != 0, barcode_distances))
    print('Now binning results...')
    binz = range(0,max(barcode_distances))
    string = 'N=' + str(len(barcode_distances))
    plt.hist(barcode_distances,bins = binz,align='left',rwidth=0.75, density=True)
    plt.title(string)
    plt.xticks(binz)
    plt.xlabel('Hamming Distances')
    plt.ylabel('Density of Distance')
    plt.yscale('log')
    plt.savefig('test.png')
