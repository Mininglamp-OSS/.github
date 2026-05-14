import os, json, urllib.request, urllib.error, sys

conclusion = os.environ['CONCLUSION']
# Cancelled runs are not real failures; skip silently
if conclusion == 'cancelled':
    print('Cancelled run, skipping.')
    sys.exit(0)

repo      = os.environ['REPO_NAME']
wf_name   = os.environ['WORKFLOW_NAME']
run_url   = os.environ['RUN_URL']
proj_gid  = os.environ['PROJECT_GROUP_ID']
gh_token  = os.environ['GITHUB_TOKEN']
bot_token = os.environ['OCTO_BOT_TOKEN']

# Fetch recent completed runs on main branch
api_url = (
    f'https://api.github.com/repos/Mininglamp-OSS/{repo}/actions/runs'
    f'?branch=main&status=completed&per_page=10'
)
req = urllib.request.Request(api_url, headers={
    'Authorization': f'Bearer {gh_token}',
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
})
try:
    with urllib.request.urlopen(req, timeout=15) as r:
        runs = json.load(r)['workflow_runs']
except (urllib.error.HTTPError, urllib.error.URLError) as e:
    print(f'ERROR: failed to fetch workflow runs: {e}')
    sys.exit(1)

# Filter to the same workflow by name
same_wf = [r for r in runs if r['name'] == wf_name]

if not same_wf:
    print('No matching runs found, skipping.')
    sys.exit(0)

# Use run_id to precisely identify the current run (avoids race conditions
# when two runs complete close together).
run_id = int(os.environ.get('RUN_ID', 0))
matched = [r for r in same_wf if r['id'] == run_id]
if not matched:
    print('WARN: run_id %s not found in recent runs window, falling back to same_wf[0]' % run_id)
current  = matched[0] if matched else same_wf[0]
# Only consider runs created before current to avoid picking a later
# concurrent run as "previous" (which would flip alert/recovery semantics).
older    = [r for r in same_wf
            if r['id'] != current['id']
            and r['created_at'] < current['created_at']]
previous = older[0] if older else None

curr_conclusion = current['conclusion']
prev_conclusion = previous['conclusion'] if previous else None

print(f'State: {prev_conclusion} → {curr_conclusion}')

# Only act on state changes
if curr_conclusion == prev_conclusion:
    print('No state change, silent.')
    sys.exit(0)

# Guard: first-ever run has no previous history — skip silently
if prev_conclusion is None:
    print('First run detected (no previous history), skipping notification.')
    sys.exit(0)

# Determine message
if curr_conclusion == 'failure':
    msg = (
        f'❌ [{repo}] main CI 挂了\n\n'
        f'工作流：{wf_name}\n'
        f'🔗 {run_url}'
    )
elif curr_conclusion == 'success' and prev_conclusion == 'failure':
    msg = (
        f'✅ [{repo}] main CI 已恢复\n\n'
        f'工作流：{wf_name}\n'
        f'🔗 {run_url}'
    )
else:
    print(f'Unhandled transition {prev_conclusion!r} → {curr_conclusion!r}, skipping.')
    sys.exit(0)

# Send to Octo IM
send_url = 'https://im.deepminer.com.cn/api/v1/bot/sendMessage'
headers  = {
    'Authorization': f'Bearer {bot_token}',
    'Content-Type': 'application/json',
}

failed = []

def send(group_id, message):
    body = json.dumps({
        'channel_id': group_id,
        'channel_type': 2,
        'payload': {'type': 1, 'content': message},
    }).encode()
    req = urllib.request.Request(send_url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f'  → {group_id[:8]}... HTTP {r.status}')
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f'ERROR: failed to send message to {group_id[:8]}...: {e}')
        failed.append(group_id)

# Push to ci-status group and the repo's project group
send('4ade985d984e432eb7fbdd0ad4f8118a', msg)
send(proj_gid, msg)
if failed:
    sys.exit(1)
