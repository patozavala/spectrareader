"""
An script to decode all files in USGS Spectral Library Version 7 Data.
"""
import os
import usgs_lib7 as usgs_datasets


dataset_path = 'datasets/usgslib7/ASCIIdata_splib07a'
spec_dataset = usgs_datasets.USGSLib7()
datafolders = next(os.walk(dataset_path))[1]
datafolders.remove('errorbars')
for folder in datafolders:
    folderpath = dataset_path + '/' + folder
    spec_dataset.encode_multiple_files(dataset_path,folderpath)

print(len(spec_dataset.get_txt_files(dataset_path)))

import glob

print(len(glob.glob(dataset_path+'/*.txt')))
