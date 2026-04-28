import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode()
        self.assertIs(node.props_to_html(), "")
        node2 = HTMLNode(props={"href": "idk", "true": "yep"})
        self.assertEqual(node2.props_to_html(), ' href="idk" true="yep"')

    def test_print(self):
        node = HTMLNode(1, 2, 3, True)
        self.assertEqual(node.__repr__(), "HTMLNode(1, 2, 3, True)")
