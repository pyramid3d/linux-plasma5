#!python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#
# @file: mapillary_download.py
# @version: see __version__
# @created: 2019-04-15
# @author: pyramid
# @brief: download mapillary images by date and sequences
# @param: username
# @param: start_date
# @param: end_date
# @example: python3 mapillary_download.py pyramid 2019-04-06 2019-04-07
# ---
# @website: https://openteq.wordpress.com/
# @repo: https://github.com/pyramid3d/python-tools
# Script to download images using the Mapillary image search API.
# Downloads images given the mapillary user and boundary dates.
# Dates are assuming midnight (00:00)
# To download only one specific day, increase end date by one day.
# ---
# code style: 
# classes - CamelCase 
# methods - mixedCase (recommended: lowercase_with_underscores) 
# constants - ALL_CAPITALS 
# public variables - mixedCase (recommended: lowercase_with_underscores 
# private variables - mixedCase (recommended: lowercase_with_underscores 
# also see http://www.python.org/dev/peps/pep-0008/ 
# indentation: 2
'''
__version__ = "v0.00.00 | 2019-04-16"

import urllib.request
import json
import os
import shutil
import argparse

BASE_DIR = 'mapillary/'
# See https://www.mapillary.com/developer/api-documentation/
MAPILLARY_API_IM_SEARCH_URL = 'https://a.mapillary.com/v3/images?'
MAPILLARY_API_IM_RETRIEVE_URL = 'https://images.mapillary.com/'
CLIENT_ID = 'MkJKbDA0bnZuZlcxeTJHTmFqN3g1dzo1YTM0NjRkM2EyZGU5MzBh'


'''
Helper functions
'''


'''
# delete existing directory and create a fresh one
'''
def createCleanDir(base_path):
  try:
      shutil.rmtree(base_path)
  except:
      pass
  os.mkdir(base_path)


'''
# try creating a directory
# skip if already existing
'''
def createDir(dirPath):
  try:
    os.mkdir(dirPath)
  except:
    pass


'''
# save filename with lon, lat for previous sequence
'''
def writeGeo(dirName, imgList):
  with open(dirName + "/geocoordinates.txt", "w") as f:
    for data in imgList:
      f.write(",".join(data) + "\n")


'''
Script to download images using the Mapillary image search API.
Downloads images from user (username) and dates (start_time, end_time)
'''

def querySearchApi(usernames, start_time, end_time, max_results):
    '''
    Send query to the search API and get dict with image data.
    '''

    # Create URL
    params = 'client_id=' + CLIENT_ID +'&usernames=' + usernames + '&start_time=' + start_time + '&end_time=' +end_time
    print(MAPILLARY_API_IM_SEARCH_URL + params)

    # Get data from server, then parse JSON
    query = urllib.request.urlopen(MAPILLARY_API_IM_SEARCH_URL + params).read()
    #print(query) # debug only
    parsed = json.loads(query)
    #print(json.dumps(parsed, indent=2, sort_keys=True)) # debug only
    query = json.loads(query)['features']

    print("Result: {0} images.".format(len(query)))
    return query


def downloadImages(query, path, size=2048):
    '''
    Download images in query result to path.

    Return list of downloaded images with lat,lon.
    There are four sizes available: 320, 640, 1024 (default), or 2048.
    '''
    im_size = "thumb-{0}.jpg".format(size)
    imgList = []
    currentSequence = ""
    currentSequenceDir = ""

    for im in query:
      # Use key to create url to download from and filename to save into
      key = im['properties']['key']
      sequence = im['properties']['sequence_key']
      imgTime = im['properties']['captured_at']
      imgTime = imgTime.replace(":","") #.replace("-","") #.replace(".","")
      #print(imgTime)
      url = MAPILLARY_API_IM_RETRIEVE_URL + key + '/' + im_size
      #filename = BASE_DIR + sequence + "/" + imgTime + ".jpg"
      #createDir(BASE_DIR + sequence)
      
      if sequence != currentSequence and imgList != []:
        # save filename with lon, lat for previous sequence
        writeGeo(BASE_DIR + currentSequenceDir, imgList)
        imgList = []

      if sequence != currentSequence:
        currentSequence = sequence
        currentSequenceDir = imgTime
        print("currentSequence:", currentSequence)
        print("currentSequenceDir:", currentSequenceDir)

      filename = BASE_DIR + currentSequenceDir + "/" + imgTime + ".jpg"
      createDir(BASE_DIR + currentSequenceDir)

      try:
        # Get image and save to disk
        # urlretrieve may become deprecated
        #filename, image = urllib.request.urlretrieve(url)
        #image.read()
        # probbaly the more stable approach
        with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
          data = response.read() # a `bytes` object
          out_file.write(data)

        # Log filename and geo coordinates
        coords = ",".join(map(str, im['geometry']['coordinates']))
        imgList.append([filename, coords])

        print("Successfully downloaded: {0}".format(filename))
      except KeyboardInterrupt:
        break
      except Exception as e:
        print("Failed to download: {} due to {}".format(filename, e))

      # save filename with lon, lat for last sequence
      writeGeo(BASE_DIR + currentSequenceDir, imgList)

    return imgList


if __name__ == '__main__':
  print("--- mapillary download |", __version__, "---")
  '''
  Use from command line as below, or run querySearchApi and downloadImages
  from your own scripts.
  '''

  parser = argparse.ArgumentParser()
  parser.add_argument('usernames', type=str)
  parser.add_argument('start_time', type=str)
  parser.add_argument('end_time', type=str)
  parser.add_argument('--max_results', type=int, default=400)
  parser.add_argument('--image_size', type=int,
                      default=2048, choices=[320, 640, 1024, 2048])
  args = parser.parse_args()

  # query api
  query = querySearchApi(args.usernames, args.start_time,
                            args.end_time, 400)

  # create fresh base directory for saving
  createCleanDir(BASE_DIR)

  # download
  dnlList = downloadImages(query, path=BASE_DIR, size=args.image_size)
