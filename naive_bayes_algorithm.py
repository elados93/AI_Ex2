class NaiveBayes(object):
    def __init__(self, data):
        """
        Build naive bayes algorithm with a given data.
        :param data: The naive bayes algorithm.
        """
        self.data = data
        self.classes = data.get_all_classes()
        self.yes_class_ratio = (data.class_counter[self.classes[1]] / data.total_count)
        self.no_class_ratio = (data.class_counter[self.classes[0]] / data.total_count)

    def predict(self, entry):
        """
        Predict entry on naive bayes algorithm.
        :param entry: The entry to do prediction on.
        :return: The prediction.
        """
        yes_probability = self.yes_class_ratio
        no_probability = self.no_class_ratio

        for attribute, value in zip(entry.attributes_names, entry.attributes):
            yes_probability *= self.calc_probability(attribute, value, self.classes[1])
            no_probability *= self.calc_probability(attribute, value, self.classes[0])

        if yes_probability > no_probability:
            return self.classes[1]
        else:
            return self.classes[0]

    def calc_probability(self, attribute, value, class_type):
        """
        Calculate the probability using bayes equation.
        :param attribute: The attribute to calculate.
        :param value: The value.
        :param class_type: The class type.
        :return: The probability.
        """
        attribute_count = 1  # starts at 1 in order to avoid 0 mul

        for entry in self.data.get_all_entries():
            if entry.entry_class == class_type:
                if entry.has_attribute(attribute, value):
                    attribute_count += 1

        smoothing_denominator = len(self.data.dict_of_attributes[attribute])

        if class_type == self.classes[1]:
            return attribute_count / (self.data.class_counter[self.classes[1]] + smoothing_denominator)
        elif class_type == self.classes[0]:
            return attribute_count / (self.data.class_counter[self.classes[0]] + smoothing_denominator)

    def __repr__(self):
        """
        Nice representation for the algorithm
        :return:
        """
        return 'naiveBase'
