def is_message_is_a_spam(p, h, u, g):
    """
        Function to test if a message is a spam using the default criteria
        p bool: true if message is classified as spom
        h bool: true is an integer indicating the duration of the history is between the 20th message date
        u bool: true if the integer indicating the user's confidence level is < 50
        g bool: true if an integer indicating the confidence level of the group is >=50
        return s: true if message is classified as spam, false if not

    """
    return p and ((h and u) or (u and not g))

def is_message_is_a_spam_dnf(p, h, u, g):
    """
        Function to test if a message is a spam using the dnf criteria
        p bool: true if message is classified as spom
        h bool: true is an integer indicating the duration of the history is between the 20th message date
        u bool: true if the integer indicating the user's confidence level is < 50
        g bool: true if an integer indicating the confidence level of the group is >=50
        return s: true if message is classified as spam, false if not
    """
    return p and h and u or p and u and not g

