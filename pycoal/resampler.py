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
from spectral.algorithms.resampling import build_fwhm, normal_integral
from spectral.algorithms.resampling import overlap, ranges_overlap
import numpy


def create_resampling_matrix(centers1, centers2):
    """
    Returns a resampling matrix to convert spectra from one band discretization
    to another.  Arguments are the band centers and full-width half maximum
    spectral response for the original and new band discretizations.
    """
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

    n_centers1 = len(centers1)
    n_centers2 = len(centers2)
    bounds1 = [[centers1[i] - fwhm1[i] / 2.0, centers1[i] + fwhm1[i] /
                2.0] for i in range(n_centers1)]
    bounds2 = [[centers2[i] - fwhm2[i] / 2.0, centers2[i] + fwhm2[i] /
                2.0] for i in range(n_centers2)]

    shape = numpy.zeros([n_centers2, n_centers1])

    j_start = 0
    nan = float('nan')
    for i in range(n_centers2):
        stdev = fwhm2[i] / sqrt_8log2
        j = j_start

        # Find the first original band that overlaps the new band
        while j < n_centers1 and bounds1[j][1] < bounds2[i][0]:
            j += 1

        if j == n_centers1:
            print(('No overlap for target band %d (%f / %f)' % (
                i, centers2[i], fwhm2[i])))
            shape[i, 0] = nan
            continue

        matches = []

        # Get indices for all original bands that overlap the new band
        while j < n_centers1 and bounds1[j][0] < bounds2[i][1]:
            if ranges_overlap(bounds1[j], bounds2[i]):
                matches.append(j)
            j += 1

        # Put NaN in first element of any row that doesn't produce a band in
        # the new schema.
        if not matches:
            print(('No overlap for target band %d (%f / %f)' % (
                i, centers2[i], fwhm2[i])))
            shape[i, 0] = nan
            continue

        # Determine the weights for the original bands that overlap the new
        # band. There may be multiple bands that overlap or even just a single
        # band that only partially overlaps.  Weights are normoalized so either
        # case can be handled.

        overlaps = [overlap(bounds1[k], bounds2[i]) for k in matches]
        contribs = numpy.zeros(len(matches))
        count = 0.
        for k in range(len(matches)):
            (first, second) = [(x - centers2[i]) / stdev for x in overlaps[k]]
            integral = normal_integral(first, second)
            contribs[k] = integral
            count += integral
        contribs = contribs / count
        for k in enumerate(matches): #range(len(matches)):
            shape[i, matches[k[0]]] = contribs[k[0]]
    return shape
