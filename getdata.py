from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import urllib.request
import pandas as pd 
import numpy as np
import utm


#Download and unzip the dataset if not already in the data folder
my_file = Path('data/geoc_inv/geoc_inv.txt')
if not my_file.is_file():
        # link to file (zipped)
    zipurl = 'https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/OTTBDX/UJJWF5'
        
        # Create a request with a modified user agent
    req = urllib.request.Request(zipurl, headers={'User-Agent' : "Real Browser"}) 
        
        # Download and unzip the file from the URL
    with urllib.request.urlopen(req) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall('data/geoc_inv')


# read using pandas, selecting only relevant columns
df=pd.read_csv('data/geoc_inv/geoc_inv.txt',usecols=[1,2,3,4,5],parse_dates=['filing_date'])


#Optional: Filter by country code, filing_date or patent_office
df=df[df["ctry_code"]=='DE']
df=df[(df["patent_office"]=='EP')|(df["patent_office"]=='DE')]
#df=df[df["filing_date"]>'1990-01-01']


# Convert lat,lon coordinates to x,y (web mercator)
# Source: https://gis.stackexchange.com/a/268233

def merc_from_arrays(args):
    lats=args[0]
    lons=args[1]
    r_major = 6378137.000
    x = r_major * np.radians(lons)
    scale = x/lons
    y = 180.0/np.pi * np.log(np.tan(np.pi/4.0 + lats * (np.pi/180.0)/2.0)) * scale
    return pd.Series([x, y])


# apply to the dataframe
df[['X','Y']]=df[['lat','lng']].apply(merc_from_arrays, axis=1)


# Save to file
df[['X','Y']].to_csv('data/stored.csv',index=False,float_format="%.6f")
