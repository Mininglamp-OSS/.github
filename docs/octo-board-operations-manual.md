# Octo Board — Operations Manual

> Mininglamp-OSS GitHub Project Management
> Author: 王大锤 | Date: 2026-05-12
> Project URL: https://github.com/orgs/Mininglamp-OSS/projects/2

---

## Table of Contents

1. [Setup Status](#1-setup-status)
2. [Views Configuration (Manual Steps)](#2-views-configuration)
3. [Auto-add Workflow Setup](#3-auto-add-workflow-setup)
4. [Day-to-Day Usage Guide](#4-day-to-day-usage-guide)
5. [Sprint Workflow](#5-sprint-workflow)
6. [Label & Field Reference](#6-label--field-reference)
7. [Automation Reference](#7-automation-reference)
8. [FAQ & Troubleshooting](#8-faq--troubleshooting)

---

## 1. Setup Status

### ✅ Already Configured (via API)

| Item | Status | Detail |
|------|--------|--------|
| Project created | ✅ | "Octo Board", Private, org-level |
| Repos linked | ✅ | All 10 repos linked to project |
| Custom fields | ✅ | 9 custom + 10 built-in = 19 total |
| Labels synced | ✅ | 15 standard labels across 9 repos |
| Seed data | ✅ | 8 open PRs imported |
| Built-in workflows | ✅ | 6 workflows active |
| Sprint iterations | ✅ | W20–W23 (1 week each, from 2026-05-12) |
| README | ✅ | Project description and field guide |

### ⚠️ Requires Manual Steps

| Item | Section |
|------|---------|
| 9 Views configuration | [Section 2](#2-views-configuration) |
| Org secret `PROJECT_TOKEN` | [Section 3](#3-auto-add-workflow-setup) |

---

## 2. Views Configuration

> GitHub Projects V2 的 Views 不支持 API 创建/修改，必须在 Web UI 手动配置。
> 以下是 9 个 Views 的逐步操作指南。

### How to Create a New View

1. 打开 https://github.com/orgs/Mininglamp-OSS/projects/2
2. 点击 Views 标签栏右侧的 **`＋`** 按钮
3. 选择 Layout (Table / Board / Roadmap)
4. 点击 View name（默认 "New view"）重命名
5. 按下方配置调整 Filter / Group / Sort / Columns
6. 点击 **Save changes** 保存

---

### View 1: Sprint Board ⭐

> 日常看板，团队每天看这个。对标 Kubernetes / Rust / Node.js / Vite 的 Kanban Board。

**Layout:** Board

**操作步骤：**
1. 将默认的 "View 1" 重命名为 `Sprint Board`
2. 点击右上角 Layout 图标 → 选择 **Board**
3. Board 默认按 Status 分列（如果不是，点击 column 设置选 **Status**）
4. 点击 Filter 栏，输入：
   ```
   sprint:Sprint W20
   ```
   （每周更新为当前 Sprint 名称，或等 GitHub 支持 `@current`）
5. 点击 **Sort** → 选择 **Priority** → **Descending**
6. Save changes

**最终效果：** 5 列看板（📋 Backlog → 🏗️ In Progress → 👀 In Review → ✅ Done → 🚫 Blocked），只显示当前 Sprint 的 items。

---

### View 2: Backlog

> 积压池，Sprint Planning 时从这里选任务拖入 Sprint。对标 Vite Backlog / Node.js Backlog。

**Layout:** Table

**操作步骤：**
1. 新建 View → 命名 `Backlog`
2. Layout 选 **Table**
3. Filter 栏输入：
   ```
   status:"📋 Backlog"
   ```
4. 点击 **Group** → 选择 **Module**
5. 点击 **Sort** → 选择 **Priority** → **Descending**
6. 调整列显示（点击 `+` 号添加列）：
   - ✅ Title
   - ✅ Priority
   - ✅ Module
   - ✅ Track
   - ✅ Size
   - ✅ Assignees
   - ❌ 隐藏 Status（都是 Backlog，不需要显示）
7. Save changes

---

### View 3: Roadmap

> 时间线视图，高层级里程碑规划。对标 K8s SIG-Auth Roadmap / Vite ecosystem Roadmap。

**Layout:** Roadmap

**操作步骤：**
1. 新建 View → 命名 `Roadmap`
2. Layout 选 **Roadmap**
3. 配置日期字段：
   - 点击 Roadmap 设置图标（⚙️）
   - **Start date field** → 选择 `Start Date`
   - **Target date field** → 选择 `Target Date`
4. 点击 **Group** → 选择 **Module**
5. 开启 **Markers**：
   - ✅ Iterations（显示 Sprint 分界线）
   - ✅ Milestones（如果有的话）
6. Zoom level 调为 **Month**（看全局）或 **Week**（看细节）
7. Save changes

**注意：** Roadmap 只显示设置了 Start Date 和 Target Date 的 items。创建 issue 时记得填日期。

---

### View 4: My Items

> 个人任务列表，每个团队成员收藏这个 View。对标 K8s / Vite / Rust 的 "My items"。

**Layout:** Table

**操作步骤：**
1. 新建 View → 命名 `My Items`
2. Layout 选 **Table**
3. Filter 栏输入：
   ```
   assignee:@me
   ```
4. 点击 **Sort**：
   - 第一排序：**Priority** → **Descending**
   - 第二排序：**Status** → **Ascending**
5. 调整列显示：
   - ✅ Title
   - ✅ Status
   - ✅ Priority
   - ✅ Repository
   - ✅ Sprint
   - ✅ Size
   - ✅ Linked pull requests
6. Save changes

**团队操作：** 每个成员打开此 View 后点击 ⭐ 收藏到侧边栏。

---

### View 5: Current Sprint

> 当前迭代按模块分泳道的看板。对标 Rust "Current iteration" / Node.js "Current iteration"。

**Layout:** Board

**操作步骤：**
1. 新建 View → 命名 `Current Sprint`
2. Layout 选 **Board**
3. Column field: **Status**
4. Filter 栏输入：
   ```
   sprint:Sprint W20
   ```
5. 点击 **Group** → 选择 **Module**（这会产生 swim-lane 效果）
6. Save changes

**和 Sprint Board 的区别：** Sprint Board 是纯看板，Current Sprint 按 Module 分了泳道，适合看各模块的 Sprint 进度。

---

### View 6: Triage

> 分诊视图，triage owner 专用。对标 Rust "Triage Queue" / Node.js "Need Triage"。

**Layout:** Table

**操作步骤：**
1. 新建 View → 命名 `Triage`
2. Layout 选 **Table**
3. Filter 栏输入：
   ```
   no:assignee
   ```
   （或 `label:needs-triage`，看需求）
4. 点击 **Sort** → **Created** → **Descending**（最新的在最上面）
5. 调整列显示：
   - ✅ Title
   - ✅ Repository
   - ✅ Labels
   - ✅ Priority（待设置）
   - ✅ Module（待设置）
   - ✅ Track（待设置）
6. Save changes

**用法：** Triage owner 每天/每周打开此 View，给无 assignee 的 items 指派优先级、模块、负责人。

---

### View 7: By Priority

> 按优先级分列的看板，一眼看优先级分布。对标 K8s "Priority board" / Vite "Priority board"。

**Layout:** Board

**操作步骤：**
1. 新建 View → 命名 `By Priority`
2. Layout 选 **Board**
3. 点击 column 设置 → 选择 **Priority** 作为 column field（替换默认的 Status）
4. 点击 **Sort** → **Status** → **Ascending**
5. Save changes

**效果：** 3 列（P0 🔴 / P1 🟡 / P2 🟢），加一列 "No Priority" 用于未分级的 items。

---

### View 8: OSS Readiness

> 开源合规专项追踪。对标 K8s Release Tracking 的专项追踪模式。

**Layout:** Table

**操作步骤：**
1. 新建 View → 命名 `OSS Readiness`
2. Layout 选 **Table**
3. Filter 栏输入：
   ```
   track:"📦 OSS Prep"
   ```
   如果需要包含 oss-blocker 标签的 items，改为：
   ```
   track:"📦 OSS Prep",label:oss-blocker
   ```
4. 点击 **Group** → 选择 **Module**
5. 点击 **Sort** → **Priority** → **Descending**
6. 调整列显示：
   - ✅ Title
   - ✅ Status
   - ✅ Priority
   - ✅ Module
   - ✅ Assignees
   - ✅ Notes
7. Save changes

---

### View 9: Stale Items

> 捞长期未更新的僵尸 items。对标 Node.js Node-API "Stale list"。

**Layout:** Table

**操作步骤：**
1. 新建 View → 命名 `Stale Items`
2. Layout 选 **Table**
3. Filter 栏输入：
   ```
   -status:"✅ Done"
   ```
   （排除已完成的）
4. 点击 **Sort** → **Updated** → **Ascending**（最久没更新的在最上面）
5. 调整列显示：
   - ✅ Title
   - ✅ Status
   - ✅ Assignees
   - ✅ Repository
   - ✅ Priority
   - ✅ Sprint
6. Save changes

**用法：** 每周扫一次，超过 2 周没动的 item 要么推进，要么关掉，要么标 Blocked 并写 Notes。

---

## 3. Auto-add Workflow Setup

> 已推送 `.github/workflows/auto-add-to-project.yml` 到 `.github` 仓库。
> 这个 workflow 会让所有 Mininglamp-OSS 仓库的新 issue/PR 自动加入 Octo Board。

### Step 1: Create a PAT (Personal Access Token)

1. 打开 https://github.com/settings/tokens?type=beta (Fine-grained tokens)
2. 点击 **Generate new token**
3. 配置：
   - **Token name:** `octo-board-auto-add`
   - **Expiration:** 90 days（或 custom）
   - **Resource owner:** `Mininglamp-OSS`
   - **Repository access:** All repositories
   - **Permissions:**
     - Organization permissions → **Projects**: Read and write
     - Repository permissions → **Issues**: Read-only
     - Repository permissions → **Pull requests**: Read-only
4. Generate token → 复制

### Step 2: Add Org Secret

1. 打开 https://github.com/organizations/Mininglamp-OSS/settings/secrets/actions
2. 点击 **New organization secret**
3. 配置：
   - **Name:** `PROJECT_TOKEN`
   - **Value:** 粘贴上一步的 PAT
   - **Repository access:** All repositories
4. Save

### Step 3: Verify

在任意 Mininglamp-OSS 仓库创建一个 test issue，检查：
- Issue 是否自动出现在 Octo Board
- Status 是否自动设为 📋 Backlog

---

## 4. Day-to-Day Usage Guide

### Creating Issues

在对应仓库创建 issue 时：
1. 写好 Title 和 Description
2. 设 Label（`type:feature` / `type:bug` / ...）
3. 设 Assignee
4. Issue 会自动加入 Octo Board

然后在 Octo Board 中补充 Project 字段：
- **Priority** — P0/P1/P2
- **Module** — 模块归属
- **Track** — 工作类别
- **Size** — T-shirt 估算
- **Sprint** — 分配到哪个 Sprint

### Moving Items

**Board View 中：**
- 拖拽 item 到不同列即可改变 Status
- 开始做 → 拖到 🏗️ In Progress
- 提了 PR → 拖到 👀 In Review
- 合入了 → 自动变 ✅ Done（如果 PR 关联了 issue）

**Table View 中：**
- 直接点击字段值修改

### Linking PRs to Issues

在 PR 描述中写：
```
Closes #<issue-number>
```
或
```
Fixes #<issue-number>
```

效果：
- PR 自动链接到 issue
- PR 合入后 issue 自动关闭
- Octo Board 自动标记 ✅ Done

### Cross-repo Linking

如果 issue 在 octo-server，PR 在 octo-lib：
```
Closes Mininglamp-OSS/octo-server#42
```

---

## 5. Sprint Workflow

### Weekly Sprint Cycle (每周一开始)

**Monday — Sprint Planning（30 min）**
1. 打开 **Backlog** View
2. 团队讨论优先级，选择本周要做的 items
3. 设置选中 items 的 **Sprint** 为当前周
4. 确认每个 item 有 **Assignee** 和 **Size**

**Daily — Standup Check**
1. 每个人打开 **My Items** View
2. 更新自己 items 的 Status
3. 遇到 Blocker → 标 🚫 Blocked + 写 Notes

**Friday — Sprint Review**
1. 打开 **Current Sprint** View
2. 检查哪些做完了，哪些没做完
3. 没做完的讨论是否移到下个 Sprint
4. 打开 **Stale Items** View，清理僵尸

**Weekly — Triage**
1. Triage owner 打开 **Triage** View
2. 给无 assignee 的 items 分配优先级和负责人
3. 补充 Module 和 Track 字段

### Creating New Sprints

当前 Sprint（W20–W23）用完后，需要手动添加：

1. 打开 Project → Settings（⚙️）
2. 找到 **Sprint** 字段 → 点击编辑
3. 添加新的 iteration：
   - Title: `Sprint W24`
   - Start date: 2026-06-09
   - Duration: 7 days

或由我通过 API 批量创建。

---

## 6. Label & Field Reference

### Labels (已同步到 9 个仓库)

| Category | Labels |
|----------|--------|
| Type | `type:bug` `type:feature` `type:security` `type:chore` `type:docs` `type:refactor` |
| Priority | `priority:P0` `priority:P1` `priority:P2` `priority:P3` |
| Status | `blocked` `needs-triage` |
| OSS | `good first issue` `help wanted` `oss-blocker` |

### Custom Fields

| Field | Type | Values |
|-------|------|--------|
| Status | Single Select | 📋 Backlog / 🏗️ In Progress / 👀 In Review / ✅ Done / 🚫 Blocked |
| Priority | Single Select | P0 🔴 / P1 🟡 / P2 🟢 |
| Module | Single Select | server / web / lib / admin / cli / matter / adapters / smart-summary / deployment / infra |
| Track | Single Select | 🚀 Feature / 🐛 Bug / 🔒 Security / 📦 OSS Prep / 🏗️ Infra / 📝 Docs |
| Size | Single Select | 🦔 XS / 🐇 S / 🐂 M / 🦑 L / 🐋 XL |
| Sprint | Iteration | W20 (05/12) / W21 (05/19) / W22 (05/26) / W23 (06/02) |
| Start Date | Date | Roadmap start |
| Target Date | Date | Roadmap end / deadline |
| Effort | Number | 1–8 story points |
| Notes | Text | Free-form context |

### Size Guide

| Size | Time Estimate | Example |
|------|--------------|---------|
| 🦔 XS | < 2 hours | Fix a typo, update a config |
| 🐇 S | Half day | Small bug fix, add a label |
| 🐂 M | 2–3 days | New API endpoint, component refactor |
| 🦑 L | ~1 week | Major feature, cross-repo change |
| 🐋 XL | Multi-week | Architecture change, new service |

---

## 7. Automation Reference

### Built-in Workflows (Active)

| Workflow | Trigger | Action |
|----------|---------|--------|
| Item added to project | Item added | Set Status → 📋 Backlog |
| Item closed | Issue/PR closed | Set Status → ✅ Done |
| Pull request merged | PR merged | Set Status → ✅ Done |
| Auto-close issue | Issue closed | Archive |
| Auto-add sub-issues | Parent issue added | Add sub-issues |
| Pull request linked | PR linked to issue | (default behavior) |

### GitHub Actions Workflow

File: `.github/workflows/auto-add-to-project.yml`

```yaml
name: Auto-add to Octo Board
on:
  issues:
    types: [opened]
  pull_request_target:
    types: [opened]
jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v1
        with:
          project-url: https://github.com/orgs/Mininglamp-OSS/projects/2
          github-token: ${{ secrets.PROJECT_TOKEN }}
```

**Effect:** 任何 Mininglamp-OSS 仓库中新建的 issue 或 PR 都会自动加入 Octo Board。

---

## 8. FAQ & Troubleshooting

### Q: 新建的 issue 没有自动出现在 Board？
**A:** 检查：
1. `PROJECT_TOKEN` org secret 是否已配置（Section 3）
2. Token 是否有 `project` 写权限
3. 打开仓库的 Actions 页面看 workflow 是否有报错

### Q: 怎么批量把现有 issues 加入 Board？
**A:** 在 Octo Board 右上角点 **＋ Add item** → 搜索仓库名 → 选择 issues 添加。

### Q: Sprint 到期了怎么办？
**A:** 未完成的 items 不会自动迁移。在 Sprint Planning 时手动修改 Sprint 字段到新的迭代。

### Q: 怎么看某个人的工作量？
**A:** 
- **My Items** View → `assignee:@me`
- 或在任意 Table View 中 **Group by → Assignees**

### Q: 可以在手机上用吗？
**A:** 可以。GitHub Mobile app 支持查看和编辑 Projects，但 Views 配置需要在 Web 上操作。

### Q: Board 设为 Private，外部贡献者能看到吗？
**A:** 不能。Private Project 仅 org members 可见。如果后续要开放给社区，可以改为 Public。

### Q: 一个 issue 可以同时属于多个 Sprint 吗？
**A:** 不可以。Iteration 字段是单选。如果任务跨 Sprint，建议拆子 issue。

---

## Appendix: Benchmarking Sources

本方案对标了以下顶级开源项目的 GitHub Project 设计：

| Project | Org | Views | Fields | Highlights |
|---------|-----|-------|--------|------------|
| SIG-Auth KEP Tracking | Kubernetes | 9 | 41 | 最复杂的模板：Kanban + Roadmap + Release tracking + Mass Update |
| Rust Program Management | rust-lang | 5 | 16 | 经典配置：Backlog + Board + Current Iteration + Roadmap + My Items |
| Node.js Website | nodejs | 2 | 12 | 精简高效：emoji Status + Priority + Size |
| Node.js Test Runner | nodejs | 5 | 16 | 标准配置：和 Rust PM 几乎一致 |
| Vite Team Board | vitejs | 9 | 12 | 按优先级分 View（P1/P2/P3/P4-P5），独特的分级管理 |
| Vite Ecosystem | vitejs | 4 | 15 | 标准配置 + Start/Target Date |

**共性模式提取：**
- ✅ Status 4-5 态（Backlog → In Progress → In Review → Done + Blocked/Stuck）
- ✅ Priority P0/P1/P2（部分加 P3）
- ✅ Size T-shirt（XS/S/M/L/XL）
- ✅ Sprint / Iteration
- ✅ Start Date + Target Date
- ✅ Kanban Board + Roadmap + My Items 三件套
- ✅ Triage 视图（Rust）/ Stale 视图（Node.js）

---

*Last updated: 2026-05-12 by 王大锤*
