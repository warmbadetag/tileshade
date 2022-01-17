from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import urllib.request
import pandas as pd 
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
df=pd.read_csv('data/geoc_inv/geoc_inv.txt',usecols=[1,2,3,4,5],parse_dates=['filing_date'],nrows=1000)


#Optional: Filter by country code, filing_date or patent_office
df=df[df["ctry_code"]=='DE']
df=df[df["patent_office"]=='EP']
df=df[df["filing_date"]>'2000-01-01']


# Convert lat,lon coordinates to x,y (web mercator)
# wrap the utm.from_latlon function to return a pandas series 
def pd_from_latlon(args):
    x,y,a,b=utm.from_latlon(args[0], args[1])
    return pd.Series([x, y])

# apply to the dataframe
df[['x','y']]=df[['lat','lng']].apply(pd_from_latlon, axis=1)


# Save to file
df[['x','y']].to_csv('data/raw.csv',header=False,index=False,float_format="%.6f")
