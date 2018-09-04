#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from anytree import find_by_attr
from anytree import NodeMixin

logger = __import__('logging').getLogger(__name__)


class ObjectHierarchyTree(NodeMixin):

    def __init__(self, name=None, parent=None, obj=None):
        self.name = name
        self.parent = parent
        self.obj = obj

    def set_root(self, obj):
        self.name = id(obj)
        self.obj = obj

    def add(self, obj, parent=None):
        # If we haven't defined a root yet set this obj as root
        if self.obj is None:
            return self.set_root(obj)

        if parent is None:
            parent = getattr(obj, '__parent__', None)
            if not parent:
                raise KeyError(u'Parent parameter must be passed or defined on object.')

        parent_name = id(parent)
        parent_node = find_by_attr(self, parent_name)
        if not parent_node:
            raise KeyError(u'The provided object\'s parent cannot be found in the tree')
        ObjectHierarchyTree(name=id(obj), parent=parent_node, obj=obj)

    def remove(self, obj):
        node = find_by_attr(self, id(obj))
        parent_node = node.parent
        # Remove this branch
        parent_children = list(parent_node.children)
        parent_children.remove(node)
        # Update the parent's children
        parent_node.children = parent_children

    def _get_object_from_node(self, node):
        return getattr(node, 'obj', None)

    def _get_objects_from_nodes(self, nodes):
        objects = []
        for node in nodes:
            objects.append(self._get_object_from_node(node))
        return tuple(objects)

    def get_node_from_object(self, obj):
        node = find_by_attr(self, id(obj))
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
