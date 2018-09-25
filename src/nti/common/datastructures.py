#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from anytree import find_by_attr
from anytree import NodeMixin

logger = __import__('logging').getLogger(__name__)


class ObjectHierarchyTree(NodeMixin):
    """
    Lookup_func should be a function that takes an object and returns a unique key
    """

    def __init__(self, name=None, parent=None, obj=None, lookup_func=id):
        self.name = name
        self.parent = parent
        self.obj = obj
        self.lookup_func = lookup_func

    def set_root(self, obj):
        self.name = self.lookup_func(obj)
        self.obj = obj

    def add(self, obj, parent=None):
        # If we haven't defined a root yet set this obj as root
        if self.obj is None:
            return self.set_root(obj)

        if parent is None:
            parent = getattr(obj, '__parent__', None)
            if parent is None:
                raise KeyError(
                    u'Parent parameter must be passed or defined on object.'
                )

        parent_name = self.lookup_func(parent)
        parent_node = find_by_attr(self, parent_name)
        if parent_node is None:
            raise KeyError(
                u'The provided object\'s parent cannot be found in the tree'
            )
        node_name = self.lookup_func(obj)
        node = find_by_attr(self, node_name)
        # If a node for this object already exists don't duplicate it
        if node is None:
            ObjectHierarchyTree(node_name, parent_node, obj, self.lookup_func)

    def remove(self, obj):
        node = find_by_attr(self, self.lookup_func(obj))
        parent_node = node.parent
        # Remove this branch
        parent_children = [x for x in parent_node.children if x != node]
        # Update the parent's children
        parent_node.children = parent_children

    def _get_object_from_node(self, node):
        return getattr(node, 'obj', None)

    def _get_objects_from_nodes(self, nodes):
        objects = []
        for node in nodes or ():
            objects.append(self._get_object_from_node(node))
        return tuple(objects)

    def get_node_from_object(self, obj):
        node = find_by_attr(self, self.lookup_func(obj))
        return node

    @property
    def children_objects(self):
        return self._get_objects_from_nodes(self.children)

    @property
    def descendant_objects(self):
        return self._get_objects_from_nodes(self.descendants)

    @property
    def ancestor_objects(self):
        return self._get_objects_from_nodes(self.ancestors)

    @property
    def sibling_objects(self):
        return self._get_objects_from_nodes(self.siblings)

    @property
    def parent_object(self):
        return self._get_object_from_node(self.parent)
