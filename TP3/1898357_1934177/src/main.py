import csv
import json
from itertools import islice
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer


def read_csv(filen):
    with open(filen, mode='r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        data = []

        # skip the first lines
        for x in range(7):
            next(csv_reader)

        for row in csv_reader:
            print(string_to_bool(row[0]), string_to_bool(row[1]), int(row[2]), int(row[3]))
            row_array = (string_to_bool(row[0]), string_to_bool(row[1]), int(row[2]), int(row[3]))
            data.append(row_array)
        return data


def string_to_bool(value):
    return value == "sum_of_logs"


def write_csv(test_data):
    with open("test_result.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerows(test_data)


def evaluate(log_prob, prob_combine, clean_option):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("test_set.json") as email_file:
        new_emails = json.load(email_file)

    i = 0
    email_count = len(new_emails["dataset"])

    print("Evaluating emails ")
    for e_mail in new_emails["dataset"]:
        i += 1
        print("\rEmail " + str(i) + "/" + str(email_count), end="")

        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        if (analyzer.is_spam(subject, body, log_prob, prob_combine, clean_option)) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body, log_prob, prob_combine, clean_option))) and (spam == "false"):
            tn += 1
        if (analyzer.is_spam(subject, body, log_prob, prob_combine, clean_option)) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body, log_prob, prob_combine, clean_option))) and (spam == "true"):
            fn += 1
        total += 1

    accuracy = round((tp + tn) / (tp + tn + fp + fn), 2)
    precision = round(tp / (tp + fp), 2)
    recall = round(tp / (tp + fn), 2)

    print("")
    print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
    print("Precision: ", round(tp / (tp + fp), 2))
    print("Recall: ", round(tp / (tp + fn), 2))

    return [accuracy, precision, recall]


if __name__ == "__main__":
    file_name = 'ACTS_output_4.csv'
    data_array = read_csv(file_name)
    results = []
    for data in data_array:
        # 1. Creation de vocabulaire.
        vocab = VocabularyCreator()
        vocab.create_vocab(data[2], data[3])

        # 2. Classification des emails et initialisation des utilisateurs et des groupes.
        renege = RENEGE()
        renege.classify_emails(data[0], data[1], data[3])

        # 3. Evaluation de performance du modele avec la fonction evaluate()
        result = evaluate(data[0], data[1], data[3])
        results.append(result)
    header = ['Accuracy', 'Precision', 'Recall']
    results.insert(0, header)
    write_csv(results)
