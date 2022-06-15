# imports the URL libary, which helps download images from websites
import urllib.request
# imports the pandas library, which stores data into spreadsheet-like objects
import pandas as pd

# the dest (short for "destination") is the path to the file where all the images will be downloaded
# Note that "\" is a break character that interferes with how strings of text are read
# Consequently, add the letter "r" in front of the destination name to avoid issues with parsing text
# This may be either an absolute path (recommended for beginners) or a relative path, depending on how the file is saved
dest = r"C:\Users\Example\FlowerClassification\Observations"

# Read data from a CSV file and stores it into a dataframe
# Like the destination, an "r" should be added in front path
# This may be either an absolute path (recommended for beginners) or a relative path, depending on how the file is saved
# Note: most of the time, no further arguments are required. Sometimes, though, there will be encoding issues
# The most common fix is to add an argument, "encoding", using either:
# encoding = 'utf-8'
# encoding = 'latin1', 
# encoding = 'iso-8859-1',
# encoding = 'cp1252'
df = pd.read_csv(r"C:\Users\Example\FlowerClassification\data.csv")

# This for loop iterates through every image url in the dataframe and downloads it locally to the destination
for i in range(0,len(df.index)):
    # The "try" tells the program to attempt the below code. If it fails for whatever reason, it moves to the "except"
    try:
        # A single line to invisibly visit the image url and download it to the preselected destination
        # Note 1: that it is assumed that the dataframe as a column labeled "image_url" and "id"
        # Note 2: Images are saved under their id as a jpg
        urllib.request.urlretrieve(df['image_url'][i], dest + str(df['id'][i]) + '.jpg')
    # If the code fails, "continue" is called so that the program continues to run. This means if there is an error,
    # (e.g. url is no longer available, incorrect url, bad internet connection, etc.) the loop moves to the next 
    # item and the image is not downloaded
    except:
        continue
    
    # This is a really rough progress bar. Essentially, whenever an image downloads, a line will print telling how
    # many images have been downloaded so far out of the total. For example, if 20 images download out of 40 total,
    # the line will read "20/40"
    print(str(i + 1) + "/" + str(len(df.index)))