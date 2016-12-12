

import sys
print "Running script against: {}".format(sys.version)

# the arguments noted below as sys.argv[1] and sys.argv[2] are passed in the cmd script "SubfieldDNDC01_reproject_join.cmd".
# They refer to the two files, the Iowa subfield feature class and the txt file containing the
# attributes (profit and DNDC data)

import arcpy
from arcpy import env
from arcpy.sa import *  #spatial analyst extension

# set the environment so that output data are being overwritten
arcpy.env.overwriteOutput=True
# specify the workspace to avoid having to write the path for each feature class
arcpy.env.workspace = "C:\\Users\\ebrandes\\Documents\\ia_clumu\\ia_clumu.gdb"

# starting with the feature class ia_clumu_2016_single (that I joined mean profit, no3 leaching,
# clu cash rents, and mean and 2015 profit), I create rasters for the different variable to be able to visualize
# the differences within the whole state.

# create a feature layer from the feature class "ia_clumu_2016_single"
print("")
print("Creating a feature layer...")
in_features = "ia_clumu_2016_single"
out_layer = "ia_clumu_2016_single_layer"
arcpy.MakeFeatureLayer_management(in_features, out_layer)


# convert the feature layer to a raster containing the mean profit data.
print("")
print("Creating raster with 2015 cash rent data...")
value_field = "clu_cash_rent_csr2_1"
out_raster = "cash_rent_2015"
cellsize = 10
arcpy.PolygonToRaster_conversion(out_layer, value_field, out_raster, cellsize = cellsize)

# clean up in memory layer
arcpy.Delete_management("ia_clumu_2016_single_layer")

print("")
print("Done. Yippie!")





