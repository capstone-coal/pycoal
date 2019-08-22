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

# Use an official Python runtime as a base image (host debian:jessie)
FROM python:3.7-slim

MAINTAINER COAL Developers <coal-capstone@googlegroups.com>

# Build-time metadata as defined at http://label-schema.org
# This means we get badges through MicroBadger
ARG BUILD_DATE
ARG VCS_REF
LABEL org.label-schema.build-date=$BUILD_DATE \
	org.label-schema.name="Coal and Open-pit surface mining impacts on American Lands (COAL)" \
	org.label-schema.description="Python library for processing hyperspectral imagery from the Airborne Visible/InfraRed Imaging Spectrometer (AVIRIS). COAL provides a suite of algorithms for classifying land cover, identifying mines and other geographic features, and correlating them with environmental data sets." \
	org.label-schema.url="https://capstone-coal.github.io/" \
	org.label-schema.vcs-ref=$VCS_REF \
	org.label-schema.vcs-url="https://github.com/capstone-coal/pycoal" \
	org.label-schema.vendor="Capstone Coal" \
	org.label-schema.schema-version="1.0"

# Install the dependencies
RUN apt-get update && \
	apt-get upgrade -y --allow-downgrades --allow-remove-essential --allow-change-held-packages && \
	apt-get install -y --allow-downgrades --allow-remove-essential --allow-change-held-packages apache2 \
		apt-utils \
		bash-completion \
		bison \
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
		libopenscenegraph-3.4-dev \
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

RUN echo "deb     http://qgis.org/debian jessie main" >> /etc/apt/sources.list
RUN echo "deb-src http://qgis.org/debian jessie main" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 073D307A618E5811
# dput breaks Docker build
RUN printf "Package: dput\nPin: origin \"\"\nPin-Priority: -1" >> /etc/apt/preferences
#RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt-get install gdal-bin #2.4.2+dfsg-1

# Download GDAL
#ENV GDAL_VERSION 3.0.1
#RUN wget http://download.osgeo.org/gdal/$GDAL_VERSION/gdal-$GDAL_VERSION.tar.gz && \
	#tar zxvf gdal-$GDAL_VERSION.tar.gz && \
	#cd gdal-$GDAL_VERSION && \
	#./configure && \
	#make && \
	#make install && \
	#ldconfig && \

# Test
RUN gdalwarp --version

# Set the working directory to /coal
WORKDIR /pycoal

# Copy the current directory contents into the container at /coal
ADD . /pycoal

# Install pycoal from source, ensures we always use the latest development branch
RUN python3 setup.py install
