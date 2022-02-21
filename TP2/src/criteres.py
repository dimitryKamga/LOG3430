def is_message_a_spam(p, h, u, g) -> bool:
    """
        Function to test if a message is a spam using the default criteria
        p bool: true if message is classified as spom
        h bool: true is an integer indicating the duration of the history is between the 20th message date
        u bool: true if the integer indicating the user's confidence level is < 50
        g bool: true if an integer indicating the confidence level of the group is >=50
        return s: true if message is classified as spam, false if not

    """
    return p and ((h and u) or (u and not g))


def is_message_spam_dnf(p, h, u, g) -> bool:
    """
        Function to test if a message is a spam using the dnf criteria
        p bool: true if message is classified as spom
        h bool: true is an integer indicating the duration of the history is between the 20th message date
        u bool: true if the integer indicating the user's confidence level is < 50
        g bool: true if an integer indicating the confidence level of the group is >=50
        return s: true if message is classified as spam, false if not
    """
    return p and h and u or implicant2(p, u, g)


def implicant2(p, u, g) -> bool:
    return int(p and u and not g)

def applyformat():
    print('rien')

def racc():
    test_set = []
    test_cases_found = False
    # P est la clause majeure
    for h in range(2):
        for u in range(2):
            for g in range(2):
                pred_true = is_message_a_spam(True, h, u, g)
                pred_false = is_message_a_spam(False, h, u, g)
                if not test_cases_found and pred_true != pred_false:
                    test_cases_found = True
                    d1 = f"<[P = 1, H = {h}, U = {u}, G = {g}],S = {pred_true}>"
                    d2 = f"<[P = 0, H = {h}, U = {u}, G = {g}],S = {pred_false}>"
                    if d1 not in test_set:
                        test_set.append(d1)
                    if d2 not in test_set:
                        test_set.append(d2)
    test_cases_found = False

    # H est la clause majeure
    for p in range(2):
        for u in range(2):
            for g in range(2):
                pred_true = bool(is_message_a_spam(p, True, u, g))
                pred_false = bool(is_message_a_spam(p, False, u, g))
                if not test_cases_found and pred_true != pred_false:
                    test_cases_found = True
                    d1 = f"<[P = {p}, H = 1, U = {u}, G = {g}],S = {pred_true}>"
                    d2 = f"<[P = {p}, H = 0, U = {u}, G = {g}],S = {pred_false}>"
                    if d1 not in test_set:
                        test_set.append(d1)
                    if d2 not in test_set:
                        test_set.append(d2)
    test_cases_found = False

    # U est la clause majeure
    for p in range(2):
        for h in range(2):
            for g in range(2):
                pred_true = is_message_a_spam(p, h, True, g)
                pred_false = is_message_a_spam(p, h, False, g)
                if not test_cases_found and pred_true != pred_false:
                    test_cases_found = True
                    d1 = f"<[P = {p}, H = {h}, U = 1, G = {g}],S = {pred_true}>"
                    d2 = f"<[P = {p}, H = {h}, U = 0, G = {g}],S = {pred_false}>"
                    if d1 not in test_set:
                        test_set.append(d1)
                    if d2 not in test_set:
                        test_set.append(d2)
    test_cases_found = False

    # G est la clause majeure
    for p in range(2):
        for h in range(2):
            for u in range(2):
                pred_true = is_message_a_spam(p, h, u, True)
                pred_false = is_message_a_spam(p, h, u, False)
                if not test_cases_found and pred_true != pred_false:
                    test_cases_found = True
                    d1 = f"<[P = {p}, H = {h}, U = {u}, G = 1],S = {pred_true}>"
                    d2 = f"<[P = {p}, H = {h}, U = {u}, G = 0],S = {pred_false}>"
                    if d1 not in test_set:
                        test_set.append(d1)
                    if d2 not in test_set:
                        test_set.append(d2)

    return test_set


def ricc():
    test_set = []
    true_pred_found = False
    false_pred_found = False

    # P est la clause majeure
    for h in range(2):
        for u in range(2):
            for g in range(2):
                pred_true = is_message_a_spam(True, h, u, g)
                pred_false = is_message_a_spam(False, h, u, g)
                if pred_true == pred_false:
                    if pred_true and not true_pred_found:
                        true_pred_found = True
                        d1 = f"<[P = 1, H = {h}, U = {u}, G = {g}],S = {pred_true}>"
                        d2 = f"<[P = 0, H = {h}, U = {u}, G = {g}],S = {pred_false}>"
                        if d1 not in test_set:
                            test_set.append(d1)
                        if d2 not in test_set:
                            test_set.append(d2)
                    if not pred_true and not false_pred_found:
                        false_pred_found = True
                        d1 = f"<[P = 1, H = {h}, U = {u}, G = {g}],S = {pred_true}>"
                        d2 = f"<[P = 0, H = {h}, U = {u}, G = {g}],S = {pred_false}>"
                        if d1 not in test_set:
                            test_set.append(d1)
                        if d2 not in test_set:
                            test_set.append(d2)
    true_pred_found = False
    false_pred_found = False

    # H est la clause majeure
    for p in range(2):
        for u in range(2):
            for g in range(2):
                pred_true = is_message_a_spam(p, True, u, g)
                pred_false = is_message_a_spam(p, False, u, g)
                if pred_true == pred_false:
                    if pred_true and not true_pred_found:
                        true_pred_found = True
                        d1 = f"<[P = {p}, H = 1, U = {u}, G = {g}],S = {pred_true}>"
                        d2 = f"<[P = {p}, H = 0, U = {u}, G = {g}],S = {pred_false}>"
                        if d1 not in test_set:
                            test_set.append(d1)
                        if d2 not in test_set:
                            test_set.append(d2)
                    if not pred_true and not false_pred_found:
                        false_pred_found = True
                        d1 = f"<[P = {p}, H = 1, U = {u}, G = {g}],S = {pred_true}>"
                        d2 = f"<[P = {p}, H = 0, U = {u}, G = {g}],S = {pred_false}>"
                        if d1 not in test_set:
                            test_set.append(d1)
                        if d2 not in test_set:
                            test_set.append(d2)
    true_pred_found = False
    false_pred_found = False

    # U est la clause majeure
    for p in range(2):
        for h in range(2):
            for g in range(2):
                pred_true = is_message_a_spam(p, h, True, g)
                pred_false = is_message_a_spam(p, h, False, g)
                if pred_true == pred_false:
                    if pred_true and not true_pred_found:
                        true_pred_found = True
                        d1 = f"<[P = {p}, H = {h}, U = 1, G = {g}],S = {pred_true}>"
                        d2 = f"<[P = {p}, H = {h}, U = 0, G = {g}],S = {pred_false}>"
                        if d1 not in test_set:
                            test_set.append(d1)
                        if d2 not in test_set:
                            test_set.append(d2)
                    if not pred_true and not false_pred_found:
                        false_pred_found = True
                        d1 = f"<[P = {p}, H = {h}, U = 1, G = {g}],S = {pred_true}>"
                        d2 = f"<[P = {p}, H = {h}, U = 0, G = {g}],S = {pred_false}>"
                        if d1 not in test_set:
                            test_set.append(d1)
                        if d2 not in test_set:
                            test_set.append(d2)
    true_pred_found = False
    false_pred_found = False

    # G est la clause majeure
    for p in range(2):
        for h in range(2):
            for u in range(2):
                pred_true = is_message_a_spam(p, h, u, True)
                pred_false = is_message_a_spam(p, h, u, False)
                if pred_true == pred_false:
                    if pred_true and not true_pred_found:
                        true_pred_found = True
                        d1 = f"<[P = {p}, H = {h}, U = {u}, G = 1],S = {pred_true}>"
                        d2 = f"<[P = {p}, H = {h}, U = {u}, G = 0],S = {pred_false}>"
                        if d1 not in test_set:
                            test_set.append(d1)
                        if d2 not in test_set:
                            test_set.append(d2)
                    if not pred_true and not false_pred_found:
                        false_pred_found = True
                        d1 = f"<[P = {p}, H = {h}, U = {u}, G = 1],S = {pred_true}>"
                        d2 = f"<[P = {p}, H = {h}, U = {u}, G = 0],S = {pred_false}>"
                        if d1 not in test_set:
                            test_set.append(d1)
                        if d2 not in test_set:
                            test_set.append(d2)
    return test_set


def vns():
    test_set = []

    # PPF pour clause P
    test_cases_found = False
    for p in range(2):
        for h in range(2):
            for u in range(2):
                for g in range(2):
                    pred_true = is_message_spam_dnf(p, h, u, g)
                    if not test_cases_found and not pred_true and is_message_spam_dnf(not p, h, u, g):
                        test_cases_found = True
                        test_case = f"<[P = {p}, H = {h}, U = {u}, G = {g}], S = {pred_true}>"
                        if test_case not in test_set:
                            test_set.append(test_case)

    # PPF pour clause H
    test_cases_found = False
    for p in range(2):
        for h in range(2):
            for u in range(2):
                for g in range(2):
                    pred_true = is_message_spam_dnf(p, h, u, g)
                    if not test_cases_found and not pred_true and is_message_spam_dnf(not p, h, u, g):
                        test_cases_found = True
                        test_case = f"<[P = {p}, H = {h}, U = {u}, G = {g}], S = {pred_true}>"
                        if test_case not in test_set:
                            test_set.append(test_case)

    # PPF pour clause H
    test_cases_found = False
    for p in range(2):
        for h in range(2):
            for u in range(2):
                for g in range(2):
                    pred_true = is_message_spam_dnf(p, h, u, g)
                    if not test_cases_found and not pred_true and is_message_spam_dnf(p, not h, u, g):
                        test_cases_found = True
                        test_case = f"<[P = {p}, H = {h}, U = {u}, G = {g}], S = {pred_true}>"
                        if test_case not in test_set:
                            test_set.append(test_case)

    # PPF pour clause U
    test_cases_found = False
    for p in range(2):
        for h in range(2):
            for u in range(2):
                for g in range(2):
                    pred_true = is_message_spam_dnf(p, h, u, g)
                    if not test_cases_found and not pred_true and is_message_spam_dnf(p, h, not u, g):
                        test_cases_found = True
                        test_case = f"<[P = {p}, H = {h}, U = {u}, G = {g}], S = {pred_true}>"
                        if test_case not in test_set:
                            test_set.append(test_case)

    # PPF pour clause G
    test_cases_found = False
    for p in range(2):
        for h in range(2):
            for u in range(2):
                for g in range(2):
                    pred_true = is_message_spam_dnf(p, h, u, g)
                    if not test_cases_found and not pred_true and is_message_spam_dnf(p, h, u, not g):
                        test_cases_found = True
                        test_case = f"<[P = {p}, H = {h}, U = {u}, G = {g}], S = {pred_true}>"
                        if test_case not in test_set:
                            test_set.append(test_case)

    # PUV pour implicant P*H*U
    test_cases_found = False
    for p in range(2):
        for h in range(2):
            for u in range(2):
                for g in range(2):
                    pred_true = is_message_spam_dnf(p, h, u, g)
                    if not test_cases_found and p * h * u and not implicant2(p, u, g):
                        test_cases_found = True
                        test_case = f"<[P = {p}, H = {h}, U = {u}, G = {g}], S = {pred_true}>"
                        if test_case not in test_set:
                            test_set.append(test_case)

    # PPF pour implicant ~G*P*U
    test_cases_found = False
    for p in range(2):
        for h in range(2):
            for u in range(2):
                for g in range(2):
                    pred_true = is_message_spam_dnf(p, h, u, g)
                    if not test_cases_found and not p * h * u and implicant2(p, u, g):
                        test_cases_found = True
                        test_case = f"<[P = {p}, H = {h}, U = {u}, G = {g}], S = {pred_true}>"
                        if test_case not in test_set:
                            test_set.append(test_case)

    return test_set
