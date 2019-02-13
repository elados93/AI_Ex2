class AttributeNode(object):

    def __init__(self, attribute_name):
        """
        Construct a node with attribute name.
        :param attribute_name: a given name for node.
        """
        self.attribute = attribute_name
        self.dict = {}

    def add_child_to_dict(self, value, child):
        """
        Adding the child with attribute to node.
        :param value: value of attribute.
        :param child: child.
        :return: None.
        """
        self.dict[value] = child

    def predict(self, entry):
        """
        Predict what will be the output for entry.
        :param entry: entry.
        :return: The prediction.
        """
        value = entry.get_attribute_value(self.attribute)
        return self.dict[value].predict(entry)

    def tree_as_string(self, space_number=0):
        """
        Construct a nice string as a representation of the tree.
        :param space_number: The number of spaces to concat in the string.
        :return: The representing tree.
        """
        my_string = ''
        branches = sorted(list(self.dict.keys()))

        for branch in branches:
            next_node = self.dict[branch]
            for _ in range(space_number):
                my_string += '\t'

            if space_number != 0:  # add | only to children
                my_string += '|'

            # divide the case for a terminal node and a continues node
            if isinstance(next_node, ClassNode):
                my_string += '%s=%s:%s\n' % (self.attribute, branch, next_node.class_name)
            else:
                my_string += '%s=%s\n' % (self.attribute, branch)
                my_string += '%s' % next_node.tree_as_string(space_number + 1)

        return my_string


class ClassNode(object):

    def __init__(self, class_name):
        """
        Construct a class node with a class name.
        :param class_name: The class name.
        """
        self.class_name = class_name

    def predict(self, entry=None):
        """
        Predict the class for entry.
        :param entry: The entry.
        :return: The prediction, actually the class.
        """
        return self.class_name

    def __repr__(self):
        """
        Nice representation
        :return:
        """
        return self.class_name
