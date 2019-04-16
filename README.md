```bash
# @file: README.md
# @version: 2019-04-16
# @created: 2019-04-16
# @author: pyramid
# @brief: documentation for python-tools
# @website: https://openteq.wordpress.com/
# @repo: https://github.com/pyramid3d/python-tools
```


=====================================
# **Python Tools**
## **python-tools.git**
**handy tools for the python 3 programming language**
=====================================

=====================================
# code style
=====================================

- classes - CamelCase 
- methods - mixedCase (recommended: lowercase_with_underscores) 
- constants - ALL_CAPITALS 
- public variables - mixedCase (recommended: lowercase_with_underscores 
- private variables - mixedCase (recommended: lowercase_with_underscores 
- also see http://www.python.org/dev/peps/pep-0008/ 
- indentation: 2


=====================================
# mapillary_download.py
=====================================

The initial version has been based on mapillary_tools
(https://github.com/mapillary/mapillary_tools).

However, the code was completely rewritten to update it to
modern python 3.7.2+, especially the use of urllib
(https://docs.python.org/3/library/urllib.html)

Further, the original code required the corners of a bounding box as input params.
This was considered very tedious, while a normal user (like me; and what is normal anyway)
would prefer to download his own images from a specific period of time, let's say a
excursion, or exploration event.

The present code only requires the user name, and the boundary dates, start date and end date.
For example:

```
> python3 mapillary_download.py pyramid 2019-04-06 2019-04-07
```

The dates always assume midnight (00:00 UTC), so if you want to download one day,
do increase the end date by one day.

Only processed images are downloaded with their maximum resolution (2048x1152).
Individual sequences are downloaded into individual folders with teh time stamp of
the first image of the sequence.
Images are named with the time stamp of the image.
A geocoordinates.txt file in each sequence directory contains the
(longitude, latitude) geo coordinates for each image.

See also:
(https://openteq.wordpress.com/2019/04/06/mapillary-images/)

