#!/usr/bin/env python3

import sys
import email
import subprocess
import urllib.parse

message_bytes = sys.stdin.buffer.read()
message = email.message_from_bytes(message_bytes)

message_id = urllib.parse.quote(message['message-id'][1:-1])
subject = message['subject']

subprocess.Popen([
    'emacsclient',
    f'org-protocol://store-link?url=message://{message_id}&title={subject}'
])
