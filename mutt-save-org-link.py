#!/usr/bin/env python3

import sys
import email
import subprocess

message_bytes = sys.stdin.buffer.read()
message = email.message_from_bytes(message_bytes)

message_id = message['message-id'][1:-1]
subject = message['subject']

subprocess.Popen([
    'emacsclient',
    f'org-protocol://store-link?url=mutt:{message_id}&title={subject}'
])
