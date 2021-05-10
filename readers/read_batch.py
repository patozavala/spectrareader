from .readers import BaseReader, ReaderUSGS, ReaderDX, ReaderSpec
from spectrus import spectre
class BatchReader(BaseReader):
    """
    The "BatchReader" class allows importing batches of files with spectral
    information from objects.
    """
    def __init__(self):
        super().__init__()

    def get_filenames(self,dirpath):
        """
        Return a list with the names of valids files in a directory.
        """
        pass

    def read_from_dir(self,dirpath,file_format):
        """
        Search and read all valid files in a directory.
        """

        self.check_dir_if_exist(dirpath)

        # avoids issues with capital letters
        file_format = file_format.casefold()

        filenames = self.get_filenames(dirpath)
        spectra_list = []

        for file in filenames:
            spec = spectre.Spectre()
            if file_format=='dx':
                spec.spectral_signature = ReaderDX.read(file)
            elif file_format=='spec':
                spec.spectral_signature = ReaderSpec.read(file)
            elif file_format=='usgs':
                spec.spectral_signature = ReaderUSGS.read(file)
            spectra_list.append(spec)

        return spectra_list


br = BatchReader()
print(br.get_filenames.__annotations__)
