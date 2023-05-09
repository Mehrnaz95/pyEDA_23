# Importing necessary libraries
import csv

def openShimmerFile(url, column_name):

  '''finding to open the files
    Funcion that extracts gsr data from the files
    
    Parameters
    ----------
    url : String
        The address of the csv file from Shimmer
	column_name : String
        The name of the column to extract its data from the file
    
    Returns
    -------
    req_data : 1-d array
        Array containing the gsr data
  '''

  req_data = []
  index = -1
  with open(url) as f:
    if 'csv' in url:
      reader = csv.reader(f, delimiter=',')
    else:
      reader = csv.reader(f, delimiter='\t')

    #sep = next(reader, None)
    #sep = next(reader, None)
    sep = next(reader, None)		
    forth_row = next(reader, None)
    shimmer_header = []
    data_header = []
    calib_header = []
    forth_row = forth_row[0].split('\t')

    for i, column in enumerate(forth_row):
      if column == column_name:
        index = i
        print(index)
    
    if index < 0:
      print("Column not found!")
      #return req_data
      
    next(reader, None)  # Skip the next row

    for row in reader:
      row = row[0].split('\t')
      if len(row) > index:
        try:
          req_data.append(float(row[index]))
          #print(row[index])
        except ValueError:
          print(f"Error converting value to float: {row[index]}")
      
# #return req_data

  return req_data
