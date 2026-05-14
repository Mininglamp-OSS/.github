import os, json, sys, time, urllib.request, urllib.error


def require_env(name):
    val = os.environ.get(name, '').strip()
    if not val:
        print(f'ERROR: required environment variable {name} is missing or empty')
        sys.exit(2)
    return val


action = require_env('EVENT_ACTION')
merged = require_env('PR_MERGED').lower() == 'true'

if action == 'closed':
    emoji = '🟢' if merged else '🔴'
else:
    emoji = {'opened': '🔵', 'reopened': '🔄',
             'review_requested': '👀', 'ready_for_review': '✅'}.get(action, 'ℹ️')

adds  = int(os.environ.get('PR_ADDITIONS', 0) or 0)
dels  = int(os.environ.get('PR_DELETIONS', 0) or 0)
files = int(os.environ.get('PR_CHANGED_FILES', 0) or 0)
stats_part = f' · +{adds} -{dels} · {files} files' if (adds or dels or files) else ''

repo   = require_env('REPO_NAME')
num    = require_env('PR_NUMBER')
title  = require_env('PR_TITLE')
url    = require_env('PR_URL')
author = require_env('PR_AUTHOR')

feed_msg = f"{emoji} [{repo}] PR #{num} · {title}\n👤 {author}{stats_part}\n🔗 {url}"
proj_msg = f"{emoji} PR #{num} · {title}\n👤 {author}{stats_part}\n🔗 {url}"

api = 'https://im.deepminer.com.cn/api/v1/bot/sendMessage'
token = require_env('OCTO_BOT_TOKEN')
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

failed = []

def send(group_id, message):
    body = json.dumps({
        'channel_id': group_id,
        'channel_type': 2,
        'payload': {'type': 1, 'content': message},
    }).encode()
    last_err = None
    for attempt in range(1, 4):
        req = urllib.request.Request(api, data=body, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                print(f'  → {group_id[:8]}... HTTP {r.status}')
                return  # success
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504) and attempt < 3:
                wait = 2 ** attempt
                print(f'  WARN: HTTP {e.code} on attempt {attempt}, retrying in {wait}s...')
                time.sleep(wait)
            else:
                break
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            if attempt < 3:
                wait = 2 ** attempt
                print(f'  WARN: {e} on attempt {attempt}, retrying in {wait}s...')
                time.sleep(wait)
            else:
                break
    print(f'ERROR: failed to send message to {group_id[:8]}...: {last_err}')
    failed.append(group_id)

proj_gid = require_env('PROJECT_GROUP_ID')
send('1c303c142e9840f2a9b46c10b0972e8d', feed_msg)
send(proj_gid, proj_msg)
if failed:
    sys.exit(1)
