.. # encoding: utf-8
   #
   # Licensed under the Apache License, Version 2.0 (the "License");
   # you may not use this file except in compliance with the License.
   # You may obtain a copy of the License at
   #
   #      http://www.apache.org/licenses/LICENSE-2.0
   #
   # Unless required by applicable law or agreed to in writing, software
   # distributed under the License is distributed on an "AS IS" BASIS,
   # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   # See the License for the specific language governing permissions and
   # limitations under the License.
   
Introduction
************

COAL is a Python library for processing hyperspectral imagery from remote sensing devices such as the Airborne Visible/InfraRed Imaging Spectrometer (AVIRIS). COAL is being developed as a 2016 – 2017 senior capstone collaboration between scientists at the Jet Propulsion Laboratory (JPL) and computer science students at Oregon State University (OSU). COAL aims to provide a suite of algorithms for classifying land cover, identifying mines and other geographic features, and correlating them with environmental data sets. COAL is Free and Open Source Software under the terms of the Apache License Version 2.0.

================
What is Pycoal?
================
pycoal provides a suite of algorithms (written in Python) to identify, classify, characterize, and quantify (by reporting a number of key metrics) the direct and indirect impacts of MTM and related destructive surface mining activities across the continental U.S.A (and further afield).

================
Dependencies
================
|`Spectral Python <http://www.spectralpython.net/>`_: needed for the mineral classification and mining identification APIs.
|`NumPy <http://www.numpy.org/>`_: needed for the mineral classification and mining identification APIs.
|`GDAL <http://www.gdal.org/>`_: needed for the GIS processing API.

More information on coal can be seen at the `project Website <https://capstone-coal.github.io/>`_ as well as the `docs directory <https://github.com/capstone-coal/pycoal/tree/master/docs>`_.
