#Function to grab the tar files for each of the normal variations:
import os
import urllib.request as req
from bs4 import BeautifulSoup as bsoup
import tarfile

def get_climate_normals(main_url, normal_type, normal_period, normalFolder):
        
    if os.path.exists(f'{normalFolder}station_files'):
        return print(f'{normal_period} {normal_type} already downloaded...')
        
    base_url = f'{main_url}{normal_type}/{normal_period}/archive/'
   
    if normal_period == '1981-2010':
        tar_url = f'{base_url}{normal_type}.tar.gz'
    else:
        html_page = req.urlopen(base_url)
        soup = bsoup(html_page, "html.parser")
        for link in soup.findAll('a'):
            if 'station' in  link.text:
                tar_url = f'{base_url}{link.text}'
        
    ftpstream = req.urlopen(tar_url)
    file = tarfile.open(fileobj = ftpstream, mode = 'r|gz')
    
    print(f'Getting {normal_period} normals...')
    print(f'*** {normal_type} extracting to {normalFolder}station_files ***')
    file.extractall(f'{normalFolder}station_files')
    return print(f'*** {normal_type} extraction completed ***')