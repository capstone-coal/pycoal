# Use an official Python runtime as a base image (host debian:jessie)
FROM python:2-slim

MAINTAINER pycoal developers <coal-capstone@googlegroups.com>

RUN echo "deb     http://qgis.org/debian jessie main" >> /etc/apt/sources.list
RUN echo "deb-src http://qgis.org/debian jessie main" >> /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key 073D307A618E5811

# Install the dependencies and download the Debian source package with apt-get or aptitude.
RUN apt-get update && \
	apt-get upgrade -y --force-yes && \
	apt-get install -y apache2 bash-completion bison checkinstall cmake devscripts doxygen flex git graphviz grass-dev libexpat1-dev libfcgi-dev libgdal-dev libgeos-dev libgsl0-dev libopenscenegraph-dev libosgearth-dev libpq-dev libproj-dev libqt4-dev libqt4-opengl-dev libqtwebkit-dev libqwt-dev libspatialindex-dev libspatialite-dev libsqlite3-dev pkg-config pkg-kde-tools pyqt4-dev-tools python-all python-all-dev python-qgis python-qt4 python-qt4-dev python-sip python-sip-dev qgis qgis-plugin-grass txt2tags xauth xfonts-100dpi xfonts-75dpi xfonts-base xfonts-scalable xvfb

# Build GDAL from source
WORKDIR /usr/local
RUN git clone https://github.com/OSGeo/gdal.git && \
	cd gdal/gdal && \
	git checkout --track origin/2.2 && \
	./configure --with-python && \
	make && \
	checkinstall
#&& gdalwarp --version

# Set the working directory to /coal
WORKDIR /coal

# Copy the current directory contents into the container at /coal
ADD . /coal

# Install pycoal from source, ensures we always use the latest development branch
RUN python setup.py install





