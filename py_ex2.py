from data_object import DataObject, Entry
from id3_algorithm import ID3
from knn_algo import Knn
from naive_bayes_algorithm import NaiveBayes


def load_train_data():
    """
    Loads the data from the train.txt file
    :return: the data object of the training files.
    """
    data = DataObject()

    with open('train.txt', 'r') as train_file:
        headers = train_file.readline().strip().split('\t')

        for line in train_file:
            entry = Entry(headers[:-1], *line.strip().split('\t'))
            data.add_entry(entry)

        return data


def write_output_file(all_predictions, success_ratios, algorithms):
    """
    Write the output
    :param all_predictions:
    :param success_ratios:
    :param algorithms:
    :return:
    """
    with open('output.txt', 'w') as output_file:
        header = 'Num'
        for algorithm in algorithms:
            header += '\t%s' % str(algorithm)
        output_file.write(header + '\n')

        data_to_output = []
        for prediction_number, prediction in enumerate(all_predictions):
            line = '%d' % (prediction_number + 1)
            for algorithm_prediction in prediction:
                line += '\t%s' % algorithm_prediction
            data_to_output.append(line + '\n')

        line = ''
        for success_ratio in success_ratios:
            line += '\t%.2f' % success_ratio
        data_to_output.append(line)
        output_file.writelines(data_to_output)


def write_predictions_to_file(*algorithms):
    """
    Write the predictions of test.txt in output.txt
    :param algorithms: List of prediction algorithms to use.
    :return: None.
    """
    algorithms_success = [0 for _ in range(len(algorithms))]
    all_predictions = []

    with open('test.txt', 'r') as test_file:
        total_tests = 0
        headers = test_file.readline().strip().split('\t')

        for line in test_file:
            entry = Entry(headers, *line.strip().split('\t'))
            total_tests += 1
            test_predictions = []

            for i, predictions_algorithm in enumerate(algorithms):
                prediction = predictions_algorithm.predict(entry)
                if prediction == entry.entry_class:
                    algorithms_success[i] += 1
                test_predictions.append(prediction)
            all_predictions.append(test_predictions)

    success_ratios = [x / total_tests for x in algorithms_success]
    write_output_file(all_predictions, success_ratios, algorithms)


if __name__ == '__main__':
    """
    Load train data, run predictions on test.txt with KNN, ID3 and Naive Bayes. Then save them in output.txt
    """
    import time

    start = time.time()
    data_object = load_train_data()

    # create 3 prediction algorithms
    id3 = ID3(data_object)
    default = max(data_object.class_counter.items(), key=lambda x: x[1])[0]
    id3.generate_tree(data_object, attributes=data_object.get_all_attributes(), default=default)
    id3.write_tree_to_file()
    knn = Knn(data=data_object, k=5)
    naive_bayes = NaiveBayes(data_object)

    write_predictions_to_file(id3, knn, naive_bayes)
    end = time.time()
    print(end - start)
