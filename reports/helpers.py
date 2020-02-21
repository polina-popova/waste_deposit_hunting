def get_desired_width(desired_height, image):
    return round(desired_height * image.width / image.height)


def clean_up_emails(emails_string):
    clean_emails = [
        letter for letter in emails_string
        if letter not in ('[', ']', '"')
    ]
    return ''.join(clean_emails)
