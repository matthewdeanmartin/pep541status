import re
from typing import List


def get_urls_in_text(text: str) -> List[str]:
    # https://stackoverflow.com/a/62723990/33264
    pattern = "(https?:((//)|(\\\\))+[\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&]*)"
    p = re.compile(pattern, re.MULTILINE)
    return [_[0] for _ in p.findall(text)]

