# /utils/filters.py

def filter_by_keywords(email_content, keywords):
    """Filter email content by a list of keywords."""
    for keyword in keywords:
        if keyword in email_content:
            return True
    return False
