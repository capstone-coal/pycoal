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
   
Quickstart
*****************

=================================
The pycoal Command Line Interface
=================================
When you install pycoal via `pip <https://github.com/capstone-coal/pycoal#pip>`_, `conda <https://github.com/capstone-coal/pycoal#conda>`_, from `source <https://github.com/capstone-coal/pycoal#source>`_ or via `Docker <https://github.com/capstone-coal/pycoal#docker>`_, you will automatically have access to a number of CLI utlity tools made available on your system path. These tools are descrtibed below. All tools can be invoked with the **-h** flag to print help.

pycoal-mineral
^^^^^^^^^^^^^^

::

   $ pycoal-mineral -h

   usage: pycoal-mineral [-h] [-i IMAGE] [-s SLIB] [-r RGB_FILENAME]
                      [-c CLASSIFIED_FILENAME]

   pycoal-mineral -- a CLI for COAL mineral classification

   pycoal-mineral provides a CLI which demonstrates how the COAL Mineral Classification
   API provides methods for generating visible-light and mineral classified images.
   Mineral classification can take hours to days depending on the size of the spectral
   library and the available computing resources, so running a script in the background
   is recommended. More reading an this example can be seen at
   https://capstone-coal.github.io/docs#usage

   @author:     COAL Developers

   @copyright:  2018 COAL Developers. All rights reserved.

   @license:    GNU General Public License version 2

   @contact:    coal-capstone@googlegroups.com

   optional arguments:
      -h, --help            show this help message and exit
      -i IMAGE, --image IMAGE
                        Input file to be processed
      -s SLIB, --slib SLIB  Spectral Library filename
      -r RGB_FILENAME, --rgb_filename RGB_FILENAME
                        RGB File Name
      -c CLASSIFIED_FILENAME, --classified_filename CLASSIFIED_FILENAME
                        Classified File Name

pycoal-mining
^^^^^^^^^^^^^

::

   $ pycoal-mining -h

   usage: pycoal-mining [-h] [-mi INPUT] [-mo OUTPUT]

   pycoal-mining -- a CLI for COAL mining classification

   pycoal-mining provides a CLI which demonstrates how the COAL Mining Classification
   API provides methods for generating mining classified images.
   Mining classification runtime depends largely on the size of the spectral
   library and the available computing resources. More reading an this example can be seen at
   https://capstone-coal.github.io/docs#usage

   @author:     COAL Developers

   @copyright:  2018 COAL Developers. All rights reserved.

   @license:    GNU General Public License version 2

   @contact:    coal-capstone@googlegroups.com

   optional arguments:
      -h, --help            show this help message and exit
      -mi INPUT, --mineral_input INPUT
                        Input classified mineral file to be processed
      -mo OUTPUT, --mining_output OUTPUT
                        Output mining classified image filename

pycoal-environment
^^^^^^^^^^^^^^^^^^

::

   $ pycoal-environment -h

   usage: pycoal-environment [-h] [-m MINING_FILENAME] [-hy VECTOR_FILENAME]
                          [-e CORRELATION_FILENAME]

   pycoal-environment -- a CLI for COAL environment classification

   pycoal-environment provides a CLI which demonstrates how the COAL Environment Classification
   API provides methods for generating environment classified images.
   Environment classification runtime depends largely on the size of the spectral
   library and the available computing resources. More reading an this example can be seen at
   https://capstone-coal.github.io/docs#usage

   @author:     COAL Developers

   @copyright:  2018 COAL Developers. All rights reserved.

   @license:    GNU General Public License version 2

   @contact:    coal-capstone@googlegroups.com

   optional arguments:
      -h, --help            show this help message and exit
      -m MINING_FILENAME, --mining MINING_FILENAME
                        Input mining classified file to be processed
      -hy VECTOR_FILENAME, --hydrography VECTOR_FILENAME
                        Path to hydrography data
      -e CORRELATION_FILENAME, --environment CORRELATION_FILENAME
                        Output environmental correlation image

===============
pycoal Examples
===============
In the `examples directory <https://github.com/capstone-coal/pycoal/tree/master/examples>`_ you can find several python scripts with specific applications of COAL. The `README <https://github.com/capstone-coal/pycoal/blob/master/examples/README.rst>`_ provides all of the information you need to get going. If you find an issue with the examples, please `report it at our issue tracker <https://github.com/capstone-coal/pycoal/issues>`_.


