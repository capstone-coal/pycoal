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

# Use an official Python runtime as a base image (host debian:jessie)
FROM python:2-slim

MAINTAINER pycoal developers <coal-capstone@googlegroups.com>

RUN echo "deb     http://qgis.org/debian jessie main" >> /etc/apt/sources.list
RUN echo "deb-src http://qgis.org/debian jessie main" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 073D307A618E5811
# dput breaks Docker build
#RUN printf "Package: dput\nPin: origin \"\"\nPin-Priority: -1" >> /etc/apt/preferences

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
		xauth \
		xfonts-100dpi \
		xfonts-75dpi \
		xfonts-base \
		xfonts-scalable xvfb

# Build GDAL from source with minimized drivers
WORKDIR /usr/local
ENV GDAL_PREFIX /usr/local/gdal_build
RUN git clone https://github.com/OSGeo/gdal.git && \
	cd gdal/gdal && \
	git checkout --track origin/2.2 && \
	./configure \
    	--prefix=$GDAL_PREFIX \
    	--with-geos \
    	--with-geotiff=internal \
    	--with-hide-internal-symbols \
    	--with-libtiff=internal \
    	--with-libz=no \
    	--with-python \
    	--with-threads \
    	--without-bsb \
    	--without-cfitsio \
    	--without-cryptopp \
    	--without-curl \
    	--without-ecw \
    	--without-expat \
    	--without-fme \
    	--without-freexl \
    	--without-gif \
    	--without-gif \
    	--without-gnm \
    	--without-grass \
    	--without-grib \
    	--without-hdf4 \
    	--without-hdf5 \
    	--without-idb \
    	--without-ingres \
    	--without-jasper \
    	--without-jp2mrsid \
    	--without-jpeg \
    	--without-kakadu \
    	--without-libgrass \
    	--without-libkml \
    	--without-libtool \
    	--without-mrf \
    	--without-mrsid \
    	--without-mysql \
    	--without-netcdf \
    	--without-odbc \
    	--without-ogdi \
    	--without-openjpeg \
    	--without-pcidsk \
    	--without-pcraster \
    	--without-pcre \
    	--without-perl \
    	--without-pg \
    	--without-php \
   		--without-png \
    	--without-qhull \
    	--without-sde \
    	--without-sqlite3 \
    	--without-webp \
    	--without-xerces \
    	--without-xml2 && \
	make && \
	checkinstall && \
	export PATH=$GDAL_PREFIX/bin:$PATH && \
	export LD_LIBRARY_PATH=$GDAL_PREFIX/lib:$LD_LIBRARY_PATH && \
	export GDAL_DATA=$GDAL_PREFIX/share/gdal && \
	# Test
	gdalwarp --version

# Set the working directory to /coal
WORKDIR /coal

# Copy the current directory contents into the container at /coal
ADD . /coal

# Install pycoal from source, ensures we always use the latest development branch
RUN python setup.py install