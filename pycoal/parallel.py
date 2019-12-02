'''
    Module Dependencies
        torch:
        torch.nn
        Dataset
        Dataloader
'''
import torch
import torch.nn as nn
from torch.autograd import Function

import pycoal
from torch.utils.data.dataset import Dataset
import numpy
#from torch.utils.data import Dataloader

import spectral
import time
import fnmatch
import shutil
import math
import sys
import os

'''
    Custom function that will perform the operations on given pixel
''' 
class LinearFunction(Function):
    '''
        ctx is a context object that is typically used to save data that will be needed for the backward
        pass, but in this application it is used to store needed data like:
            1. Given data
            2. Given resampling_matrix
    '''
    @staticmethod
    def forward(x, y, data, resampling_matrix, classified, scored):
        
        # read the pixel from the file
        pixel = data[x, y]

        # if it is not a no data pixel
        if not numpy.isclose(pixel[0], -0.005) and not pixel[0] == -50:

            # resample the pixel ignoring NaNs from target bands that
            # don't overlap

            # TODO fix spectral library so that bands are in order
            resample_data = numpy.einsum('ij,j->i', resampling_matrix, pixel)
            resample_data = numpy.nan_to_num(resample_data)

            # calculate spectral angles
            # Adapted from Spectral library
            norms = numpy.sqrt(numpy.einsum('i,i->', resample_data, resample_data))
            dots = numpy.einsum('i,ji->j', resample_data, ang_m)
            dots = numpy.clip(dots / norms, -1, 1)
            angles = numpy.arccos(dots)

            # normalize confidence values from [pi,0] to [0,1]
            angles = 1 - angles / math.pi

            # get index of class with largest confidence value
            classified[x, y] = numpy.argmax(angles)

            # get confidence value of the classified pixel
            scored[x, y] = angles[classified[x, y]]

        return classified[x,y], scored[x,y]

    # This is typically for the gradient formula. Since we don't need a gradient for this project, we will be returning None
    @staticmethod
    def backward():
        return None


'''

'''
def data_parallel(resampling_matrix, data, classified, scored):
    # Get the number of available GPUs on device
    deviceNum = torch.cuda.device_count()
    # Create model
    model = ImageParallelModel()

    # Check if more than one GPU is available
    if deviceNum > 1:
        model = nn.DataParallel(mode, device_ids=range(0,deviceNum))

    return model(resmapling_matrix, data, classified, scored)

'''
    Data Model
        Purpose: To utilize torch's parallelization modules for processing images
        Input: input size (input_size), output size (output_size)
        Output:   
'''
class ImageParallelModel(nn.Module):
    '''
        This is where all used models are instantiated
    '''
    def __init__(self):
        super(ImageParallelModel, self).__init__()
        self.func = LinearFunction()

    def forward(self, resampling_matrix, data, classified, scored):
        for x in range(0, data.get_shape()[0].value):
            for y in range(0, data.get_shape()[1].value):
                classified[x,y], scored[x,y] = self.func(x,y,data,resampling_matrix, classified, scored)       

        return classified, scored


'''
    Dataset class
'''
class ImageDataSet(Dataset):
    def __init__(self, x, y, image, classified, scored):
        self.x = x
        self.y = y
        self.image = image
        self.classified = classified
        self.scored = scored
        self.resample = resample

        return
    def __len__(self):
        return self.x
    # Returns tensor column 
    def __get__(self, x,y):
        data = torch.narrow(self.image, 0, x, y - x)
        classified = torch.narrow(self.classified, 0, x, y - x)
        scored = torch.narrow(self.scored, 0, x, y - x)

        return (data, classified, scored)
        
