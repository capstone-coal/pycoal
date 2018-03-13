# Copyright (C) 2017-2018 COAL Developers
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

# Use an official Python runtime as a base image (host debian:jessie)
FROM python:3-slim

MAINTAINER COAL Developers <coal-capstone@googlegroups.com>

RUN echo "deb     http://qgis.org/debian jessie main" >> /etc/apt/sources.list
RUN echo "deb-src http://qgis.org/debian jessie main" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 073D307A618E5811
# dput breaks Docker build
RUN printf "Package: dput\nPin: origin \"\"\nPin-Priority: -1" >> /etc/apt/preferences
#RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable

# Install the dependencies
RUN apt-get update && \
	apt-get upgrade -y --force-yes && \
	apt-get install -y --force-yes apache2 \
		bash-completion \
		bison \
		checkinstall \
		cmake \
		devscripts \
		doxygen \
		flex \
		git \
		graphviz \
		grass-dev \
		libexpat1-dev \
		libfcgi-dev \
		libgdal-dev \
		libgeos-dev \
		libgsl0-dev \
		libopenscenegraph-dev \
		libosgearth-dev \
		libpq-dev \
		libproj-dev \
		libqt4-dev \
		libqt4-opengl-dev \
		libqtwebkit-dev \
		libqwt-dev \
		libspatialindex-dev \
		libspatialite-dev \
		libsqlite3-dev \
		pkg-config \
		pkg-kde-tools \
		pyqt4-dev-tools \
		python-all \
		python-all-dev \
		python-qgis \
		python-qt4 \
		python-qt4-dev \
		python-sip \
		python-sip-dev \
		qgis \
		qgis-plugin-grass \
		txt2tags \
		wget \
		xauth \
		xfonts-100dpi \
		xfonts-75dpi \
		xfonts-base \
		xfonts-scalable xvfb

# Download GDAL
RUN wget http://download.osgeo.org/gdal/CURRENT/gdal-2.2.3.tar.gz && \
	tar zxvf gdal-2.2.3.tar.gz && \
	cd gdal-2.2.3 && \
	./configure && \
	make && \
	make install && \
	ldconfig && \
	# Test
	gdalwarp --version

# Set the working directory to /coal
WORKDIR /coal

# Copy the current directory contents into the container at /coal
ADD . /coal

# Install pycoal from source, ensures we always use the latest development branch
RUN python setup.py install
