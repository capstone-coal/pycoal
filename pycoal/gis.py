#!/usr/bin/env python

import gdal

class GISProcessing:

    def combine(rasterFunction, selectLayers, gisFilename, classifiedFilename, outputFilename):

        """
        Combine GIS layers with a classified image using a transformation function and write the output to a file.
        """

        # TODO update docstring
        # TODO test

        # load gis
        gisDataset = gdal.Open(gisFilename, gdalconst.GA_ReadOnly)

        # load classified image
        classifiedDataset = gdal.Open(classifiedFilename, gdalconst.GA_ReadOnly)

        # select one or more layers
        # FIXME temporary dataset ?
        gisLayersDataset = selectLayers(gisDataset)

        # crop to flightline and convert to bitmap
        # FIXME temporary dataset ?
        gisRasterLayersDataset = cropSourceToDest(gisLayersDataset, classifiedDataset)

        # apply function to result dataset and write to file
        resultRasterDataset = createEmptyCopy(classifiedDataset, outputFilename)
        rasterFunction(gisRasterLayersDataset, classifiedDataset, resultRasterDataset)
        resultRasterDataset = None

    def cropSourceToDest(sourceDataset, destDataset):

        """
        Crop a vector source dataset to the same dimensions and format as a raster destination dataset.
        """

        # TODO update docstring
        # TODO test

        # get destination projection (spatial reference system)
        projection = destDataset.GetProjection()

        # get destination image size (in pixels)
        xSize = destDataset.RasterXSize
        ySize = destDataset.RasterYSize

        # get destination transform
        geotransform = destDataset.GetGeoTransform()

        # get destination pixel size
        pixelXSize = geotransform[1]
        pixelYSize = geotransform[5]

        # get destination bounding box
        minX = geotransform[0]
        maxX = minX + (xSize * pixelXSize)
        maxY = geotransform[3]
        minY = maxY + (ySize * pixelYSize)

        # set warp options
        warpOptions = gdal.WarpOptions(format=???,
                                       dstSRS=projection,
                                       width=xSize,
                                       height=ySize,
                                       outputBounds=(minX,minY,maxX,maxY))

        # TODO define resultDataset ?

        # crop source to destination dimensions and format
        gdal.Warp(resultDataset, sourceDataset, warpOptions)

        # return the result
        return resultDataset

    def createEmptyCopy(inputDataset, filename):

        """
        Return an empty dataset with the given filename and the same dimensions as the input dataset.
        """

        # TODO test

        # get driver
        driver = gdal.GetDriverByName(???) # TODO

        # copy dimensions from input dataset
        xSize = inputDataset.RasterXSize
        ySize = inputDataset.RasterYSize
        layerCount = inputDataset.GetLayerCount()
        dataType = gdal.GDT_??? # TODO

        # create output dataset
        outputDataset = driver.create(filename, xSize, ySize, layerCount, dataType)

        # copy transform and projection from input dataset
        outputDataset.SetGeoTransform(inputDataset.GetGeoTransform())
        outputDataset.SetProjection(inputDataset.GetProjection())

        # return output dataset
        return outputDataset
