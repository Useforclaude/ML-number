# 🔄 Session Continuity Protocol - Flowchart

> **Visual guide ของการทำงาน Protocol**

---

## 📊 Main Flow: Session Startup

```
┌─────────────────────────────────────────┐
│  User เปิด Claude session ใหม่          │
└─────────────────────┬───────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│  User พิมพ์คำสั่ง (เช่น "ทำต่อ")       │
└─────────────────────┬───────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │  Claude ตรวจสอบคำสั่ง  │
         └────────┬───────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
    [ทำต่อ/Continue]    [สถานะ/Status]
        │                    │
        ▼                    ▼
┌───────────────┐     ┌──────────────┐
│ READ PROTOCOL │     │ READ PROTOCOL│
│ Step 1-3      │     │ Step 1-2     │
└───────┬───────┘     └──────┬───────┘
        │                    │
        ▼                    ▼
  [Continue]            [Show Status]
        │                    │
        └─────────┬──────────┘
                  │
                  ▼
         ┌────────────────┐
         │ Work/Response  │
         └────────────────┘
```

---

## 🔍 Detailed Flow: "ทำต่อ" Command

```
User: "ทำต่อ"
    │
    ▼
┌─────────────────────────────────────────────────┐
│ STEP 1: Read .project_state.json               │
│                                                 │
│ ✓ Get current progress (X%)                    │
│ ✓ Get session_id (session_00X)                 │
│ ✓ Get completed tasks                          │
│ ✓ Get pending tasks                            │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│ STEP 2: Read checkpoints/checkpoint_latest.json│
│                                                 │
│ ✓ Get timestamp (check if < 24h)               │
│ ✓ Get current_task                             │
│ ✓ Get last_completed_task                      │
│ ✓ Get next_task                                │
│ ✓ Get files_modified                           │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│ STEP 3: Read NEXT_SESSION.md                   │
│                                                 │
│ ✓ Get immediate priority tasks                 │
│ ✓ Get step-by-step instructions                │
│ ✓ Get expected outcomes                        │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│ STEP 4: Synthesize Information                 │
│                                                 │
│ • Session X completed task Y                   │
│ • Progress is at Z%                            │
│ • Next task is: [task_description]             │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│ STEP 5: Present to User                        │
│                                                 │
│ "I see from checkpoint that session_001        │
│  completed [tasks]. Progress is at 75%.        │
│  Next task: [description].                     │
│  Should I proceed?"                            │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
            ┌─────────┴─────────┐
            │                   │
            ▼                   ▼
        [Yes/OK]            [No/Wait]
            │                   │
            ▼                   │
    ┌──────────────┐            │
    │ Start Work   │            │
    └──────────────┘            │
                                │
                                ▼
                        ┌───────────────┐
                        │ Wait for User │
                        └───────────────┘
```

---

## 💾 Auto-Checkpoint Flow

```
                    ┌─────────────────┐
                    │  Claude Working │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Check Triggers  │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    [30min elapsed]   [Task Complete]   [Session Ending]
            │                │                │
            └────────────────┼────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Create Checkpoint:
                    │ {
                    │   timestamp: "...",
                    │   session_id: "...",
                    │   current_task: "...",
                    │   next_task: "...",
                    │   progress: X%,
                    │   files_modified: [...]
                    │ }
                    └────────┬───────┘
                             │
                    ┌────────▼────────┐
                    │ Save to:        │
                    │ • checkpoint_latest.json
                    │ • checkpoint_YYYYMMDD_HHMMSS.json
                    │ • .project_state.json
                    └────────┬────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Continue Work  │
                    └────────────────┘
```

---

## 🚨 Error Recovery Flow

```
        ┌────────────────────┐
        │ Error Occurs/      │
        │ ไฟดับ/Crash        │
        └─────────┬──────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │ User Opens New      │
        │ Session             │
        └─────────┬───────────┘
                  │
                  ▼
        User: "ไฟดับ ทำต่อจากที่ค้าง"
                  │
                  ▼
        ┌─────────────────────────────┐
        │ Claude Reads Last Checkpoint│
        └─────────┬───────────────────┘
                  │
                  ▼
        ┌─────────────────────────────┐
        │ Check Timestamp             │
        └─────────┬───────────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
    [< 1 hour ago]      [> 1 hour ago]
        │                    │
        ▼                    ▼
    [Highly Reliable]   [Ask Confirmation]
        │                    │
        └─────────┬──────────┘
                  │
                  ▼
        ┌─────────────────────────────┐
        │ Present Recovery Options:   │
        │                             │
        │ 1. Resume from checkpoint   │
        │ 2. Show details first       │
        │ 3. Start fresh              │
        └─────────┬───────────────────┘
                  │
                  ▼
        ┌─────────────────┐
        │ User Chooses    │
        └─────────┬───────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
    [Option 1]          [Option 3]
    Resume              Start Fresh
        │                   │
        ▼                   ▼
    [Continue Work]     [New Session]
```

---

## 📋 Session Quality Check Flow

```
                ┌──────────────────┐
                │ Session Running  │
                └────────┬─────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │ Check Quality Metrics  │
            └────────┬───────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    [Recovery    [User         [Checkpoint
     Time]        Questions]    Updated]
        │            │            │
        ▼            ▼            ▼
    [< 60s?]     [< 2?]       [Has timestamp?]
        │            │            │
        ▼            ▼            ▼
    ┌────────────────────────────┐
    │ All Green (✅)?            │
    └────────┬───────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
  [YES]             [NO]
    │                 │
    ▼                 ▼
[PASS ✅]        [FAIL ❌]
    │                 │
    │                 ▼
    │         ┌───────────────┐
    │         │ Identify Issue│
    │         └───────┬───────┘
    │                 │
    │         ┌───────▼───────────┐
    │         │ • Missing checkpoint?
    │         │ • Old checkpoint?
    │         │ • Context loss?
    │         └───────┬───────────┘
    │                 │
    │                 ▼
    │         ┌───────────────┐
    │         │ Apply Fix     │
    │         └───────────────┘
    │                 │
    └─────────────────┘
```

---

## 🔄 Session Chain Flow

```
Session 001 (2025-10-03)
    │
    ├─ Tasks: Environment setup, data loading
    ├─ Progress: 0% → 50%
    ├─ Files: 11 created/modified
    │
    ├─ Checkpoint: checkpoint_20251003_131638.json
    │   {
    │     "session_id": "session_001",
    │     "parent_session": null,
    │     "milestone": "Environment Setup Complete"
    │   }
    │
    └─────────┬──────────────────────────
              │
              ▼
Session 002 (2025-10-04)
    │
    ├─ Parent: session_001
    ├─ Tasks: Session Continuity Protocol
    ├─ Progress: 50% → 80%
    ├─ Files: 4 created/modified
    │
    ├─ Checkpoint: checkpoint_session_continuity.json
    │   {
    │     "session_id": "session_002",
    │     "parent_session": "session_001",
    │     "milestone": "Protocol Implementation Complete"
    │   }
    │
    └─────────┬──────────────────────────
              │
              ▼
Session 003 (Next Session)
    │
    ├─ Parent: session_002
    ├─ Tasks: Test protocol, final deployment
    ├─ Progress: 80% → 100% (target)
    ├─ Files: Deploy to Colab/Kaggle
    │
    ├─ Checkpoint: checkpoint_final.json
    │   {
    │     "session_id": "session_003",
    │     "parent_session": "session_002",
    │     "milestone": "Project Complete"
    │   }
    │
    └─────────▼──────────────────────────
          [COMPLETE]
```

---

## 🎯 Decision Tree: User Intent Recognition

```
                User Input
                    │
        ┌───────────┼────────────┐
        │           │            │
        ▼           ▼            ▼
    [Thai]      [English]   [Slash Cmd]
        │           │            │
        ▼           ▼            ▼
    ┌──────────────────────────────┐
    │ Match Pattern                │
    └───────────┬──────────────────┘
                │
    ┌───────────┼──────────────┐
    │           │              │
    ▼           ▼              ▼
["ทำต่อ"]  ["Status"]    ["/resume"]
    │           │              │
    ▼           ▼              ▼
Continuation  Status Check  Quick Command
  Intent        Intent         Intent
    │           │              │
    └───────────┼──────────────┘
                │
                ▼
        ┌───────────────┐
        │ Execute Action│
        └───────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
[Read State] [Show Info] [Perform Action]
```

---

## 📊 Progress Calculation Flow

```
            ┌─────────────────┐
            │ Calculate       │
            │ Progress        │
            └────────┬────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
    [Simple Method]         [Weighted Method]
        │                         │
        ▼                         ▼
    completed_tasks         environment_setup * 0.15
    ───────────────         + data_loading * 0.10
    total_tasks             + feature_eng * 0.20
    × 100%                  + model_training * 0.30
        │                   + evaluation * 0.10
        │                   + deployment * 0.15
        │                         │
        └────────────┬────────────┘
                     │
                     ▼
            ┌────────────────┐
            │ Return:        │
            │ {              │
            │   simple: X%,  │
            │   weighted: Y%,│
            │   stage: "..." │
            │ }              │
            └────────────────┘
```

---

## 🔍 Checkpoint Validation Flow

```
        ┌─────────────────────┐
        │ Load Checkpoint     │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Validate Checkpoint │
        └──────────┬──────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
    [Timestamp]          [Completeness]
        │                     │
        ▼                     ▼
    Age < 24h?           All fields?
        │                     │
        ▼                     ▼
    ┌─────────────────────────┐
    │ Consistency Check       │
    └──────────┬──────────────┘
               │
               ▼
    Does .project_state.json
    match checkpoint?
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
      [YES]         [NO]
        │             │
        ▼             ▼
    [File Check]  [WARN: Inconsistent]
        │             │
        ▼             │
    Files exist?      │
        │             │
        ▼             │
    ┌──────┬──────────┘
    │      │
    ▼      ▼
  [PASS] [FAIL]
    │      │
    ▼      ▼
  [Use]  [Ask User]
```

---

## 🎨 Visual Summary

### Protocol ทำงานเป็น 3 Layer:

```
┌─────────────────────────────────────────┐
│  LAYER 1: User Interface                │
│  • Thai/English commands                │
│  • Slash commands                       │
│  • Pattern recognition                  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  LAYER 2: State Management              │
│  • Read .project_state.json             │
│  • Read checkpoints/*.json              │
│  • Read NEXT_SESSION.md                 │
│  • Validate & synthesize                │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  LAYER 3: Action Execution              │
│  • Continue work                        │
│  • Show status                          │
│  • Save checkpoint                      │
│  • Recover from error                   │
└─────────────────────────────────────────┘
```

---

## 📈 Flow Optimization

### Before Protocol (ช้า):
```
User Input → Claude Confused → Ask Questions → User Explains
→ Claude Understands → Start Work
(⏱️ 5-10 minutes)
```

### After Protocol (เร็ว):
```
User Input ("ทำต่อ") → Claude Reads State → Start Work
(⏱️ 30 seconds)
```

**Time Saved: 90%** 🚀

---

## 🎯 Key Takeaways

1. **"ทำต่อ" triggers 3-step read**: `.project_state.json` → `checkpoint_latest.json` → `NEXT_SESSION.md`

2. **Auto-save triggers**: 30min timer, task completion, session end, risky operation

3. **Quality check**: Recovery time, user questions, checkpoint freshness

4. **Session chain**: Each session links to parent via `session_id`

5. **Error recovery**: Check timestamp → Offer options → Resume work

---

**พิมพ์แค่ "ทำต่อ" → Claude ทำงานต่อทันที!** 🚀

*Created: 2025-10-04*
*Part of Session Continuity Protocol*
