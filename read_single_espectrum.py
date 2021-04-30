from spectrareaders import readers

"""
Example 1: read a single file from the USGS Spectral Library Version 7 Data.
"""
spec = readers.ReaderUSGS()
print(spec.__doc__)
files = {
    'reflectance': 'samples/usgs/Actinolite.txt',
    'bandpass': 'samples/usgs/Bandpass.txt',
    'wavelength': 'samples/usgs/Wavelength.txt'
}
usgs_record = spec.read_usgs(files=files)

print(usgs_record['data'])
