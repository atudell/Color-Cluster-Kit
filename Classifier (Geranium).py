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
# data is the number to compare
# the lower_bin is the lower value of the color bin
# the upper_bin is the upper value of the color bin
# If the data is lower than the lower_bin, it classifies as light
# If the data is higher than the upper_bin, it classifies as dark
# Anything in between the upper and lower bins (inclusive) classifies as medium
# For example if data = 5, lower_bin = 4, upper_bin = 6, the functions will return "medium"
def classify (data, lower_bin, upper_bin):
    
     # If the data column didn't pick up flowers, just return 0 for the values
    if data == 0:
        return 0
    
    # If the data is lower than the lower bin, it's light
    if data < lower_bin:
        return "light"
    # If the data is higher than the upper bin, it's dark
    elif data > upper_bin: 
        return "dark"
    # If it's neither of those cases, the color must be between the upper and lower bounds, so it's medium
    else:
        return "medium"
        
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

# This creates a new column in the dataframe that extracts the saturation value from the K-Means Clustering data
df["Saturation"] = df["KMeansData"].apply(lambda x: parse_data(x, 1))

# This creates a new column in the dataframe that classifies each observation as "light", "medium", and "dark"
# based on the rules described in the function
# Note that the example values are the upper and lower bounds of the saturation for Geranium
df["Classification"] = df["Saturation"].apply(lambda x: classify(x, 70.5828523, 92.75856618))

# Finally, the code is saved to a csv file locally
# Use just a file name to save it in the same directoty
# Use an absolute path to save it to some other location in the system
df.to_csv("FlowerClassifications(Geranium).csv")