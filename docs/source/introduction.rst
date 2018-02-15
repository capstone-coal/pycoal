.. # encoding: utf-8
   #
   # Copyright (C) 2017 COAL Developers
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
   
Introduction
************

COAL is a Python library for processing hyperspectral imagery from remote sensing devices such as the Airborne Visible/InfraRed Imaging Spectrometer (AVIRIS). COAL is being developed as a 2016 – 2017 senior capstone collaboration between scientists at the Jet Propulsion Laboratory (JPL) and computer science students at Oregon State University (OSU). COAL aims to provide a suite of algorithms for classifying land cover, identifying mines and other geographic features, and correlating them with environmental data sets. COAL is Free and Open Source Software under the terms of the GNU GENERAL PUBLIC LICENSE, Version 2.

================
What is COAL?
================
COAL provides a suite of algorithms and a command line interface (all written in Python) to identify, classify, characterize, and quantify (by reporting a number of key metrics) the direct and indirect impacts of MTM and related destructive surface mining activities across the continental U.S.A (and further afield).

================
Dependencies
================
* `Spectral Python <http://www.spectralpython.net/>`_: needed for the mineral classification and mining identification APIs.
* `NumPy <http://www.numpy.org/>`_: needed for the mineral classification and mining identification APIs.
* `GDAL <http://www.gdal.org/>`_: needed for the GIS processing API.

More information on COAL can be seen at the `project Website <https://capstone-coal.github.io/>`_ as well as the `docs directory <https://github.com/capstone-coal/pycoal/tree/master/docs>`_.
