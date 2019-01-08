#!/usr/bin/env python
import sys
import subprocess
import re
import os
import shlex

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <message-id>')
    sys.exit(0)

message_id = sys.argv[1].replace('message://', '')
print(f'Searching for message...', end='')

p = subprocess.run(['notmuch', 'search', '--output=files', f'id:{message_id}'],
                   stdout=subprocess.PIPE)

out = p.stdout.decode('utf-8')
if not out:
    print('not found.')
    sys.exit(0)
else:
    print('found.')

mail_file = out.split('\n')[0]
mail_dir = os.path.dirname(mail_file)
mail_dir = re.sub('/(cur|new|tmp)$', '', mail_dir)

# We escape the regex (because that is what neomutt wants), and then
# escape it for the shell.  I'm not sure why the latter is necessary.
escaped_id = shlex.quote(re.escape(message_id))
mutt_keys = f'push "l~i {escaped_id}\n\n"'
mutt_command = ['neomutt', '-R', '-f', mail_dir, '-e', mutt_keys]

print('Launching neomutt in new gnome-terminal...')
subprocess.run(['setsid', '-f', 'gnome-terminal', '--window', '--'] +
               mutt_command,
               stdout=subprocess.DEVNULL,
               stderr=subprocess.DEVNULL)
