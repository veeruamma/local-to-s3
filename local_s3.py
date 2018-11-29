# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 19:40:02 2018

@author: Veeresh
"""
import boto
import configparser

#Reading the configuration file
config =configparser.ConfigParser()
config.read('s3_config.ini')

#Read s3 configuration file
host = config['s3']['host']
port = int(config['s3']['port'])
access_key = config['s3']['access_key']
secret_key = config['s3']['secret_key']

#boto.set_stream_logger('boto')
conn = boto.connect_s3(aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        port=port,
                        host=host, is_secure=False)

# Print all the buckets in S3
for bucket in conn.get_all_buckets():
    print(bucket)


#Creating a bucket and key in S3
bucket = conn.create_bucket('my_bucket1')
key = bucket.new_key('mykey')
key.set_contents_from_filename('img.png')

#Reading from bucket and writing it as image
mb = conn.get_bucket('my_bucket')
for key in mb.list():
    print(key.name)
    key.get_contents_to_filename('abc.png')

# get all the keys from bucket
full_bucket = conn.get_bucket('boto-demo-1539346193')

# before deleting the bucket , it should be empty
for key in full_bucket.list():
    key.delete()
    
    
conn.delete_bucket('boto-demo-1539346193')


import socket
socket.getaddrinfo('124.9.14.64', 8080)





