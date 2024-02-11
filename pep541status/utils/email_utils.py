import re
from typing import List

from email_validator import validate_email, EmailNotValidError

def is_email_good(email):
    try:
      # Validate.
      valid = validate_email(email, check_deliverability=False)

      # Update with the normalized form.
      email = valid.email
      return True
    except EmailNotValidError as e:
      # email is not valid, exception message is human-readable
      # print(str(e))
      return False

def get_emails_in_text(text:str)->List[str]:
    # https://stackoverflow.com/a/62723990/33264
    p = re.compile(r"[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+", re.MULTILINE)
    return [_ for _ in p.findall(text) if is_email_good(_) and "." in _ and len(_)>4]
