# This is a script that can be used to rasterize the base clumu x mukey map, using a field of choice
# that is present in the attributes table (because it was joined to the feature class in a preceding step)

# The arguments noted below as sys.argv[1] and sys.argv[2] are passed in a cmd script
# (e.g., "SubfieldDNDC01_reproject_join.cmd")
# They refer to the two files, the Iowa subfield feature class and the txt file containing the
# attributes (profit and DNDC data)

import sys
print "Running script against: {}".format(sys.version)
import arcpy
from arcpy import env
from arcpy.sa import *  #spatial analyst extension

# arguments:

# sys.argv[1] is the clumu feature class in the database "ia_clumu_2016_single"
# sys.argv[2] is the value field that should be used in the raster layer, e.g. "ave_n_loss_change_perc_10000"
# sys.argv[2] is the name of the raster layer, e.g., "N_loss_reduction"

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

# starting with the feature class, I create rasters for the different variable to be able to visualize
# the differences within the whole state.

# create a feature layer from the input feature class 
print("")
print("Creating a feature layer...")
in_features = sys.argv[1]
out_layer = str(in_features) + "_layer"
arcpy.MakeFeatureLayer_management(in_features, out_layer)


# convert the feature layer to a raster containing the 2015 profit data.
print("")
print("Creating raster...")
value_field = sys.argv[2]
out_raster = sys.argv[3]
cellsize = 10
arcpy.PolygonToRaster_conversion(out_layer, value_field, out_raster, cellsize = cellsize)

# clean up in memory layer
arcpy.Delete_management(out_layer)

print("")
print("Done. Yippie!")





