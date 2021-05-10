import os
import glob
import shutil
from pathlib import Path

class USGSLib7():
    """
    The "USGSLib7" class encodes the files into the USGS Spectral Library Version 7 Data. Each original file contains spectra measured with laboratory, field, and airborne spectrometers. In parallel, each encoded file merges the wavelength, reflectance, and bandpass into a .txt document designed for automated treatment in ai-based algorithms.

    The library is provided on digital media and online at https://speclab.cr.usgs.gov/spectral-lib.html.

    Reference
    Kokaly, R.F., Clark, R.N., Swayze, G.A., Livo, K.E., Hoefen, T.M., Pearson, N.C., Wise, R.A., Benzel, W.M., Lowers, H.A., Driscoll, R.L., and Klein, A.J., 2017, USGS Spectral Library Version 7 Data: U.S. Geological Survey data release, https://dx.doi.org/10.5066/F7RR1WDJ. 
    """
    def __init__(self):
        pass

    def encode_single_file(self, files: dict, category: str) -> bool:
        """
        This function associates a reflectance measurement with its corresponding instrument wavelength and bandpass files. The encoding process delivers a new .txt file that stores all information and has the following structure.

        #METADATA 
        #reflectance metadata
        ...
        #wavelength metadata
        ...
        #bandpass metadata
        ...
        #DATA 
        #reflectance
        ...
        #wavelength
        ...
        #bandpass
        ... 
        """
        
        metadata = ['#METADATA \n']
        data = ['#DATA \n']


        for filename in files:
            # open and read every non-empty pathfile
            if files[filename] != None:
                with open(files[filename],'r') as file_reader:
                    file_data = file_reader.readlines()
                    file_reader.close()

                # metadata and label are extracted from the reflectance file
                if filename.casefold() == 'reflectance':
                    meta_reflectance = file_data[0].strip().split(sep=' ')
                    label = meta_reflectance[2]
                    id_record = meta_reflectance[1][:-1]

                    encoded_filepath = (
                        'datasets/usgslib7/data/'
                        + category
                        + '/'
                        + label.casefold().replace('/','-')
                        + '_'
                        + id_record.casefold().replace('=','_')
                        + '.txt'
                    )

                # stores metadata into a list
                metadata.append('#' + filename + ' metadata' + '\n')
                metadata.append(file_data[0].strip(' '))

                # stores numeric data of each file in a list
                file_data.pop(0)
                data += ['#' + filename + '\n']
                data += [file_data[i] for i in range(len(file_data))]

                # write encoded file
                with open(encoded_filepath,'w+') as spectrus_writer:
                    spectrus_writer.writelines(metadata)
                    spectrus_writer.writelines(data)
                    spectrus_writer.close()

        return True

    def encode_multiple_files(self, instruments_dirpath: str, data_dirpath: str) -> bool:
        """
        This function performs the encoding process for all files into a directory. 

        The encoding process joins a reflectance measurement with its corresponding instrument parameters (bandpass and wavelength), and stores all information into a .txt file.
        """

        instruments = self.get_instruments(instruments_dirpath)
        measurements = self.group_by_instrument(instruments, data_dirpath)
        
        category = data_dirpath.split(sep='_')[-1]
        encoded_path = Path('datasets/usgslib7/data/' + category)

        # removes encoded_path folder if it exists and creates a new one
        if encoded_path.is_dir():
            shutil.rmtree(encoded_path)
        os.makedirs(encoded_path)

        # performs the encoding process for each reflectance file
        for instrument in instruments:
            for reflectance in measurements[instrument].reflectance:
                spectre_files = {
                    'reflectance': data_dirpath + '/' + reflectance,
                    'wavelength': measurements[instrument].wavelength,
                    'bandpass': measurements[instrument].bandpass,
                }
                self.encode_single_file(spectre_files,category)

        return True

    def get_txt_files(self, dataset_path: str) -> list[str]:
        """
        Delivers a list with all text files into a directory.
        """

        txt_files = glob.glob(dataset_path + '/*.txt')
        return txt_files

    def get_instruments(self, dataset_path: str) -> dict:
        """
        Delivers the name of the instruments and the pathfiles associated to each one.
        """

        txt_files = self.get_txt_files(dataset_path)

        # dict with all available instruments in this dataset
        instruments = {
            'ASDNG': Instrument(name='ASDNG'),
            'BECK': Instrument(name='BECK'),
            'ASDFR': Instrument(name='ASDFR'),
            'AVIRIS': Instrument(name='AVIRIS'),
            'NIC4': Instrument(name='NIC4'),
            'ASDHR': Instrument(name='ASDHR'),
        }

        # removes the wavenumber file
        wavenumber_file = [i for i in txt_files if 'Wavenumber' in i][0] 
        txt_files.remove(wavenumber_file)
        # get instrument name and the file paths for bandpass and wavelength
        for filepath in txt_files:
            with open(filepath, 'r') as reader:
                metadata = reader.readlines()[0]
                reader.close()
            if 'Wavelength' in metadata:
                instrument_name = metadata.strip().split(sep=' ')[3]
                if 'ASD' in instrument_name:
                    instruments['ASDFR'].update_wavelength(filepath)
                    instruments['ASDHR'].update_wavelength(filepath)
                    instruments['ASDNG'].update_wavelength(filepath)
            elif 'Bandpass' in metadata:
                instrument_name = metadata.strip().split(sep=' ')[4]
                instruments[instrument_name].update_bandpass(filepath)

        return instruments

    def group_by_instrument(self, instruments: dict, dirpath: str) -> dict:
        """
        Groups the files contained into a directory by its instrument name informed in the metadata.
        """

        reflectances = self.get_txt_files(dirpath)
        instruments_names = instruments.keys()

        for reflectance in reflectances:
            for instrument in instruments_names:
                if instrument in reflectance:
                    instruments[instrument].update_reflectance(reflectance)
        return instruments


class Instrument():
    """
    An instrument stores all the file paths necessary to construct the spectral signatures measured with a specific spectroradiometer.
    """

    def __init__(self, name: str):
        self.name = name
        self.wavelength = None
        self.bandpass = None
        self.reflectance = []

    def update_wavelength(self, wavelength_path: str) -> str:
        """
        This function update the filename that contains the wavelength.
        """
        self.wavelength = wavelength_path
        return self.wavelength

    def update_bandpass(self, bandpass_path: str) -> str:
        """
        This function update the filename that contains the bandpass.
        """
        self.bandpass = bandpass_path
        return self.bandpass

    def update_reflectance(self, filepath: str):
        """
        This function attaches a filename to the reflectance file list associated with the instrument.
        """
        self.reflectance.append(filepath)

