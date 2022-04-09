import json

from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer

def evaluate(model):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("./dataset/" + model + ".json") as email_file:
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

        if ((analyzer.is_spam(subject, body))) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body))) and (spam == "false"):
            tn += 1
        if ((analyzer.is_spam(subject, body))) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body))) and (spam == "true"):
            fn += 1
        total += 1

    print("")
    # print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))

    print("Precision: ", round(tp / (tp + fp), 2))
    precision = round(tp / (tp + fp), 2)

    print("Recall: ", round(tp / (tp + fn), 2))
    recall = round(tp / (tp + fn), 2)

    return f1(precision, recall)


def f1(precision, recall):
    return 2 * (precision * recall) / (precision + recall)


def evaluatePerformance(filename, model):
    # 1. Creation de vocabulaire.
    vocab = VocabularyCreator(filename)
    vocab.create_vocab()

    # 2. Classification des emails et initialisation des utilisateurs et des groupes.
    renege = RENEGE(filename)
    renege.classify_emails()

    # 3. Evaluation de performance du modele avec la fonction evaluate()
    evaluate(model)


if __name__ == "__main__":

    options = ["train", "test"]
    metamorphic_transformations = ["clean", "shuffle", "triple", "words"]

    for option in options:
        for mt in metamorphic_transformations:
            if mt == "triple" and option == "train":
                mt = "700x3"
            if mt == "triple" and option == "test":
                mt = "300x3"

            # build the filename
            filename = option + '_' + mt
            # build the fileset
            fileset = option + "_set"

            vocab = VocabularyCreator(fileset)
            vocab.create_vocab()
            renege = RENEGE(fileset)
            renege.classify_emails()

            if option == "train":
                evaluatePerformance(filename, "test_set")
            else:
                evaluatePerformance("train_set", filename)

