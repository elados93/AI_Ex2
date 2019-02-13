class Knn(object):

    def __init__(self, data, k):
        """
        Construct KNN algorithm.
        :param data: given data to train on.
        :param k: an integer. MUST BE ODD!
        """
        if k % 2 == 0:
            raise ValueError("k must be odd!")

        self.data = data
        self.k = k
        self.k_nearest = []

    def predict(self, entry):
        """
        Predict what entry class will be.
        :param entry: the entry to predict.
        :return: The predication.
        """
        self.k_nearest = [(float('inf'), None) for _ in range(self.k)]

        for data_entry in self.data.get_all_entries():
            current_dist = entry - data_entry
            self._add_to_k_nearest(current_dist, data_entry.entry_class)

        only_classes = [x[1] for x in self.k_nearest]
        return max(only_classes, key=only_classes.count)

    def _add_to_k_nearest(self, current_dist, entry_class):
        """
        Adding the distance and entry class to k nearest.
        :param current_dist: The distance.
        :param entry_class: The entry class.
        :return: None.
        """
        for i, k_entry in enumerate(self.k_nearest):
            if current_dist < k_entry[0]:
                self.k_nearest[i] = (current_dist, entry_class)
                # when we find the right spot, we can just exit
                return

    def __repr__(self):
        """
        Nice representation of KNN algorithm.
        :return: String of representation.
        """
        return 'KNN'
