from io import BytesIO
from zipfile import ZipFile
import urllib
import utm

    # link to file (zipped)
zipurl = 'https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/OTTBDX/UJJWF5'
    
     # Create a request with a modified user agent
req = urllib.request.Request(zipurl, headers={'User-Agent' : "Real Browser"}) 
    
    # Download and unzip the file from the URL
with urllib.request.urlopen(req) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall('/data/geoc_inv')

    # read using pandas, selecting only relevant columns
df=pd.read_csv('data/geoc_inv.txt',usecols=[2,3,4,5],parse_dates=['filing_date'],nrows=10)

    #Optional: Filter by country code
#df=df[df["ctry_code"]=='DE']


    # Convert lat,lon coordinates to x,y (web mercator)
#x, y = utm.from_latlon(input_lat, input_lon)

    # Save to file

