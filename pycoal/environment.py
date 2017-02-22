#!/usr/bin/env python

import coal

def correlateMiningEnvironment(environmentFilename, miningFilename, outputFilename):

    """
    Correlate environmental impact GIS data with classified mines and save the result to a file.
    """

    # define function to select the environmental impact layer
    def impactLayer(environmentDataset):

        ???

        return impactDataset

    # define raster function to correlate environmental impact with classified mines
    def correlate(impactDataset, miningDataset, outputDataset):

        ???

    # apply the correlation and save the result
    coal.gis.combine(correlate, impactLayer, environmentFilename, miningFilename, outputFilename)
