from unittest import TestCase
import unittest
from uforgecli.utils import compare_utils

class Distrib(object):
    def __init__(self, name):
        self.name = name

centos = Distrib("CentOS")
debian = Distrib("Debian")
fedora = Distrib("Fedora")

class TestCompare(TestCase):

    def test_compare_should_retain_only_elements_matching_with_given_value(self):
        candidates = [centos , debian, fedora]
        filtered_elements = compare_utils.compare(candidates, "CentOS", "name")
        self.assertListEqual(filtered_elements, [centos])

    def test_compare_should_support_several_values_as_second_parameter(self):
        candidates = [centos , debian, fedora]
        filtered_elements = compare_utils.compare(candidates, ["CentOS", "Fedora"], "name")
        self.assertListEqual(filtered_elements, [centos, fedora])

    def test_compare_should_support_wide_card(self):
        candidates = [centos , debian, fedora]
        filtered_elements = compare_utils.compare(candidates, "Deb*", "name")
        self.assertListEqual(filtered_elements, [debian])

if __name__ == '__main__':
    unittest.main()