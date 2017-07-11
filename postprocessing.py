'''
Contains all the post processing tools necessary after the savu process has occured
'''


processed_data = '/dls/i08/data/2017/cm16789-3/processing/aaron/20170705111629_10481/i08-10481_processed.nxs'
outfile = '/dls/i08/data/2017/cm16789-3/processing/aaron/20170705111629_10481/pymca_rgb_converted.dat'

# def convert_to_pymca_rgb(processed_data, outfile):
#     import h5py as h5
#     f = h5.File(processed_data,'r')
#     scan_axes = 0,1
#     det_elem = 0
#     peak_indices  = f['entry/final_result_fluo'].attrs['PeakElements_indices']
#     elements = list(f['entry/final_result_fluo/PeakElements'][...])
#     data = f['entry/final_result_fluo/data']
#     
#     titles = ['row','column']
#     titles.extend(elements)
#     titles = [ix.replace(" ", "-") for ix in titles]
#     titles = "  ".join(titles)
#     k = 0 
#     
#     with open(outfile,'wb') as f:
#         if k==0:
#             f.write(titles+"\n")
#         for row in range(data.shape[0]):
#             print("%d of %d" % (row, data.shape[0]))
#             for column in range(data.shape[1]):
#                 line = list(data[row,column,det_elem])
#                 line = [str(ix) for ix in line]
#                 extra = [str(row),str(column)]
#                 extra.extend(line)
#                 line_to_write = "  ".join(extra)
#                 f.write(line_to_write+"\n")
# 
# def convert_to_pymca_edf(processed_data, outfile):
import h5py as h5
f = h5.File(processed_data,'r')
scan_axes = 0,1
det_elem = 0,#,1,2,3
peak_indices  = f['entry/final_result_fluo'].attrs['PeakElements_indices']
elements = list(f['entry/final_result_fluo/PeakElements'][...])
data = f['entry/final_result_fluo/data']
import collections
import numpy as np
from fabio.edfimage import EdfImage


for num, key in enumerate(elements):
    for channel in det_elem:
        foo = data[:,:,channel,num]
        header = collections.OrderedDict()     
        header['HeaderID'] = 'EH:000001:000000:000000'
        header['Image'] = '1'
        header['ByteOrder'] = 'LowByteFirst'
        header['DataType']=  'DoubleValue'
        header['Dim_1'] = str(foo.shape[-1]) 
        header['Dim 2'] = str(foo.shape[-2])
        header['Size'] = str(8.0*np.prod(foo.shape))
        out_title = "%s_channel_%s" % (key.replace(" ","_"), str(channel))
        header['Title'] = out_title
        fout = EdfImage(foo, header)
        fout.write('/dls/i08/data/2017/cm16789-3/processing/aaron/20170705111629_10481/'+out_title+'.edf')



    