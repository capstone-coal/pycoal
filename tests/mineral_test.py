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

def test_normalize():
    """
    This tests the public method normalize in the class MineralClassification.
    Args:
        None
    Returns:
        None
    """
    obj = mineral.MineralClassification()
    library = spectral.open_image("s06av95a_envi.hdr")

    spectra = library.spectra[..., numpy.newaxis, ...]
    normalized = obj.normalize(spectra, library.metadata.get('wavelength'))


def test_indexOfGreaterThan():
    """
    This tests the private method __indexOfGreaterThan in the class MineralClassification.
    Args:
        None
    Returns:
        None
    """
    test_list = [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]

    # [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    #                         ---  ---
    # 6.0 is the first value greater than 5.0, so the return should be its index (6)
    assert mineral.MineralClassification._MineralClassification__indexOfGreaterThan(test_list, 5.0) == 6

    # [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    #     ---  ---
    # 2.0 is the first value greater than 1.0, so the return should be its index (2)
    assert mineral.MineralClassification._MineralClassification__indexOfGreaterThan(test_list, 1.0) == 2

    # [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    # 11.0 is not in the range of this list, so the return will just be the last index
    assert mineral.MineralClassification._MineralClassification__indexOfGreaterThan(test_list, 11.0) == 9

def test_classifyPixel():
    pass

def test_classifyImage():
    pass

def test_classifyImages():
    pass

