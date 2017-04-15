# pycoal

[![license](https://img.shields.io/github/license/capstone-coal/pycoal.svg?maxAge=2592000?style=plastic)](http://www.apache.org/licenses/LICENSE-2.0)
[![Build Status](https://travis-ci.org/capstone-coal/pycoal.svg?branch=master)](https://travis-ci.org/capstone-coal/pycoal)
[![PyPI](https://img.shields.io/pypi/v/pycoal.svg?maxAge=2592000?style=plastic)](https://pypi.python.org/pypi/pycoal)
[![Python Badge](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/)
[![Python Badge](https://img.shields.io/badge/python-2-blue.svg)](https://www.python.org/downloads/)
[![Launch Binder](https://img.shields.io/badge/launch-binder-e66581.svg?style=plastic)](http://mybinder.org/repo/capstone-coal/pycoal)
[![Google Group](https://img.shields.io/badge/-Google%20Group-lightgrey.svg)](https://groups.google.com/forum/#!forum/coal-capstone)
[![Documentation](https://readthedocs.org/projects/pycoal/badge/?version=latest)](http://pycoal.readthedocs.io/en/latest/)
[![Requirements Status](https://requires.io/github/capstone-coal/pycoal/requirements.svg?branch=master)](https://requires.io/github/capstone-coal/pycoal/requirements/?branch=master)
[![Code Health](https://landscape.io/github/capstone-coal/pycoal/master/landscape.svg?style=plastic)](https://landscape.io/github/capstone-coal/pycoal/master)

Coal and Open-pit surface mining impacts on American Lands

# Introduction and Context
Mountain-top Mining (MTM) is a method of open surface mining with the primary aim of exploring and exploiting coal seams present within the land and solid earth (LSE) on mountaintops. Amongst other surface mining activities, MTM is known to be an extremely destructive mining procedure predominantly limited to the spatial boundaries of the Southern Appalachians (Eastern Kentucky, West Virginia and very small sections of Virginia and Tennessee). MTM is known to have caused irreparable damage to mountain landscapes and significant immediate and longer-term damage to key streams and watersheds. Larger afield, the rest of the U.S.A has some extensive surface mining in various places for exploitation of resources such as gravel/sand, various metals, other minerals and even radioactive materials, etc. Several studies have provided important scientific understanding related to the local, regional and state-level impacts of such environmentally destructive practices, however a similar understanding on the national and continental levels are very much lacking.

# Project Motivation & Statement 
**pycoal provides a suite of algorithms (written in Python) to identify, classify, characterize, and quantify (by reporting a number of key metrics) the direct and indirect impacts of MTM and related destructive surface mining activities across the continental U.S.A (and further afield)**. 

More information on coal can be seen at the [project Website](http://capstone-coal.github.io) as well as the [docs](./docs) directory.

# Installation

From the cheeseshop

```
pip install pycoal
```
    
or from conda

```
conda install -c conda-forge pycoal
```

or from source

```
git clone https://github.com/capstone-coal/pycoal.git && cd pycoal
python setup.py install
```

# Quickstart
[![Launch Binder](https://img.shields.io/badge/launch-binder-e66581.svg?style=plastic)](http://mybinder.org/repo/capstone-coal/pycoal)

In the [examples directory](https://github.com/capstone-coal/pycoal/tree/master/examples) you can find several Jupyter notebooks with specific applications of coal. You can launch a cloud Jupyter server using binder to edit the notebooks without installing anything. Try it out!

http://mybinder.org/repo/capstone-coal/pycoal

# Documentation
PyCOAL documentation can be found at http://pycoal.readthedocs.io however you can also build documentation manually.
```
$ cd docs/source && make html
```
Documentation can then be located in ```_build/html/index.html```

# Tests
Pycoal uses the popular [nose](http://nose.readthedocs.io/en/latest/testing.html) testing framework. Tests can be run as follows
```
$ nosetests
```

# Community and Development

## Mailing list
[![Google Group](https://img.shields.io/badge/-Google%20Group-lightgrey.svg)](https://groups.google.com/forum/#!forum/coal-capstone)

To become involved or if you require help using the project request to join our project [Google Group](https://groups.google.com/forum/#!forum/coal-capstone).

## Issue Tracker
If you have issue using COAL, please log a ticket in our [issue tracker](https://github.com/capstone-coal/coal/issues).

# License
coal is licensed under the [Apache License v2.0](http://www.apache.org/licenses/LICENSE-2.0) a copy of which ships with this source code.
