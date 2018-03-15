## ---------- BEGIN README ---------- ##

#The purpose of this script is to mosaic statistical parameter raster tiles that were created by TIFFS.exe.

#Optimized for: 
#ArcMap 10.4.1
#Python 2.7 with IDLE (included in the ArcMap package) 

#To run:
#1. Open MosaicStatOutputs.py in IDLE (Python GUI) and change user inputs as necessary.
#2. Save the file.
#3. Run the script by pressing F5 or clicking the "Run" button. 

#Brandyn Balch, Graduate Research Assistant
#West Virginia University, Department of Geology and Geography, Remote Sensing Lab
#Spring, 2018

## ---------- END README ---------- ##

#Import modules: 
import arcpy
import glob
import os

## ---------- BEGIN USER INPUTS ---------- ##

#SET WORKSPACE (should be the same workspace folder used for the TIFFS outputs you are mosaicing)
arcpy.env.workspace = "C:/Users/bbalch/Desktop/PineBarrensLiDARData/2011Workspace"

#SET INPUT FOLDER (the folder in your workspace containing the tiles that need to be mosaiced. ex: trees_upper, trees, trees_lower, etc.)
InputFolder = "trees_lower"

#SET OUTPUT FOLDER (the folder in your workspace to which mosaics will be saved. ex: mosaic, stat_outputs, etc.) 
OutputFolder = "mosaic_lower/test" 

#SET YEAR (for output naming) 
Year = 2011

#SET HEIGHT BINS
NumberofBins = 25   #The number of bins that were generated (ex. 25). 
BinIncrement = 1    #The height increment for each bin (ex. 1) 

#SET PERCENTAGE BINS
pctIncrement = 10

#ARE YOU PROCESSING "allReturns" OR "firstReturnsOnly" ? (Type precisely as in quotes) 
returns = "allReturns"

#SET OVERWRITE PREFERENCE (ex: True, False)
arcpy.env.overwriteOutput = True

## ---------- END USER INPUTS ---------- ##

#Set the arcpy workspace as the Python working directory.
os.chdir(arcpy.env.workspace)

## ---------- BEGIN MOSAIC SCRIPTS ---------- ##

#Define function 

def MosaicStats(RasterInputs, output):
    arcpy.MosaicToNewRaster_management(RasterInputs,
                            OutputFolder,
                            output,
                            arcpy.SpatialReference("WGS 1984 UTM Zone 18N"),
                            "32_BIT_FLOAT",
                            "10",
                            "1",
                            "FIRST",
                            "FIRST")
    arcpy.CalculateStatistics_management("./" + OutputFolder + "/" + output)    

#Count, kurtosis, quadMean, skewness, std, mean

metriclist = ["count", "kurtosis", "quadMean", "skewness", "std", "mean"]
while len(metriclist) > 0:
    metric = metriclist[0]
    MosaicStats(glob.glob("./" + InputFolder + "/*_" + metric + "_" + returns + ".tif"),
                str(Year) + "_mosaic_" + metric + "_" + returns + ".tif")
    del metriclist[0]

#Height bins

BinLower = 0
BinUpper = BinLower + BinIncrement
while BinUpper <= NumberofBins:
    MosaicStats(glob.glob("./" + InputFolder + "/*_htBin" + str(BinLower) + "to" + str(BinUpper) + "_" + returns + ".tif"),
                str(Year) + "_mosaic_htBin" + str(BinLower) + "to" + str(BinUpper) + "_" + returns + ".tif")
    BinLower = BinLower + BinIncrement
    BinUpper = BinUpper + BinIncrement

#Percentages

pct = 0 + pctIncrement
while pct <= 100:
    MosaicStats(glob.glob("./" + InputFolder + "/*_pct" + str(pct) + "_" + returns + ".tif"),
                            str(Year) + "_mosaic_pct" + str(pct) + "_" + returns + ".tif")            
    pct = pct + pctIncrement

## ---------- END MOSAIC SCRIPTS ---------- ##

