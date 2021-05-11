import os
import glob
import pandas as pd

class BaseReader():
    """
    Implements several verifications and utilities for handling spectral files.
    """
    def __init__(self):
        pass

    def check_file_if_exists(self,filepath):
        """
        Verifies that a required file exists.
        """
        try:
            f = open(filepath)
            f.close()
        except:
            raise Exception (filepath + ' does not exists.')         

    def check_file_is_readable(self,filepath):
        """
        Verifies that a required file is readable.
        """
        try:
            f = open(filepath)
            f.readable()
            f.close()
        except:
            raise Exception (filepath + ' is not readable.')
    
    def check_dir_if_exist(self,dirpath):
        """
        Verifies that a directory exists.
        """
        if os.path.isdir(dirpath):
            return True
        else:
            raise Exception (dirpath + 'does not exists.')

class SpectraReader(BaseReader):
    """
    SpectraReader reads .csv file with spectral information from objects. The spectrum is measured with laboratory and field spectrometers.
    SpectraReader allows handling the spectral information into a pandas dataframe. Each spectral measurement must follow the current protocols of the company.
    """

    def __init__(self):
        super().__init__()
    
    def read_spectrum(self, filepath: str) -> dict:
        """
        Reads a .csv file with an spectroradiometer measurement. 
        """

        self.check_file_if_exists()
        self.check_file_is_readable()

        data = pd.read_csv(filepath)
        label = filepath.split(sep='_')[0]

        spectrum = {
            'label': label,
            'data': data,
        }
        return spectrum

    def read_multiple_spectra(self, dirpath: str) -> list:
        """
        Reads multiple files from a directory an store each measurement into a Spectrum object.
        """

        self.check_dir_if_exist()
        filepaths = glob.glob(dirpath + '/*.txt')
        spectra = []
        for file in filepaths:
            spectrum = self.read_single_file(file)
            spectra.append(spectrum)

        return spectra
