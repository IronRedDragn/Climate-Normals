#Function to grab the tar files for each of the normal variations:
import os
import urllib.request as req
from bs4 import BeautifulSoup as bsoup
import tarfile
import csv

dataFolder = './data/station_normals/'
txtFiles_Folder = './txt_files/'
normals_dict = { '1981-2010': ('normals-hourly','normals-daily', 'normals-monthly'),
                 '1991-2020': ('normals-hourly','normals-daily', 'normals-monthly'),
                 '2006-2020': ('normals-hourly','normals-daily', 'normals-monthly')
                 }
main_url = 'https://www.ncei.noaa.gov/data/'


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

def generate_header_files():
    '''
This function creates the header csv files. This files list the expected columns in each of the 
climate normal records. Each line will be consists of :

column name: name of the normal variable or normal variable flags

format: --(1980-2010 normals)--  None: no formatting needed
                                 decimal place for each variable 
                                 -> Wholes: 705 -> 700
                                    Tenths: 705 -> 70.5
                                    Hundredths: 705 -> 7.05

        --(1991-2020, 2006-2020)-- None: no formatting needed
                                   these values are provided in correct decimal place

        --(hourly normals)-- Wind_Direction: prevailing and secondary wind directions can take on 8 values: 
                                              1=N, 2=NE, 3=E, 4=SE, 5=S, 6=SW, 7=W, 8=NW


The decision to format the column is based off the documentation found on the ncei website.
'''
    baseHeaders = [['STATION'], ['DATE'],['month'],['day'],['hour']]

    # column formatting 1980-2010 normals
    hundreths = ['precipitation totals', 'precipitation amount']
    whole = ['degree days','snow depth totals', 'vector direction']
    wind_dir = ['wind direction']

    for normal_period, normal_types in normals_dict.items():
        for normal_type in normal_types:
            headerFile = f'{txtFiles_Folder}csv_headers/headers-{normal_period}-{normal_type}.txt'
            varFile = f'{txtFiles_Folder}variables/variables-{normal_period}-{normal_type}.csv'

            with open(headerFile, 'w' , newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(baseHeaders)
                with open(varFile, 'r') as infile:
                    reader = csv.reader(infile)
                    for row in reader:
                        colName = row[0]
                        fullName = row[1]
                        if normal_period == '1981-2010':
                            format = 'Tenths'
                            if any(word in fullName.lower() for word in hundreths):
                                format = 'Hundredths'
                            elif any(word in fullName.lower() for word in whole):
                                format = 'None'
                            elif any(word in fullName.lower() for word in wind_dir):
                                format = 'Wind_Direction'

                            varRows = [[colName,format],[colName + '_ATTRIBUTES', 'None']]
                        else:
                            format = 'None'                     
                            if any(word in fullName.lower() for word in wind_dir):
                                format = 'Wind_Direction'
                            varRows = [[colName,format],
                                       ['meas_flag_' + colName, 'None'],
                                       ['comp_flag_' + colName, 'None'],
                                       ['years_' + colName, 'None']]

                        writer.writerows(varRows)
    return print(f'Headers files generated at {txtFiles_Folder}csv_headers/')

def main():

    for normal_period, normal_types in normals_dict.items():
        for normal_type in normal_types:
            folder_location = f'{dataFolder}{normal_period}/{normal_type}/'
            get_climate_normals(main_url, normal_period, normal_type, folder_location)

    generate_header_files()


if __name__ == "__main__":
    main()