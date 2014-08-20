#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands, os

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto.elastictranscoder

REGION = "us-west-1"
PIPELINE_ID = "1408045265931-rhai25"
BUCKET_NAME_INPUT = "plugair-youtube-encode-input"
BUCKET_NAME_OUTPUT = "plugair-youtube-encode-output"
PRESET_ID = "1351620000001-000040"  #  System preset generic 360p 16:9
VIDEO_FORMAT = "mp4"
VIDEO_EXT = "." + VIDEO_FORMAT

def download_youtube(video_id):
  print "Get video info...."

  # Video title
  status, output = commands.getstatusoutput('youtube-dl --get-filename -o "%(title)s" ' + video_id)
  if status != 0:
    print "### ERROR ### " + output
    return
  print "Title: " + output + ", Status: " + str(status)

  # Video thumbnail
  thumbnail_url = "http://i.ytimg.com/vi/" + video_id + "/hqdefault.jpg"
  print "Thumbnail URL: " + thumbnail_url

  # Download video
  status, output = commands.getstatusoutput('youtube-dl --max-quality ' + VIDEO_FORMAT + ' -o "tmp/%(id)s.%(ext)s" ' + video_id)
  if status != 0:
    print "### ERROR ### " + output 
    return
  print "Finished download: tmp/" + video_id + VIDEO_EXT

def upload_video_s3(video_id):
  filename = video_id + VIDEO_EXT
  filepath = "tmp/" + filename

  conn = S3Connection(os.environ.get("AWS_ACCESS_KEY_ID"), os.environ.get("AWS_SECRET_ACCESS_KEY"))
  bucket_input = conn.get_bucket(BUCKET_NAME_INPUT)

  # Remove all movie on input/output dir
  for a in bucket_input.list():
    bucket_input.delete_key(a)

  f = Key(bucket_input)
  f.key = filename
  f.set_contents_from_filename(filepath)
  #f.make_public()
  url = "https://s3-us-west-1.amazonaws.com/" + BUCKET_NAME_INPUT + "/" + filename
  f.close()
  print url

def transcode_video(video_id):
  filename = video_id + VIDEO_EXT
  filepath = "tmp/" + filename

  input_object = {
    "Key": filename,
    "Container": VIDEO_FORMAT, 
    "AspectRatio": "auto",
    "FrameRate": "auto",
    "Resolution": "auto",
    "Interlaced": "auto"
  }

  output_objects = [
    {
      "Key": filename,
      "PresetId": PRESET_ID,
      "Rotate": "auto",
      "ThumbnailPattern": "",
    }
  ]

  tc = boto.elastictranscoder.connect_to_region(REGION)
  tc.create_job(PIPELINE_ID, input_name=input_object, outputs=output_objects)

def cleaning():
  commands.getstatusoutput('rm tmp/*')

# main
video_id = "yArjZZKt7YA"
download_youtube(video_id)
upload_video_s3(video_id)
transcode_video(video_id)
cleaning()

