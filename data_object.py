class DataObject(object):

    def __init__(self):
        """
        Construct a data object for prediction. or training
        """
        self.entries = []
        self.dict_of_attributes = {}

        self.attributes_counter = {}
        self.class_counter = {}  # {'class1: counter1, class 2: counter2...}
        self.total_count = 0

    def add_entry(self, entry):
        """
        Adding the entry to the data.
        :param entry: The entry to add.
        :return: None.
        """
        self.entries.append(entry)
        self._add_attributes_of_entry(entry)
        self._count_attributes(entry)

        if entry.entry_class in self.class_counter:
            self.class_counter[entry.entry_class] += 1
        else:
            self.class_counter[entry.entry_class] = 1

        self.total_count += 1

    def get_all_entries(self):
        """
        Return the entries.
        :return: The entries.
        """
        return self.entries

    def get_all_attributes(self):
        """
        Return all the attributes.
        :return: All the attributes.
        """
        return self.entries[0].attributes_names

    def _add_attributes_of_entry(self, entry):
        """
        Adding entry's attributes to the dictionary.
        :param entry: given entry.
        :return: None
        """
        for attribute, value in zip(entry.attributes_names, entry.attributes):
            if attribute in self.dict_of_attributes:
                if value not in self.dict_of_attributes[attribute]:
                    self.dict_of_attributes[attribute].append(value)
            else:
                self.dict_of_attributes[attribute] = [value]

    def most_common_class(self):
        """
        Return the most common class.
        :return: The most common class.
        """
        # part of the exercise requirements, to choose yes and 1 over no and 0 in case of equality
        if len(self.class_counter.keys()) == 2:
            values = list(self.class_counter.values())
            if values[0] == values[1]:
                return sorted(self.class_counter.keys())[1]
        return max(self.class_counter.items(), key=lambda x: x[1])[0]

    def get_data_with_attribute_choice(self, attribute, value):
        """
        Return the data only with attribute as value.
        :param attribute: given attribute.
        :param value: given value.
        :return: New data with only these properties.
        """
        new_data = DataObject()
        for entry in self.entries:
            if entry.has_attribute(attribute, value):
                new_data.add_entry(entry)
        return new_data

    def get_all_classes(self):
        """
        Return all the classes in data.
        :return: All the classes in data.
        """
        return [name for name, occ in self.class_counter.items() if occ != 0]

    def _count_attributes(self, entry):
        """
        Count all the attributes in entry. Making a counter dictionary like:
         {pclass: {1st: 34, ..}, sex:{male: 3...}}.
        :param entry: given entry.
        :return: None.
        """
        for attribute_index, value in enumerate(entry.attributes):
            attribute_name = entry.attributes_names[attribute_index]

            if attribute_name in self.attributes_counter:
                if value in self.attributes_counter[attribute_name]:
                    self.attributes_counter[attribute_name][value] += 1
                else:
                    self.attributes_counter[attribute_name][value] = 1
            else:
                self.attributes_counter[attribute_name] = {value: 1}


class Entry(object):

    def __init__(self, attributes_names, *attributes):
        """
        Construct an entry to predict or train.
        :param attributes_names: All the attributes name.
        :param attributes: All the values of attributes.
        """
        self.attributes_names = attributes_names
        self.attributes = [attr for attr in attributes[:-1]]
        self.entry_class = attributes[-1]

    def has_attribute(self, attribute, value):
        """
        True or False if the attribute has the value 'value'
        :param attribute: attribute
        :param value: value
        :return: True or False if the attribute has the value 'value'
        """
        index_of_attribute = self.attributes_names.index(attribute)
        return self.attributes[index_of_attribute] == value

    def get_attribute_value(self, attribute):
        """
        Return the value of attribute in entry.
        :param attribute: given attribute.
        :return: The value at attribute.
        """
        index_of_attribute = self.attributes_names.index(attribute)
        return self.attributes[index_of_attribute]

    def __sub__(self, other):
        """
        Do hamming distance for 2 entries.
        :param other: another entry.
        :return: The hamming dist.
        """
        total_dist = 0
        for self_attr, other_attr in zip(self.attributes, other.attributes):
            if self_attr != other_attr:
                total_dist += 1
        return total_dist

    def __eq__(self, other):
        """
        True or False if entry is equal to other.
        :param other: another entry.
        :return: True or False if entry is equal to other.
        """
        return self.attributes == other.attributes

    def __repr__(self):
        """
        Nice representation for entry.
        :return: String of entry.
        """
        return '%s %s' % (str(self.attributes), self.entry_class)
