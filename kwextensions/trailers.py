import re

BRANCH_HEAD_PREFIX = 'Branch-at: '
ACK_PREFIX = 'Acked-by: '
REJECTED_PREFIX = 'Rejected-by: '
TESTED_PREFIX = 'Tested-by: '

TRAILER_RE = re.compile('^[A-Z][a-zA-Z-]*: .+$')

def parse(text):
    lines = text.splitlines()
    trailers = []

    # Find trailers at the end of comments.
    for line in reversed(lines):
        if TRAILER_RE.match(line):
            trailers.append(line.split(': ', 2))
        # Accept empty lines at the end of the comment.
        elif not line and not trailers:
            continue
        else:
            break

    return reversed(trailers)
