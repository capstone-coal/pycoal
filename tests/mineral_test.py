#!/usr/bin/env python

from pycoal import mineral

def test_normalize():
    pass

def test_indexOfGreaterThan():
    # test object
    test_classifier = mineral.MineralClassification()

    # [0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    test_list = [x * 1.0 for x in range(10)]

    assert test_classifier._MineralClassification__indexOfGreaterThan(test_list, 5) == 6

    assert test_classifier._MineralClassification__indexOfGreaterThan(test_list, 1) == 2

    assert test_classifier._MineralClassification__indexOfGreaterThan(test_list, 11) == 9

def test_trainClassifier():
    pass

def test_saveClassifier():
    pass

def test_readClassifier():
    pass

def test_classifyPixel():
    pass

def test_classifyImage():
    pass

def test_classifyImages():
    pass
