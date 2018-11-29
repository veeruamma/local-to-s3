# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 20:45:35 2018

@author: Veer
"""

import botocore.session
from botocore.client import Config
import configparser, os


import numpy as np 
import pandas as pd 
import sklearn as sk
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform



def get_s3_keys(bucket):
    """Get a list of keys in an S3 bucket."""
    keys = []
    resp = blob_client.list_objects(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys

#Reading the configuration file
config_parser =configparser.ConfigParser()
config_parser.read('s3_config.ini')

#Read s3 configuration file
url = config_parser['s3']['url']
access_key = config_parser['s3']['access_key']
secret_key = config_parser['s3']['secret_key']

config = Config(signature_version='s3')
session = botocore.session.get_session()

#creating client to access S3 database
blob_client = session.create_client('s3',region_name='',
                                    aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key,
                                    endpoint_url=url,
                                    config=config)
class_translate = {"test_fault_0" : 0, "test_fault_1" : 1, "test_fault_2" : 2, 
                   "test_fault_3" : 3, "test_fault_4" : 4, "test_fault_5" : 5}

#create bucket and saving images to each bucket
for i in class_translate.keys():
    print("Processing bucket : ", i)
    blob_client.create_bucket(Bucket=i)
    for j in os.listdir("RP_Images/training_set/"+i+"/"):
        #print("Saving image : ", j)
        blob_client.put_object(Body=open("RP_Images/training_set/"+i+"/"+j, 'rb').read(), 
                       Bucket=i, Key=j)
    print("Total "+str(len(os.listdir("RP_Images/training_set/"+i+"/")))+
          " are inserted in bucket "+i)
import tempfile
import shutil
path= 'C:\delete\local to s3'
dir_name = tempfile.mkdtemp(prefix='s3_rp_', dir=path)
d0 = tempfile.mkdtemp(prefix='f0_', dir=dir_name)
d1 = tempfile.mkdtemp(prefix='f1_', dir=dir_name)
d2 = tempfile.mkdtemp(prefix='f2_', dir=dir_name)
d3 = tempfile.mkdtemp(prefix='f3_', dir=dir_name)
d4 = tempfile.mkdtemp(prefix='f4_', dir=dir_name)
d5 = tempfile.mkdtemp(prefix='f5_', dir=dir_name)
print(d1)
list_d = [d0, d1, d2, d3, d4, d5]

class_translate = {"d0" : 0, "d1" : 1, "d2" : 2, 
                   "d3" : 3, "d4" : 4, "d5" : 5}
remove = 'C:\delete\local to s3\s3_rp_hscn6b86'
shutil.rmtree(remove)

#Reading the images from buckets 

k=0
for i in list_d:
    print("Reading from bucket : ", 'fault_'+str(k))
    key_list = get_s3_keys('fault_'+str(k))
    for j in key_list:
        resp_get = blob_client.get_object(Bucket='fault_'+str(k),Key=j)
        with open(i+'/'+j,'wb') as f:
            f.write(resp_get['Body'].read())
    k=k+1
            


len(blob_client.list_objects(Bucket='fault_2', Prefix='sample'))


key_list = get_s3_keys('fault_2')


#inserting the object into the bucket 
blob_client.put_object(Body=open("s3_database/img.png", 'rb').read(), 
                       Bucket='aoi-test-iii', Key='test_1.jpg')


blob_client.list_buckets()

resp_get = blob_client.get_object(Bucket='trial-veer',
                                  Key='test_1.jpg')

#delete a bucket
blob_client.delete_bucket(Bucket='trial-veer')

for i in class_translate.keys():
    blob_client.delete_bucket(Bucket=i)

for j in os.listdir("RP_Images/fault_0/"):
    print(j)





#type 2
def rec_plot(s, eps=0.10, steps=10):
    d = pdist(s[:,None])
    d = np.floor(d/eps)
    d[d>steps] = steps
    Z = squareform(d)
    return Z

def get_max_values(signal, size):
    max_values = []
    st = 100
    for i in range(0, size, st):
        max_value_A = max(signal[i:i+st])
        min_value_A = min(signal[i:i+st])
        max_values.append((max_value_A-min_value_A))
    return max_values



#second trial
size = 20000
rec_steps = 1000
fig = plt.figure(figsize=(15,14))
ax = fig.add_subplot(2, 3, 1)
dat = pd.read_csv("sample_1.csv").iloc[:,4]
rec_a = rec_plot(np.array(get_max_values(dat, size)))
ax.imshow(rec_a)
ax.set_xlabel('Fault1')
import numpy
 
def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = numpy.fromstring ( fig.canvas.tostring_argb(), dtype=numpy.uint8 )
    buf.shape = ( w, h,4 )
 
    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = numpy.roll ( buf, 3, axis = 2 )
    return buf

from PIL import Image
 
def fig2img ( fig ):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    """
    # put the figure pixmap into a numpy array
    buf = fig2data ( fig )
    w, h, d = buf.shape
    return Image.fromstring( "RGB", ( w ,h ), buf.tostring( ) )

im = fig2data(fig)


blob_client.put_object(Body=open(im, 'rb').read(), 
                       Bucket='trial-veer', Key='test_1.jpg')