======
COAL
======

**Development**

|license| |PyPI| |Python3| |GoogleGroup| |documentation| |Travis| |Coveralls| |Requirements Status| |Code Health| |Anaconda-Server Version| |Anaconda-Server Downloads|

**Docker**

|Docker Pulls| |microbadger|

COAL is a Python library for processing hyperspectral imagery from remote sensing devices such as the
`Airborne Visible/InfraRed Imaging Spectrometer (AVIRIS) <https://aviris.jpl.nasa.gov/>`__ and 
`AVIRIS-Next Generation <https://avirisng.jpl.nasa.gov/>`__ enabling scientific analysis of Coal and 
Open-pit surface mining impacts on American Lands.

Introduction and Context
------------------------
Mountain-top Mining (MTM) is a method of open surface mining with the primary aim of exploring and 
exploiting coal seams present within the land and solid earth (LSE) on mountaintops. Amongst other 
surface mining activities, MTM is known to be an extremely destructive mining procedure predominantly 
limited to the spatial boundaries of the Southern Appalachians (Eastern Kentucky, West Virginia 
and very small sections of Virginia and Tennessee). MTM is known to have caused irreparable damage 
to mountain landscapes and significant immediate and longer-term damage to key streams and watersheds. 
Larger afield, the rest of the U.S.A has some extensive surface mining in various places for 
exploitation of resources such as gravel/sand, various metals, other minerals and even radioactive 
materials, etc. Several studies have provided important scientific understanding related to the 
local, regional and state-level impacts of such environmentally destructive practices, however 
a similar understanding on the national and continental levels are very much lacking.

Project Motivation & Statement 
------------------------------
COAL provides a suite of algorithms (written in Python) to identify, classify, characterize,
and quantify (by reporting a number of key metrics) the direct and indirect impacts of 
MTM and related destructive surface mining activities across the continental U.S.A (and further afield). 

More information on COAL can be seen at the `Project Website <https://capstone-coal.github.io/>`__ 
as well as the **docs** directory.

Installation
------------

pip
^^^
|PyPI|

The Python COAL package **pycoal** can be installed from the cheeseshop

::

	pip3 install pycoal
    
conda
^^^^^
|Anaconda-Server Version| |Anaconda-Server Downloads|

or from conda

::

	conda install -c conda-forge pycoal

Source
^^^^^^

or from source

::

	git clone https://github.com/capstone-coal/pycoal.git && cd pycoal
	python3 setup.py install

Docker
^^^^^^
|Docker Pulls| |microbadger|

`Docker <https://www.docker.com/>`_ greatly simplifies installation of pycoal and the environment. 
The image can be installed from `Dockerhub <https://hub.docker.com/>`_ as follows

::

	docker pull capstonecoal/coal:latest

Additionally, if you are developing the image and wish to build it locally, you can run the following

**Installation**

1. Install `Docker <https://www.docker.com/>`_.

2. Build from files in this directory:

::

	$(boot2docker shellinit | grep export)
	docker build -t capstonecoal/coal .

**Usage**

Start docker

::

	boot2docker up
	$(boot2docker shellinit | grep export)

Start up an image and attach to it

::

	docker run -t -i -d --name coalcontainer capstonecoal/coal /bin/bash
	docker attach --sig-proxy=false coalcontainer

pycoal is located in /coal and is almost ready to run. You just need to grab some data.

Tests
-----

|Travis| |Coveralls|

COAL uses the popular `nose <http://nose.readthedocs.org/en/latest/>`__
testing suite for unit tests.

You can run the COAL tests simply by running

::

    nosetests

Additonally, click on the build sticker at the top of this readme to be
directed to the most recent build on `travis-ci <https://travis-ci.org/capstone-coal/pycoal>`__.

Quickstart
----------

See the `quickstart documentation <https://capstone-coal.github.io/docs#usage>`_.

If you would like to run the examples yourself, head over to the **examples** module.

**WARNING** Running the examples requires `additional downloads <https://github.com/capstone-coal/pycoal/tree/master/examples#aviris-ng-data>`_. Ensure you have sufficient storage (~20 GB).

Documentation
-------------

|documentation|

COAL documentation can be found at `Readthedocs <http://pycoal.readthedocs.io>`__ however you can also build documentation manually.

::

	$ cd docs/source && make html

Documentation can then be located in **_build/html/index.html**

Community and Development
-------------------------

Mailing list
^^^^^^^^^^^^

|GoogleGroup|

To become involved or if you require help using the project request to join our mailing list.

Issue Tracker
^^^^^^^^^^^^^

If you have issue using COAL, please log a ticket in our `Github issue tracker <https://github.com/capstone-coal/coal/issues>`__.

License
-------

COAL is licensed under the |license| a copy of which ships with this source code.

.. |license| image:: https://anaconda.org/conda-forge/pycoal/badges/license.svg
   :target: https://www.gnu.org/licenses/gpl-2.0.html
.. |Python3| image:: https://img.shields.io/badge/python-3-blue.svg
   :target: https://www.python.org/downloads/
.. |PyPI| image:: https://img.shields.io/pypi/v/pycoal.svg?maxAge=2592000?style=plastic
   :target: https://pypi.python.org/pypi/pycoal
.. |GoogleGroup| image:: https://img.shields.io/badge/-Google%20Group-lightgrey.svg
   :target: https://groups.google.com/forum/#!forum/coal-capstone
.. |documentation| image:: https://readthedocs.org/projects/pycoal/badge/?version=latest
   :target: http://pycoal.readthedocs.org/en/latest/
.. |Travis| image:: https://img.shields.io/travis/capstone-coal/pycoal.svg?maxAge=2592000?style=plastic
   :target: https://travis-ci.org/capstone-coal/pycoal
.. |Coveralls| image:: https://coveralls.io/repos/github/capstone-coal/pycoal/badge.svg?branch=master
   :target: https://coveralls.io/github/capstone-coal/pycoal?branch=master
.. |Requirements Status| image:: https://requires.io/github/capstone-coal/pycoal/requirements.svg?branch=master
   :target: https://requires.io/github/capstone-coal/pycoal/requirements/?branch=master
.. |Code Health| image:: https://landscape.io/github/capstone-coal/pycoal/master/landscape.svg?style=plastic
   :target: https://landscape.io/github/capstone-coal/pycoal/master
.. |Anaconda-Server Version| image:: https://anaconda.org/conda-forge/pycoal/badges/version.svg
   :target: https://anaconda.org/conda-forge/pycoal
.. |Anaconda-Server Downloads| image:: https://anaconda.org/conda-forge/pycoal/badges/downloads.svg
   :target: https://anaconda.org/conda-forge/pycoal
.. |Docker Pulls| image:: https://img.shields.io/docker/pulls/capstonecoal/coal.svg?maxAge=2592000?style=plastic
   :target: https://cloud.docker.com/swarm/capstonecoal/repository/docker/capstonecoal/coal/general
.. |microbadger| image:: https://images.microbadger.com/badges/image/capstonecoal/coal.svg
   :target: https://microbadger.com/images/capstonecoal/coal
