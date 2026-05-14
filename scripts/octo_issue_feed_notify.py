import os, json, sys, urllib.request, urllib.error

action = os.environ['EVENT_ACTION']
emoji = {'opened': '🆕', 'closed': '✅', 'reopened': '🔄', 'labeled': '🏷️'}.get(action, 'ℹ️')

try:
    labels = json.loads(os.environ['ISSUE_LABELS'])
    labels_part = ' · 🏷️ ' + ', '.join(labels) if labels else ''
except Exception:
    labels_part = ''

repo  = os.environ['REPO_NAME']
num   = os.environ['ISSUE_NUMBER']
title = os.environ['ISSUE_TITLE']
url   = os.environ['ISSUE_URL']
author = os.environ['ISSUE_AUTHOR']

feed_msg = f"{emoji} [{repo}] Issue #{num} · {title}\n👤 {author}{labels_part}\n🔗 {url}"
proj_msg = f"{emoji} Issue #{num} · {title}\n👤 {author}{labels_part}\n🔗 {url}"

api = 'https://im.deepminer.com.cn/api/v1/bot/sendMessage'
token = os.environ['OCTO_BOT_TOKEN']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

failed = []

def send(group_id, msg):
    body = json.dumps({'channel_id': group_id, 'channel_type': 2,
                       'payload': {'type': 1, 'content': msg}}).encode()
    req = urllib.request.Request(api, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f'→ {group_id[:8]}... {r.status}')
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f'ERROR: failed to send message to {group_id[:8]}...: {e}')
        failed.append(group_id)

send('151a45970e1546afa9e947ac36a5c4e5', feed_msg)
send(os.environ['PROJECT_GROUP_ID'], proj_msg)
if failed:
    sys.exit(1)
