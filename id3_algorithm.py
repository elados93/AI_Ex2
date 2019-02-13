from math import log

from attribute_node import AttributeNode, ClassNode


def check_for_consolidation(root):
    """
    Check if a consolidation on root may happen in order to avoid unwanted branches.
    :param root: The given root to check consolidation.
    :return: The consolidated root.
    """
    same_class = None

    for child in root.dict.values():
        if not isinstance(child, ClassNode):
            return root
        if same_class is None:
            same_class = child.class_name
        elif child.class_name != same_class:
            return root

    return ClassNode(same_class)


class ID3(object):

    def __init__(self, data, log_base=2):
        """
        Construct ID3 object using a given log base, usually it's 2. Also define the tree as None.
        :param log_base: The logarithm base for the calculation of the probability.
        """
        self.log_base = log_base
        self.data = data
        self.tree = None

    def predict(self, entry):
        """
        Returns the current tree for a given entry.
        :param entry: Entry to predict.
        :return: Decision tree for that entry.
        """
        return self.tree.predict(entry)

    def generate_tree(self, data, attributes, default=None):
        """
        Generate the decision tree for a given data.
        :param data: The data we have as training examples.
        :param attributes: The attributes of the data.
        :param default: The default class in case of tie.
        :return: The decision tree for data.
        """
        # if we got no data left, return the default value
        if data.total_count == 0:
            return ClassNode(default)

        # if all the classes are the same, return a terminal node
        data_classes = data.get_all_classes()
        if len(data_classes) == 1:
            return ClassNode(data_classes.pop())

        # if there is only one attribute left, choose the more common class
        if len(attributes) == 0:
            return ClassNode(data.most_common_class())

        # calc entropy for all attributes
        entropy_dict = {}
        decision_entropy = self.calc_decision_entropy(data)

        for attribute in attributes:
            entropy_dict[attribute] = self.calc_gain(decision_entropy, attribute, data)

        best_attribute = max(entropy_dict.items(), key=lambda x: x[1])[0]
        root = AttributeNode(best_attribute)
        best_attribute_options = self.data.dict_of_attributes[best_attribute]

        for choice in best_attribute_options:
            data_with_attribute = data.get_data_with_attribute_choice(best_attribute, choice)
            new_attributes = [x for x in attributes if x != best_attribute]
            new_default = max(data.class_counter.items(), key=lambda x: x[1])[0]

            child = self.generate_tree(data_with_attribute, new_attributes, default=new_default)
            root.add_child_to_dict(choice, child)

        # in the exercise we didn't need to, but I made consolidate function
        # root = check_for_consolidation(root)
        self.tree = root
        return root

    def calc_gain(self, decision_entropy, attribute, data):
        """
        Calculate the gain of an attribute on the current data.
        :param decision_entropy: The decision entropy of data.
        :param attribute: The attribute to check gain for.
        :param data: The data we are working on.
        :return: The calculated gain.
        """
        total_entropy = decision_entropy
        attribute_options = data.dict_of_attributes[attribute]
        attribute_count_dictionary = data.attributes_counter[attribute]
        classes = data.get_all_classes()

        for value in attribute_options:
            yes_count = 0
            no_count = 0
            for entry in data.get_all_entries():
                if entry.has_attribute(attribute, value):
                    if entry.entry_class == classes[1]:
                        yes_count += 1
                    elif entry.entry_class == classes[0]:
                        no_count += 1

            total_value_count = attribute_count_dictionary[value]
            yes_ratio, no_ratio = yes_count / total_value_count, no_count / total_value_count
            value_ratio = total_value_count / data.total_count

            if yes_ratio == 0 or no_ratio == 0:
                entropy = 0
            else:
                entropy = -yes_ratio * log(yes_ratio, self.log_base) - no_ratio * log(no_ratio, self.log_base)
            total_entropy -= value_ratio * entropy

        return total_entropy

    def calc_decision_entropy(self, data):
        """
        Calculate the decision entropy of data. Assume 2 values.
        :param data: The given data.
        :return: The decision entropy.
        """
        yes_count, no_count = 0, 0
        classes = data.get_all_classes()

        for entry in data.get_all_entries():
            if entry.entry_class == classes[1]:
                yes_count += 1
            elif entry.entry_class == classes[0]:
                no_count += 1

        yes_ratio, no_ratio = yes_count / data.total_count, no_count / data.total_count

        if yes_ratio == 0 or no_ratio == 0:
            entropy = 0
        else:
            entropy = -yes_ratio * log(yes_ratio, self.log_base) - no_ratio * log(no_ratio, self.log_base)
        return entropy

    def write_tree_to_file(self):
        """
        Write a nice representation of the tree in output.txt file.
        :return: None
        """
        with open('output_tree.txt', 'w') as tree_file:
            tree_file.write(self.tree.tree_as_string())

    def __repr__(self):
        """
        Representation for ID3 Algorithm.
        :return:
        """
        return 'DT'
