# All the imports from the sklearn module are statistical tools to help perform K-Means Clustering
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
# Imports the webbrowser module which will open a new tab
import webbrowser
# imports pandas and numpy, two important libraries for data manipulation
import pandas as pd
import numpy as np
# imports cv2, a computer vision library to help manipulate images
import cv2
# imports os, or operating system which will help perform system specific operations
import os

# A function that receives an image path and number of clusters k and returns a dictionary of clusters and values
def image_summary(image_source, k):
    
    # Load image
    image = cv2.imread(image_source)
        
    # Convert image to the HSV color space
    image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    # By default, images are stored as 3D objects with a width and height defined by the image resolution
    # In addition, each pixel stores three pieces of information pertaining to color, in this case, H, S, and V
    # Mathematrical operations on this 3D object is cumbersome and inefficient, so the flatten() method
    # turns it into a 2D array for quicker operations.
    # The first three values in the 2D array correspond with the 3 color values in the top-left pixel
    # The next three values correspond with the 3 color values in next pixel to the right, etc.
    # For example, the data structure of an image typically look like this:
    # [[[1,2,3], [4,5,6]],
    # [[7,8,9], [10,11,12]]
    # The flatten argument transforms it to this:
    # [1,2,3,4,5,6,7,8,9,10,11,12]
    image_flat = image_hsv.flatten()

    # Because of how the image is flatten, we know that the H, S, and V values reoccur at every third pixel
    # at a slight different index i.e. All H values are at the 0th place, 3rd place, 6th place, 9th place and so on
    # We take advantage of this to collect all the H, S, and V values into single variables
    
    # The h-channel. Takes every 3rd value from flatten image starting at 0th place
    h = image_flat[0::3]
    # The s-channel. Takes every 3rd value from flatten image starting at 1st place
    s = image_flat[1::3]
    # The v-channel. Takes every 3rd value from flatten image starting at 2nd place
    v = image_flat[2::3]

    # Create a dataframe from the pixel values
    df = pd.DataFrame(data = h, columns = ["h"])
    df['s'] = s
    df['v'] = v

    # H, S, and V values are at different scales. H values vary from 0-179 and S and V vary from 0-255
    # Consequently, any clustering based on a geometric distance will be skewed
    # To remedy this, the StandScaler() function brings everything onto a standard scale
    
    # initialize scaler
    scaler = StandardScaler()

    # Scaled features
    scaler.fit(df)
    df_scaled = scaler.transform(df)

    # These two lines actually perform the K-Means clustering. Note that k is the same k passed in the initial argument
    kmeans = KMeans(n_clusters = k)
    kmeans.fit(df_scaled)

    # Create a new column in the dataframe for the labels
    # The labels themselves are simple numeric values that denote which pixels go into which cluster
    # (ie, all pixels labeled as 1 are in the same cluster)
    df["cluster"] = kmeans.labels_

    # create an empty dictionary to store summary values
    colors = {}

    # Iterate through the clusters, calculates the summary stats, and saves a masked image
    for i in range(k):

        # filter the dataframe by cluster
        df_filter = df[df["cluster"] == i]

        # Calculates the summary stats. By default, the average is taken. If these need to change, this is the 
        # place to do it. Note that using the numpy library for calulations generally yield faster results
        # The summary states are then stored in the dictionary.
        colors["cluster " + str(i)] = [
            np.mean(df_filter["h"]), 
            np.mean(df_filter["s"]), 
            np.mean(df_filter["v"])
        ]

        # create a "mask" based on the labels. This is basically the array that will dictate whether or not a pixel
        # will be displayed in the image
        detect = np.array([1 if x == i else 0 for x in kmeans.labels_], dtype='uint8')
        
        # reshape the mask into the dimensions of the picture
        dims = image_hsv.shape
        detect = detect.reshape(dims[0], dims[1])
        
        # Create a copy of the image
        image_copy = image_hsv
        
        # create the masked image
        output = cv2.bitwise_and(image_copy, image_copy, mask = detect)
        
        # Convert back to rgb for better visualization
        output = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
        
        # save the image locally
        cv2.imwrite("image_cluster_" + str(i) + ".jpg", output)

    # Finally return the colors dictionary
    return colors
    
# takes a list of hsv values and converts it to the RGB colorspace.
# This is purely a utility function that becomes useful later
def hsv_to_rgb(hsv_vals):
    
    # round the the values
    h = round(hsv_vals[0], 0)
    s = round(hsv_vals[1], 0)
    v = round(hsv_vals[2], 0)
    
    # To convert with openCV's rules, a simple one pixel "image" is created
    image = [
        [
            [h, s, v]
        ]
    ]
    
    # convert to BGR colorspace
    image = cv2.cvtColor(np.uint8(image), cv2.COLOR_HSV2BGR)
    
    # Get the pixel values in an array
    pixel = image[0][0]
    
    # Because openCV stores it as a BGR, the reverse is stored in a list and returned for the traditional RGB format
    return [pixel[2], pixel[1], pixel[0]]
    
# takes a path and number of clusters k and creates an html file with the summary statistics and sample color 
# Note that a html file is the basic bare-bones component to a static website. This provides a useful frame work
# for displaying data and information in an organized way. If running this on Jupyter Notebooks, the web browswer
# will be open anyway and will open a new tab to render the html file
def get_summary_visual(path, k):
    
    # Get the photo data
    summary = image_summary(path, k)
    
    # write the start of the html file
    start = """
<!DOCTYPE html>

<html>

    <body>
        <h>Image Summary</h>
        <br>
    """
    
    # start the body of the html as a blank
    body = ""
    
    # For each entry in the summary (ie, that colors dictionary from the image_summary() function), 
    # add the details to the html file
    for key in summary:    
        
        # The hsv values stored in a nice variable
        hsv_cluster = summary[key]
        
        # Convert the hsv values into RGB values
        rgb_cluster = hsv_to_rgb(hsv_cluster)
        
        # Concat the body of the html and use f-strings to "fill in blanks" for key summary statistics
        body = body + f"""      
        <p>{key}</P>
        <p>Average H: {hsv_cluster[0]}</p>
        <p>Average S: {hsv_cluster[1]}</P>
        <p>Average V: {hsv_cluster[2]}</p>
        <div style ="background-color:rgb({rgb_cluster[0]},{rgb_cluster[1]},{rgb_cluster[2]});height: 50px;width: 50px;" ></div>
        <img src = "image_cluster_{key[8:]}.jpg">
        <br>
        """
    
    # Write a closing
    end = """
    </body>
</html>
    """
    
    # Right now, all the components to the HTML file are in separate varaibles
    # Concat all the elements together into a single, cohesive html document
    html = start + body + end
    
    # write the html locally
    with open("image_summary.html", 'w') as file:
        file.write(html)
    
    # Get the working directory, so the user doesn't have to manually configure the path to the file
    cwd = os.getcwd()
    
    # Geth the absolute path
    path = cwd + "\\" + "image_summary.html"
    
    # open the html file in the webbrowser
    webbrowser.open(path, new=2)
    
# This is the point where user input is required!!

# All the code above supports this single line
# The first argument is the path to the file of interest
# Note that "\" is a break character that interferes with how strings of text are read
# Consequently, add the letter "r" in front of the destination name to avoid issues with parsing text
# The second argument is K, used for K-Means clustering
# Depending on the size of the image and the value k, this may take several minutes to complete
# Generally, larger images and larger values of K take longer to complete
get_summary_visual(r"C:\Users\Example\FlowerClassification\Observations\123.jpg", 5)
