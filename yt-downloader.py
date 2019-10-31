import json
import subprocess
import boto3
import os
import time
from botocore.exceptions import ClientError
from subprocess import CalledProcessError
from subprocess import Popen, PIPE

bucket_name = str(os.environ['s3bucket_'])
key_name = str(os.environ['s3bucketkey_'])
key_name = ""
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

copy = subprocess.check_output("cp -f ./yt-lambda/youtube-dl /tmp/youtube-dl", shell=True)

def check_dir_size():
    check_ = subprocess.check_output("ls -s /tmp/", shell=True)
    check_proc = str(check_.decode('UTF-8')).split('\n')
    check_size = str(check_proc[0]).split(" ")
    return(int(check_size[1]))

def wait_for_complete():
    #wait for file to copy
    time_ = 0
    size_0 = check_dir_size()
    while 5 >= time_:
        size_1 = check_dir_size()
        if size_1 == size_0:
            time.sleep(1)
            time_ +=1
        else:
            time_ = 0
            size_0 = size_1
    return(size_1)

def lambda_handler(event, context):
    clean1 = subprocess.call("rm -r /tmp/*.*", shell=True)

    yt_link_import = event
    yt_link_parse = yt_link_import.split('&')
    yt_link = "https://www.youtube.com/watch?v=" + yt_link_parse[0]
    print(yt_link)

    ytdl_command = "./youtube-dl -itcv -f mp4 " + yt_link + " --write-all-thumbnails --restrict-filenames"

    # Setup youtube downloader
    os.chdir("/tmp")

    wait_for_complete()

    # run youtube downloader, saves output to /tmp/
    prep = subprocess.check_output("chmod 777 youtube-dl", shell=True)
    process = subprocess.Popen(ytdl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    wait_for_complete()


    # format file string
    prep_string_ = subprocess.check_output("ls -1", shell=True).decode()
    string_split_ = prep_string_.split("\n")
    file_name = str(string_split_[1])
    file_path = key_name + file_name
    s3_client.upload_file(file_name,bucket_name,"videos/ingest/" + file_name, ExtraArgs={'ACL':'bucket-owner-full-control'})
    wait_for_complete()

    return("completed: " + file_name)
