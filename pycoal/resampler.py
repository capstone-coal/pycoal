# Copyright (C) 2017-2019 COAL Developers
#
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; version 2.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty 
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public 
# License along with this program; if not, write to the Free 
# Software Foundation, Inc., 51 Franklin Street, Fifth 
# Floor, Boston, MA 02110-1301, USA.

# Adapted from Spectral Library: resampling.py
# https://github.com/spectralpython/spectral/blob/master/spectral/algorithms/resampling.py

from spectral.spectral import BandInfo
from spectral.algorithms.resampling import *
from math import erf
import math
import numpy

def create_resampling_matrix(centers1, centers2):
    '''
    Returns a resampling matrix to convert spectra from one band discretization
    to another.  Arguments are the band centers and full-width half maximum
    spectral response for the original and new band discretizations.
    '''
    fwhm1 = None	
    fwhm2 = None
    if isinstance(centers1, BandInfo):
        fwhm1 = centers1.bandwidths
        centers1 = centers1.centers
    if isinstance(centers2, BandInfo):
        fwhm2 = centers2.bandwidths
        centers2 = centers2.centers
    if fwhm1 is None:
        fwhm1 = build_fwhm(centers1)
    if fwhm2 is None:
        fwhm2 = build_fwhm(centers2)

    sqrt_8log2 = 2.3548200450309493

    N1 = len(centers1)
    N2 = len(centers2)
    bounds1 = [[centers1[i] - fwhm1[i] / 2.0, centers1[i] + fwhm1[i] /
                2.0] for i in range(N1)]
    bounds2 = [[centers2[i] - fwhm2[i] / 2.0, centers2[i] + fwhm2[i] /
                2.0] for i in range(N2)]

    M = numpy.zeros([N2, N1])

    jStart = 0
    nan = float('nan')
    for i in range(N2):
        stdev = fwhm2[i] / sqrt_8log2
        j = jStart

        # Find the first original band that overlaps the new band
        while j < N1 and bounds1[j][1] < bounds2[i][0]:
            j += 1

        if j == N1:
            print(('No overlap for target band %d (%f / %f)' % (
                i, centers2[i], fwhm2[i])))
            M[i, 0] = nan
            continue

        matches = []

        # Get indices for all original bands that overlap the new band
        while j < N1 and bounds1[j][0] < bounds2[i][1]:
            if ranges_overlap(bounds1[j], bounds2[i]):
                matches.append(j)
            j += 1

        # Put NaN in first element of any row that doesn't produce a band in
        # the new schema.
        if len(matches) == 0:
            print(('No overlap for target band %d (%f / %f)' % (
                i, centers2[i], fwhm2[i])))
            M[i, 0] = nan
            continue

        # Determine the weights for the original bands that overlap the new
        # band. There may be multiple bands that overlap or even just a single
        # band that only partially overlaps.  Weights are normoalized so either
        # case can be handled.

        overlaps = [overlap(bounds1[k], bounds2[i]) for k in matches]
        contribs = numpy.zeros(len(matches))
        A = 0.
        for k in range(len(matches)):
            #endNorms = [normal(centers2[i], stdev, x) for x in overlaps[k]]
            #dA = (overlaps[k][1] - overlaps[k][0]) * sum(endNorms) / 2.0
            (a, b) = [(x - centers2[i]) / stdev for x in overlaps[k]]
            dA = normal_integral(a, b)
            contribs[k] = dA
            A += dA
        contribs = contribs / A
        for k in range(len(matches)):
            M[i, matches[k]] = contribs[k]
    return M
