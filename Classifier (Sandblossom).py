# imports pandas and numpy, two important libraries for data manipulation
import numpy as np
import pandas as pd

# Create a function to parse the Kmeans Data
# As the data is output in the csv file, its a string, formatted as "[number, number, number]"
# This function takes the string as the data argument and uses the place to return the corresponding number
# For example, if the data = "[1, 2, 3]" and the place = 0, the function will return 1
def parse_data (data, place):
    
    # If the data column didn't pick up flowers, just return 0 for the values
    if data == "no flowers":
        return 0

    # Use splicing to get rid of square brackets and split by a comma and space
    data = data[1:-1].split(", ")

    # return an item from the list, based on the specified index
    return float(data[place])
    
# Define a function to make an assignment 
# This function assumes a simple single variable classification
# pixels are the number of pixels detected in the data
# threshold is the number of pixels detected in order to be classified in a certain group
# Note that because this dataset assumes there is an flower in each image, there's no consideration
# for images with no flowers
def classify(pixels, threshold):
    
    # If less than the threshold number of blue pixels are detected (or none are), then the image is assumed white
    if pixels <= threshold:
        return "White"
    # If more than the threshold number of bluw pixels are detected, then the image is classified as blue
    else:
        return "Blue"
        
# Read data from a CSV file and stores it into a dataframe
# Like the destination, an "r" should be added in front path
# This may be either an absolute path (recommended for beginners) or a relative path, depending on how the file is saved
# Note: most of the time, no further arguments are required. Sometimes, though, there will be encoding issues
# The most common fix is to add an argument, "encoding", using either:
# encoding = 'utf-8'
# encoding = 'latin1', 
# encoding = 'iso-8859-1',
# encoding = 'cp1252'
df = pd.read_csv(r"C:\Users\Example\FlowerClassification\YourSaveFile.csv")

# This creates a new column in the dataframe that extracts the number of pixels from the K-Means Clustering data
df["pixels"] = df["KMeansData"].apply(lambda x: parse_data(x, 2))

# This creates a new column in the dataframe that classifies each observation as "White" or "Blue"
# based on the rules described in the function
# Note that the example threshold is 3000 pixels
df["Classification"] = df["pixels"].apply(lambda x: classify(x, 3000))

# Finally, the code is saved to a csv file locally
# Use just a file name to save it in the same directoty
# Use an absolute path to save it to some other location in the system
df.to_csv("FlowerClassifications(Sandblossom).csv")