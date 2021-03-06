#!/usr/bin/python3

# Copyright 2018 The VGC Developers
# See the COPYRIGHT file at the top-level directory of this distribution
# and at https://github.com/vgc/vgc/blob/master/COPYRIGHT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from vgc.dom import Document, Element, Node, NodeType

def getChildNames(node):
    return [child.name for child in node.children]

class TestNodeType(unittest.TestCase):

    def testValues(self):
        NodeType.Document
        NodeType.Element

class TestNode(unittest.TestCase):

    def testConstructor(self):
        with self.assertRaises(TypeError):
            node = Node()

    def testNodeType(self):
        node = Element("foo")
        self.assertEqual(node.nodeType, NodeType.Element)

    def testParentChildRelationships(self):
        n1 = Element("foo")
        self.assertIsNone(n1.parent)
        self.assertIsNone(n1.firstChild)
        self.assertIsNone(n1.lastChild)
        self.assertIsNone(n1.previousSibling)
        self.assertIsNone(n1.nextSibling)

        n2 = Element("bar")
        n3 = Element("bar")
        n4 = Element("bar")
        n1.appendChild(n2)
        n1.appendChild(n3)
        n1.appendChild(n4)

        self.assertEqual(n1.parent,          None)
        self.assertEqual(n1.firstChild,      n2)
        self.assertEqual(n1.lastChild,       n4)
        self.assertEqual(n1.previousSibling, None)
        self.assertEqual(n1.nextSibling,     None)

        self.assertEqual(n2.parent,          n1)
        self.assertEqual(n2.firstChild,      None)
        self.assertEqual(n2.lastChild,       None)
        self.assertEqual(n2.previousSibling, None)
        self.assertEqual(n2.nextSibling,     n3)

        self.assertEqual(n3.parent,          n1)
        self.assertEqual(n3.firstChild,      None)
        self.assertEqual(n3.lastChild,       None)
        self.assertEqual(n3.previousSibling, n2)
        self.assertEqual(n3.nextSibling,     n4)

        self.assertEqual(n4.parent,          n1)
        self.assertEqual(n4.firstChild,      None)
        self.assertEqual(n4.lastChild,       None)
        self.assertEqual(n4.previousSibling, n3)
        self.assertEqual(n4.nextSibling,     None)

    def testChildren(self):
        n1 = Element("foo")
        n2 = Element("bar1")
        n3 = Element("bar2")
        n4 = Element("bar3")
        n1.appendChild(n2)
        n1.appendChild(n3)
        n1.appendChild(n4)
        self.assertEqual(getChildNames(n1), ["bar1", "bar2", "bar3"])

    def testDocument(self):
        doc = Document()
        self.assertEqual(doc.document, doc)

        n1 = Element("foo")
        self.assertIsNone(n1.document)

        n2 = Element("bar")
        n1.appendChild(n2)
        self.assertIsNone(n1.document)
        self.assertIsNone(n2.document)

        doc.appendChild(n1)
        self.assertEqual(n1.document, doc)
        self.assertEqual(n2.document, doc)

    def testAppendChild(self):
        node1 = Element("foo")
        node2 = Element("bar")
        self.assertTrue(node1.canAppendChild(node2))
        self.assertEqual(node1.appendChild(node2), node2)

    def testAppendChildDocument(self):
        element = Element("foo")
        document = Document()
        self.assertFalse(element.canAppendChild(document))
        self.assertIsNone(element.appendChild(document))

    def testAppendChildRootElement(self):
        document = Document()
        element1 = Element("foo")
        element2 = Element("bar")
        document.appendChild(element1)
        self.assertEqual(document.rootElement, element1)
        self.assertFalse(document.canAppendChild(element2))
        self.assertIsNone(document.appendChild(element2))

    def testRemoveChild(self):
        n = Element("foo")
        n1 = Element("n1")
        n2 = Element("n2")
        n3 = Element("n3")
        n4 = Element("n4")

        n.appendChild(n1)
        n.appendChild(n2)
        n.appendChild(n3)
        n.appendChild(n4)
        self.assertEqual(getChildNames(n), ["n1", "n2", "n3", "n4"])

        n.removeChild(n3)
        self.assertEqual(getChildNames(n), ["n1", "n2", "n4"])

        n.removeChild(n4)
        self.assertEqual(getChildNames(n), ["n1", "n2"])

        self.assertIsNone(n.removeChild(n4))
        self.assertEqual(getChildNames(n), ["n1", "n2"])

        n5 = Element("n5")
        self.assertIsNone(n.removeChild(n5))
        self.assertEqual(getChildNames(n), ["n1", "n2"])

        n.removeChild(n1)
        self.assertEqual(getChildNames(n), ["n2"])

        n.removeChild(n2)
        self.assertEqual(getChildNames(n), [])

if __name__ == '__main__':
    unittest.main()
