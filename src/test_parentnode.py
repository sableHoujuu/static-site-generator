import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_many_children(self):
        children = []
        for i in range(0, 10):
            child_node = LeafNode("span", "this is a child")
            children.append(child_node)
        parent_node = ParentNode("div", children)
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>this is a child</span><span>this is a child</span><span>this is a child</span><span>this is a child</span><span>this is a child</span><span>this is a child</span><span>this is a child</span><span>this is a child</span><span>this is a child</span><span>this is a child</span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode(None, None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_complex_heritage(self):
        child_node_1 = LeafNode("b", "this is a child")
        child_node_2 = LeafNode("b", "this is a child")
        child_node_3 = LeafNode("b", "this is a child")
        child_node_4 = LeafNode("b", "this is a child")
        parent_node_1 = ParentNode("div", [child_node_1])
        parent_node_2 = ParentNode("div", [child_node_2])
        parent_node_3 = ParentNode("div", [child_node_3])
        parent_node_4 = ParentNode("div", [child_node_4])
        grandparent_node = ParentNode(
            "span", [parent_node_1, parent_node_2, parent_node_3, parent_node_4]
        )
        expected_string = "<span><div><b>this is a child</b></div><div><b>this is a child</b></div><div><b>this is a child</b></div><div><b>this is a child</b></div></span>"
        self.assertEqual(grandparent_node.to_html(), expected_string)

    def test_to_html_with_complex_heritage_and_no_child(self):
        child_node_2 = LeafNode("b", "this is a child")
        child_node_3 = LeafNode("b", "this is a child")
        child_node_4 = LeafNode("b", "this is a child")
        parent_node_1 = ParentNode("div", None)
        parent_node_2 = ParentNode("div", [child_node_2])
        parent_node_3 = ParentNode("div", [child_node_3])
        parent_node_4 = ParentNode("div", [child_node_4])
        grandparent_node = ParentNode(
            "span", [parent_node_1, parent_node_2, parent_node_3, parent_node_4]
        )
        self.assertRaises(ValueError, grandparent_node.to_html)

    def test_to_html_with_missing_value_child(self):
        child_node = LeafNode("a", None)
        parent_node = ParentNode("div", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)
