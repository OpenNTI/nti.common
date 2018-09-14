#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that

from anytree import CountError

import unittest

from nti.common.datastructures import ObjectHierarchyTree


class Root(object):
    __name__ = u'Root'


class Child(Root):
    __name__ = u'Child'


class GrandChild(Child):
    __name__ = u'Grandchild'


class TestDatastructures(unittest.TestCase):

    def test_object_tree(self):
        tree = ObjectHierarchyTree()
        root = Root()
        tree.add(root, None)
        assert_that(tree.height, is_(0))

        # pylint: disable=attribute-defined-outside-init
        child = Child()
        child.__parent__ = root
        tree.add(child, root)
        assert_that(tree.height, is_(1))

        gc1 = GrandChild()
        gc2 = GrandChild()
        gc1.__parent__ = child
        gc2.__parent__ = child
        tree.add(gc1, child)
        tree.add(gc2, child)
        assert_that(tree.height, is_(2))

        # Test duplicate object
        try:
            tree.add(child)
            tree.add(gc1)
        except CountError:  # pragma: no cover
            self.fail(u'Failed to add duplicate object to tree')

        # Test remove bottom node
        assert_that(tree.height, is_(2))
        tree.remove(gc1)
        assert_that(tree.height, is_(2))
        tree.remove(gc2)
        assert_that(tree.height, is_(1))

        # Test remove nested node
        tree.add(gc1)
        tree.add(gc2)
        tree.remove(child)
        assert_that(tree.height, is_(0))

        # Test properties
        tree.add(child)
        tree.add(gc1)
        tree.add(gc2)
        assert_that(tree.children_objects, is_((child,)))
        assert_that(tree.descendant_objects, is_((child, gc1, gc2)))
        assert_that(tree.parent_object, is_(None))
        assert_that(tree.ancestor_objects, is_(()))
        assert_that(tree.sibling_objects, is_(()))

        child_tree = tree.get_node_from_object(child)
        assert_that(child_tree.children_objects, is_((gc1, gc2)))
        assert_that(child_tree.descendant_objects, is_((gc1, gc2)))
        assert_that(child_tree.parent_object, is_(root))
        assert_that(child_tree.ancestor_objects, is_((root,)))
        assert_that(child_tree.sibling_objects, is_(()))

        gc_tree = tree.get_node_from_object(gc1)
        assert_that(gc_tree.children_objects, is_(()))
        assert_that(gc_tree.descendant_objects, is_(()))
        assert_that(gc_tree.parent_object, is_(child))
        assert_that(gc_tree.sibling_objects, is_((gc2,)))
        assert_that(gc_tree.ancestor_objects, is_((root, child)))

        # Test assertions
        with self.assertRaises(KeyError):
            tree.add({'noparent', 'obj'})

        with self.assertRaises(KeyError):
            foster_child = Child()
            foster_child.__parent__ = u'WrongRoot'
            tree.add(foster_child)
