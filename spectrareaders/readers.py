import pandas as pd

class BaseReader():
    def __init__(self):
        pass

    def check_file_if_exists(self,filepath):
        """
        Verify that a required file exists.
        """
        try:
            f = open(filepath)
            f.close()
        except:
            raise Exception (filepath+' does not exists.')         

    def check_file_is_readable(self,filepath):
        """
        Verify that a required file is readable.
        """
        try:
            f = open(filepath)
            f.readable()
            f.close()
        except:
            raise Exception (filepath+' is not readable.')

class ReaderUSGS(BaseReader):
    """
    ReaderUSGS class manages the files into the USGS Spectral Library Version
    7 Data. Each file contains spectra measured with laboratory, field, and 
    airborne spectrometers.

    The library is provided on digital media and online at 
    https://speclab.cr.usgs.gov/spectral-lib.html.

    Reference
    Kokaly, R.F., Clark, R.N., Swayze, G.A., Livo, K.E., Hoefen, T.M., 
    Pearson, N.C., Wise, R.A., Benzel, W.M., Lowers, H.A., Driscoll, R.L.,
    and Klein, A.J., 2017, USGS Spectral Library Version 7 Data: U.S. 
    Geological Survey data release, https://dx.doi.org/10.5066/F7RR1WDJ.
    """

    def __init__(self):
        super().__init__()

    def read_usgs(self, files):
        """
        Read a dictionary with spectroscopy file in .txt file format used in
        USGS Spectral Library Version 7 Data.

        Args:
            files ([dict]): A <dict> object with file paths necessary to handle
                            records from the spectrometer. Each key corresponds
                            to the column name in the output dataframe.
        
        Returns:
            data ([dict]): A <dict> object that contains the data from the 
                           spectroradiometer, the metadata associated with the
                           record, and the label of the measured object.
        """

        # initialization
        label= None
        id_record= None
        metadata = {}
        data_dict = {}
        # import and decode each file
        for file in files:
            measurement = self.__decode_file_usgs(files[file])
            metadata[str(measurement['metadata'])] = measurement['metadata']
            if file!='reflectance':
                data_dict[str(measurement['name'])] = measurement['data']           
            else:
                data_dict['Reflectance'] = measurement['data']
                label = measurement['name']
                id_record = measurement['id_record']

        data_df = pd.DataFrame.from_dict(
            data_dict,
            orient='columns', 
            dtype=float
        )
        data_df.index.name = label+'_'+id_record
        data = {'data': data_df,
                'metadata': metadata,
                'label': label
        }
        return data
       
    def __read_txt(self, filepath):
        """
        Read a single .txt file and remove the leading and the trailing 
        characters in each line.

        Args:
            filepath ([str]): file path of the file to read.

        Returns:
            data_clean ([list]): list of str objects of every line of the text
                                 file without the leading and the trailing 
                                 characters.
        """
        # previous checks
        self.check_file_if_exists(filepath)
        self.check_file_is_readable(filepath)

        with open(filepath,'r') as reader:
            data_raw = reader.readlines()
        data_clean = [data_raw[i].strip() for i in range(len(data_raw))]
        return data_clean  

    def __decode_file_usgs(self, filepath):
        """
        Decode a single spectrometer file in the USGS file format.

        Args:
            filepath ([txt]): file path of the file to decode.

        Returns:
            [dict]: dictionary with the data and relevant metadata.
        """
        # read file
        file = self.__read_txt(filepath)
        # metadata
        name = file[0].split(sep=' ')[2]
        id_record = file[0].split(sep=' ')[1][:-1]
        metadata= file[0].strip()
        # data recorded
        data = [float(file[i]) for i in range(1,len(file))]
        data_decoded = {
            'name': name,
            'metadata': metadata,
            'data': data,
            'id_record': id_record 
        }
        return data_decoded
