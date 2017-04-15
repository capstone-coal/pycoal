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

from pycoal import mineral
import spectral
import numpy

def test_classifyImage():
    """
    This function tests the method "classifyImage" from the "mineral" class.
    Args:
        None
    Returns:
        None
    """
    lib_file = "/home/claytonh/Downloads/USGS/s06av95a_envi.hdr"

    tst_class = mineral.MineralClassification(lib_file)

    # make sure library is being opened as such
    assert isinstance(tst_class.library, spectral.io.envi.SpectralLibrary)

    raw_filename = "/home/claytonh/Downloads/raw/ang20140912t192359_corr_v1c_img.hdr"
    class_filename = "/home/claytonh/Downloads/classified/ang20140912t192359_corr_v1c_img_class.hdr"

    #classify image
    #tst_class.classifyImage(raw_filename, class_filename)

    raw_image = spectral.open_image(raw_filename)
    class_image = spectral.open_image(class_filename)
    library_image = spectral.open_image(lib_file)

    # make sure shape is consistent between raw and classified
    assert raw_image.nrows == class_image.nrows
    assert raw_image.ncols == class_image.ncols

    # make sure number of classes in classified image is consistent with library
    assert int(class_image.metadata.get(u'classes')) == len(library_image.names) + 1

    


test_classifyImage()