# 🔄 Session Continuity Protocol - Quick Reference

> **Quick cheat sheet สำหรับใช้งาน Protocol**

---

## 🚀 Quick Start (30 วินาที)

### เริ่ม Session ใหม่
```bash
# แค่พิมพ์:
"ทำต่อ"

# Claude จะ:
✅ อ่าน .project_state.json
✅ อ่าน checkpoints/checkpoint_latest.json
✅ อ่าน NEXT_SESSION.md
✅ บอกว่าทำอะไรไปแล้ว
✅ ทำงานต่อทันที
```

---

## 📋 คำสั่งพิเศษ

### ภาษาไทย
| คำสั่ง | ผลลัพธ์ |
|--------|---------|
| **"ทำต่อ"** | ทำงานต่อจาก checkpoint |
| **"สถานะ"** | แสดง progress + next steps |
| **"บันทึก"** | บันทึก checkpoint ทันที |
| **"เริ่มใหม่"** | Reset (ถามยืนยันก่อน) |
| **"ทำอะไรอยู่"** | แสดง last 3 tasks |
| **"ไฟดับ"** | กู้คืนจาก checkpoint |

### English
| Command | Result |
|---------|--------|
| **"Continue"** / **"Resume"** | Continue from checkpoint |
| **"Status"** / **"Progress"** | Show progress |
| **"Save"** / **"Checkpoint"** | Save checkpoint now |
| **"Start over"** / **"Reset"** | Reset (ask confirmation) |
| **"What was I doing?"** | Show last tasks |
| **"Crashed"** / **"Error"** | Recover from checkpoint |

### Slash Commands
| Command | Action |
|---------|--------|
| `/resume` | Resume from last checkpoint |
| `/status` | Show current progress |
| `/last-task` | Show last completed task |
| `/save` | Update all checkpoint files |
| `/what-next` | Show next steps |
| `/reset` | Start fresh (ask confirmation) |

---

## 📂 ไฟล์สำคัญ (อ่านทุก Session)

### Priority 1 - MUST READ
1. **`.project_state.json`** → สถานะโปรเจกต์
2. **`checkpoints/checkpoint_latest.json`** → Checkpoint ล่าสุด
3. **`NEXT_SESSION.md`** → คำสั่งถัดไป

### Priority 2 - Should Read
4. **`SESSION_SUMMARY.md`** → สรุป session ที่แล้ว
5. **`FINAL_SUMMARY.md`** → สรุปสุดท้าย

---

## ✅ Startup Checklist (30 วินาที)

```bash
# 1. ตรวจสอบ location (3 วินาที)
pwd

# 2. Activate venv (3 วินาที)
source .venv/bin/activate

# 3. อ่าน project state (5 วินาที)
cat .project_state.json | head -30

# 4. อ่าน checkpoint ล่าสุด (5 วินาที)
cat checkpoints/checkpoint_latest.json | head -40

# 5. อ่าน next session (5 วินาที)
cat NEXT_SESSION.md | head -50

# 6. ตรวจสอบ imports (5 วินาที)
python -c "from src.config import BASE_PATH; print(f'✅ {BASE_PATH}')"

# 7. ดู checkpoints ทั้งหมด (4 วินาที)
ls -lh checkpoints/*.json | tail -5

# ✅ พร้อมทำงาน!
```

---

## 🔄 Auto-Save Triggers

Claude จะบันทึก checkpoint อัตโนมัติเมื่อ:

1. ⏰ **ทุก 30 นาที** (time-based)
2. ✅ **เสร็จงานใหญ่** (task completion)
3. 👋 **ก่อนปิด session** (session end)
4. ⚠️ **ก่อนทำงานเสี่ยง** (safety backup)

---

## 📊 Success Indicators

### ✅ Session ทำงานได้ดี
- Context recovery < 60 วินาที
- User ถามคำถาม < 2 คำถาม
- Claude รู้ว่าทำอะไรไปแล้ว
- Claude รู้ว่าต้องทำอะไรต่อ

### ❌ Session มีปัญหา
- Claude ถาม "คุณอยากให้ทำอะไร"
- Claude เริ่มจากศูนย์
- User ต้องอธิบายซ้ำ
- Checkpoint เก่า > 24 ชั่วโมง

---

## 🎯 Expected Behavior

### เมื่อ User พิมพ์ "ทำต่อ"
```
1. Claude อ่าน .project_state.json
2. Claude อ่าน checkpoints/checkpoint_latest.json
3. Claude อ่าน NEXT_SESSION.md
4. Claude บอก: "I see from checkpoint that..."
5. Claude บอก: "Last session completed X, Y, Z"
6. Claude บอก: "Progress is at X%"
7. Claude บอก: "Next task is: ..."
8. Claude ถาม: "Should I proceed?"
```

### เมื่อ User พิมพ์ "สถานะ"
```
📊 Project Status:

✅ Completed (X%):
- Task 1
- Task 2
- Task 3

📋 Pending (Y%):
- Task 4
- Task 5

🎯 Next Task: ...

Ready to continue?
```

---

## 🔧 Troubleshooting

### ถ้า Claude ไม่อ่านไฟล์ state
```
"อ่าน .project_state.json ก่อน"
"อ่าน checkpoints/checkpoint_latest.json"
"อ่าน NEXT_SESSION.md แล้วบอกว่าต้องทำอะไรต่อ"
```

### ถ้า checkpoint หาย
```bash
# ดู checkpoint ทั้งหมด
ls -lt checkpoints/*.json

# ใช้ checkpoint รองลงมา
cat checkpoints/checkpoint_20251003_131337.json
```

---

## 📈 Progress Stages

| Progress | Stage |
|----------|-------|
| 0-20% | Setup & Configuration |
| 21-40% | Data Preparation |
| 41-70% | Model Training |
| 71-90% | Evaluation & Optimization |
| 91-100% | Deployment & Documentation |

---

## 🎉 Quick Win Examples

### Example 1: กลับมาทำงานหลัง 3 วัน
```
User: "ทำต่อ"

Claude: "I see from checkpoint_latest.json that session_001
        completed environment setup and data loading (50% progress).

        Next task: Test Session Continuity Protocol and deploy to Colab.

        Should I proceed with testing?"

User: "Yes"

Claude: [เริ่มทำงานทันที]
```

### Example 2: ไฟดับตอน training
```
User: "ไฟดับ ทำต่อจากที่ค้าง"

Claude: "Found checkpoint from 15 minutes ago:
        - Task: Training XGBoost
        - Progress: Trial 87/150

        Options:
        1. Resume from trial 87 ✅
        2. Restart training

        Which option?"

User: "1"

Claude: [กู้คืนและทำต่อ]
```

---

## 📝 Quick Notes

### Files Modified in Session 002
- ✅ CLAUDE.md (added Protocol)
- ✅ SESSION_CONTINUITY_GUIDE.md (created)
- ✅ SESSION_002_SUMMARY.md (created)
- ✅ NEXT_SESSION.md (updated)
- ✅ checkpoints/checkpoint_session_continuity.json (created)

### Progress
- Session 001: 0% → 50%
- Session 002: 50% → 80%
- Session 003: 80% → 100% (target)

### Key Achievements
- ✅ 19 components implemented
- ✅ Auto-resume with "ทำต่อ"
- ✅ 30-second recovery
- ✅ Zero context loss
- ✅ Crash-proof checkpoints

---

## 🔗 Related Files

- **Full Protocol**: `CLAUDE.md` (top section)
- **User Guide**: `SESSION_CONTINUITY_GUIDE.md`
- **Session Summary**: `SESSION_002_SUMMARY.md`
- **Next Steps**: `NEXT_SESSION.md`
- **Latest Checkpoint**: `checkpoints/checkpoint_latest.json`

---

## 💡 Pro Tips

1. **Always type "ทำต่อ" first** → Claude จะรู้ context
2. **Check "สถานะ" regularly** → เห็น progress
3. **Use "บันทึก" before risky tasks** → Safety backup
4. **Test "ไฟดับ" recovery** → Verify checkpoint works

---

**พิมพ์แค่ "ทำต่อ" → Claude ทำงานต่อทันที!** 🚀

*Last Updated: 2025-10-04*
*Version: 1.0.0*
