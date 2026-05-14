import os, json, sys, urllib.request, urllib.error

action = os.environ['EVENT_ACTION']
merged = os.environ['PR_MERGED'].lower() == 'true'

if action == 'closed':
    emoji = '🟢' if merged else '🔴'
else:
    emoji = {'opened': '🔵', 'reopened': '🔄',
             'review_requested': '👀', 'ready_for_review': '✅'}.get(action, 'ℹ️')

adds  = int(os.environ.get('PR_ADDITIONS', 0) or 0)
dels  = int(os.environ.get('PR_DELETIONS', 0) or 0)
files = int(os.environ.get('PR_CHANGED_FILES', 0) or 0)
stats_part = f' · +{adds} -{dels} · {files} files' if (adds or dels or files) else ''

repo   = os.environ['REPO_NAME']
num    = os.environ['PR_NUMBER']
title  = os.environ['PR_TITLE']
url    = os.environ['PR_URL']
author = os.environ['PR_AUTHOR']

feed_msg = f"{emoji} [{repo}] PR #{num} · {title}\n👤 {author}{stats_part}\n🔗 {url}"
proj_msg = f"{emoji} PR #{num} · {title}\n👤 {author}{stats_part}\n🔗 {url}"

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

send('1c303c142e9840f2a9b46c10b0972e8d', feed_msg)
send(os.environ['PROJECT_GROUP_ID'], proj_msg)
if failed:
    sys.exit(1)
