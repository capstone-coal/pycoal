'''
    Module Dependencies
        torch:
        torch.nn
        Dataset
        Dataloader
'''
import torch
import torch.nn as nn
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

print("Parallel in Library")
'''
    Check
        Purpose: To check if there are multiple GPUs available to use, if there are then we wrap the model with DataParallel, otherwise we don't
        Input:
            model: A model of the data we use
        Output: 
            model: A wrapped model with DataParallel, or the original model
'''
def check(model):
    if torch.cuda.device_count() > 1:
        model = nn.DataParallel(model)

    return model

'''
    Dataset class
'''
class ImageDataSet(Dataset):
    def __init__(self, x, y, image, resample, classified, scored):
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
    def get(self, x):
        image = torch.from_numpy(self.image)
        #resample = torch.from_numpy(self.resample[:,x])
        #classified = torch.from_numpy(self.classified[:,x])
        #scored = torch.from_numpy(self.scored[:,x])

        #return torch.cat((image,resample,classified,scored),1)
        
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
        super().__init__()
        self.conv1 = nn.Conv2d(963, 128, kernel_size=3, padding=1)
        pass
    '''
	# variables needed: data
        self.M = dataClass.M
        self.N = dataClass.N
        self.newData = dataClass.image
        self.newResample = dataClass.resample
        self.newClassified = dataClass.classified
        self.newScored = dataClass.scored
    '''

    def innerLoop(pixel, classified, scored):
        classified = 0
        scored  = 0

       	# Resample the Data
        angle_data = torch.einsum('ij,j->i', resampling_matrix, pixel)
        angle_data[angle_data != angle_data] = 0

        # calculate spectral angles: adapted from spectral.spectral_angles
        dots = torch.einsum('i,ji->j', angle_data, m) / torch.norm(angle_data)
        angles = torch.acos(torch.clamp(dots, -1, 1))

        # normalize confidence values from [pi,0] to [0,1]
        angles = ((angles / math.pi) * -1) + 1

        # get index of class with largest confidence value
        score,index_of_max = torch.max(angles, 0)

        # classify pixel if confidence above threshold
        if score > threshold:

            # index from one (after zero for no data)
            classified = index_of_max + 1

            if scores_file_name is not None:
                # store score value
                scored = score

        return classified, scored

    def forward(self, pixel, classified, scored):
        return innerLoop(pixel, classified, scored)

'''

'''
def run():
    return
