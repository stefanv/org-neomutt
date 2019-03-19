#!/usr/bin/env python3

import sys
import email
import subprocess
import urllib.parse

# Parse the email from standard input
message_bytes = sys.stdin.buffer.read()
message = email.message_from_bytes(message_bytes)

# Grab the relevant message headers
message_id = urllib.parse.quote(message['message-id'].strip()[1:-1])
subject = message['subject'].replace('[', '{').replace(']', '}')

# Ask emacsclient to save a link to the message
p = subprocess.Popen([
    'emacsclient',
    f'org-protocol://store-link?url=message://{message_id}&title={subject}'
])

p.wait()
