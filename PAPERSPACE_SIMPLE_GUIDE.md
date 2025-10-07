# 🚀 Paperspace Simple Guide - เริ่มต้นจากศูนย์

**สำหรับ**: ถอดเสียงวิดีโอภาษาไทยด้วย Whisper บน Paperspace
**แพ็กเกจ**: Growth Plan ($8/month) - RTX A4000 GPU (แนะนำ)
**ระดับ**: เริ่มต้นจาก New Notebook เปล่าๆ
**เวอร์ชัน**: 4.0 - Added Technical Deep Dive: Terminal vs Notebook architecture, process management, platform comparison (2025-10-07)

---

## 📋 ภาพรวม

**คู่มือนี้จะพาคุณทำตามลำดับ:**

```
1. สร้างโฟลเดอร์ (Jupyter UI)          → 5 นาที
2. ติดตั้ง Whisper (Terminal)          → 5 นาที
3. สร้าง Python Script (Jupyter UI)    → 5 นาที
4. Upload วิดีโอ (Google Drive/gdown)  → 2-4 นาที ⭐
5. ถอดเสียง (Terminal)                 → 3-8 นาที ⚡
6. Download ผลลัพธ์ (Jupyter UI)       → 2 นาที
───────────────────────────────────────────────────
รวม: 22-29 นาที (สำหรับวิดีโอ 1 ชม., 1.5 GB, RTX A4000)

⭐ ใช้ gdown เร็วกว่า Jupyter UI Upload 5-10 เท่า!
⚡ ถ้าใช้ RTX 5000 Ada → ถอดเสียง 2.5-3 นาที (เร็วกว่า!)
```

**💡 เวลาถอดเสียงขึ้นกับ GPU:**
- **RTX 5000 Ada**: วิดีโอ 1 ชม. → **2.5-3 นาที** (เร็วที่สุด!)
- **RTX 4000 Ada**: วิดีโอ 1 ชม. → **3-4 นาที**
- **RTX A4000**: วิดีโอ 1 ชม. → **3-6 นาที** (ใช้ในคู่มือนี้)
- **P5000**: วิดีโอ 1 ชม. → **5-8 นาที**

ดูรายละเอียดเพิ่มเติม: PART 5 → เปรียบเทียบ GPU

---

## 🤔 Terminal vs Notebook - ต่างกันยังไง?

**คำถามที่ถามบ่อย:**
> "ทำใน Terminal หมดเลยเหรอ? ไม่ต้องใช้ Notebook (.ipynb) เลย?"
> "ประสิทธิภาพต่างกันมั้ย?"

---

### 📊 Paperspace Jupyter Lab มี 2 ส่วน

```
┌─────────────────────────────────────────┐
│     Paperspace Jupyter Lab              │
├─────────────────────────────────────────┤
│                                         │
│  1. Jupyter UI (File Browser)          │
│     → สร้าง/ลบไฟล์, drag & drop        │
│     → ไม่ใช่ Notebook!                  │
│                                         │
│  2. Terminal (Command Line)             │
│     → รันคำสั่ง, pip install, python    │
│     → ใช้ส่วนนี้เป็นหลัก!               │
│                                         │
│  3. Notebook (.ipynb) [ไม่ใช้ในคู่มือนี้]│
│     → Interactive cells                 │
│     → สำหรับ exploration/visualization  │
│                                         │
└─────────────────────────────────────────┘
```

---

### ✅ คู่มือนี้ใช้อะไรบ้าง?

**ใช้ส่วนไหน:**

| PART | ใช้อะไร | ทำอะไร |
|------|---------|--------|
| **PART 1-3** | **Jupyter UI** | สร้างโฟลเดอร์, สร้างไฟล์ .py |
| **PART 2** | **Terminal** | pip install, ติดตั้ง Whisper |
| **PART 4** | **Terminal** | gdown, upload วิดีโอ |
| **PART 5** | **Terminal** | รัน Python script ถอดเสียง |
| **PART 6** | **Jupyter UI** | Download ไฟล์ transcript |

**🎯 สรุป:**
- ✅ **Jupyter UI** - สร้าง/download ไฟล์ (file manager)
- ✅ **Terminal** - รันคำสั่งทั้งหมด (หลัก!)
- ❌ **Notebook (.ipynb)** - ไม่ใช้เลย!

---

### 🔍 ความแตกต่าง Terminal vs Notebook

| | **Terminal** | **Notebook (.ipynb)** |
|---|--------------|---------------------|
| **รูปแบบ** | Command line (ดำๆ) | Interactive cells |
| **รันคำสั่ง** | `python script.py` | Cell-by-cell |
| **เหมาะกับ** | Scripts, long tasks | Exploration, visualize |
| **Timeout** | ไม่มี (background OK) | มี (idle → disconnect) |
| **Output** | Linear, streaming | Cell output |
| **GPU** | ใช้ได้ ✓ | ใช้ได้ ✓ |
| **ประสิทธิภาพ** | **เหมือนกัน!** | **เหมือนกัน!** |
| **ใช้ในคู่มือ** | ✅ ใช้เป็นหลัก | ❌ ไม่ใช้ |

---

### ⚡ ประสิทธิภาพ - เหมือนกันหรือไม่?

```
✅ เหมือนกันทุกอย่าง!

ทั้ง Terminal และ Notebook ใช้:
- GPU เดียวกัน (RTX A4000)
- RAM เดียวกัน
- CPU เดียวกัน
- VRAM เดียวกัน

ไม่มีความแตกต่างด้าน performance เลย!
```

**🔍 อธิบาย:**
- Terminal: รัน `python script.py` → ใช้ Python interpreter
- Notebook: รัน cell → ใช้ Python interpreter **เดียวกัน**
- ทั้งสองเข้าถึง GPU ได้เหมือนกัน

**ตัวอย่าง:**
```bash
# Terminal
python whisper_transcribe.py video.mp4
→ ใช้ GPU RTX A4000 ✓

# Notebook cell
!python whisper_transcribe.py video.mp4
→ ใช้ GPU RTX A4000 ✓  (เหมือนกัน!)
```

---

### 🤔 ถ้าเหมือนกัน ทำไม Notebook ถึง Timeout?

**คำถามที่ดี!** ให้อธิบายความแตกต่างที่สำคัญ:

```
ประสิทธิภาพ (Performance) ≠ Connection Management
```

---

#### 📊 ความแตกต่างที่แท้จริง:

| Aspect | Terminal | Notebook |
|--------|----------|----------|
| **Performance** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡⚡ **(เหมือนกัน!)** |
| **GPU Access** | ✅ เต็มที่ | ✅ เต็มที่ **(เหมือนกัน!)** |
| **ความเร็ว** | เร็ว | เร็ว **(เหมือนกัน!)** |
| | | |
| **Connection** | 🔌 Independent | 🔗 Browser-dependent **(ต่างกัน!)** |
| **Timeout Risk** | ❌ ไม่มี | ⚠️ มี **(ต่างกัน!)** |
| **Background Run** | ✅ ได้ | ❌ ไม่ได้ **(ต่างกัน!)** |

---

#### 🔍 เหตุผลที่ Notebook Timeout (แต่ Performance เหมือนกัน):

**ไม่ใช่เพราะช้า - แต่เพราะ Connection!**

```
┌─────────────────────────────────────────────┐
│           Terminal Process                  │
├─────────────────────────────────────────────┤
│                                             │
│  Browser → Paperspace Server               │
│              ↓                              │
│         Terminal (bash)                     │
│              ↓                              │
│    python script.py (รันอิสระ)             │
│              ↓                              │
│            GPU ⚡                            │
│                                             │
│  ✅ ปิด browser → process ยังทำงานต่อ!      │
│  ✅ Network ขาด → process ยังทำงานต่อ!       │
│                                             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│         Notebook Cell Process               │
├─────────────────────────────────────────────┤
│                                             │
│  Browser ↔ Jupyter Kernel ↔ Python Process │
│     ↕          ↕              ↕             │
│  Activity   Heartbeat        GPU ⚡          │
│                                             │
│  ❌ ปิด browser → kernel ตาย → process หยุด!│
│  ❌ Network ขาด → kernel ตาย → process หยุด!│
│  ❌ Idle นาน → kernel timeout → process หยุด!│
│                                             │
└─────────────────────────────────────────────┘
```

---

#### 💡 อธิบายแบบง่าย:

**Terminal:**
```
1. คุณสั่ง: python script.py
2. Terminal รัน process แยกต่างหาก
3. คุณปิด browser → process ยังทำงานต่อ ✓
4. Internet ขาด → process ยังทำงานต่อ ✓
5. คุณไปนอน → process ยังทำงานต่อ ✓

เหมือนปล่อยให้รถวิ่งเอง (autopilot)
```

**Notebook:**
```
1. คุณสั่ง: !python script.py (ใน cell)
2. Jupyter Kernel รัน process
3. Kernel ต้อง "คุย" กับ browser ตลอดเวลา (heartbeat)
4. คุณปิด browser → Kernel ตัดการเชื่อมต่อ → process หยุด ✗
5. Internet ขาด → Kernel ตาย → process หยุด ✗
6. ไม่มี activity → Kernel timeout → process หยุด ✗

เหมือนต้องบังคับรถเอง (ถ้าปล่อยมือ → รถหยุด)
```

---

#### 📋 ตัวอย่างจริง:

**Scenario: ถอดเสียงวิดีโอ 1 ชั่วโมง (ใช้เวลา 5 นาที)**

**Terminal:**
```bash
# รันคำสั่ง
python whisper_transcribe.py video.mp4

# นาทีที่ 1: ✅ ทำงาน (GPU 100%)
# นาทีที่ 2: ✅ ทำงาน
# คุณปิด browser ไปทำธุระ...
# นาทีที่ 3: ✅ ยังทำงานต่อ!
# นาทีที่ 4: ✅ ยังทำงานต่อ!
# นาทีที่ 5: ✅ เสร็จ! ไฟล์พร้อม
```

**Notebook:**
```python
# รันใน cell
!python whisper_transcribe.py video.mp4

# นาทีที่ 1: ✅ ทำงาน (GPU 100%)
# นาทีที่ 2: ✅ ทำงาน
# คุณปิด browser ไปทำธุระ...
# นาทีที่ 3: ❌ Kernel ตาย! (ไม่มี browser connection)
# ผลลัพธ์: Process หยุดกลางคัน, ไม่มีไฟล์!

# หรือ:
# นาทีที่ 1-2: ทำงานปกติ
# คุณเปิด browser ค้างแต่ไม่กด/คลิกอะไร
# นาทีที่ 3: Jupyter คิดว่า "idle"
# นาทีที่ 5: ❌ Kernel timeout! (ไม่มี user activity)
```

---

#### 🎯 สรุป - ตอบคำถาม "ทำไมถึง Timeout?"

**ไม่เกี่ยวกับ Performance เลย!**

| เรื่อง | Terminal | Notebook |
|--------|----------|----------|
| **ความเร็ว** | เร็ว | เร็ว **(เหมือนกัน!)** |
| **GPU** | ใช้เต็มที่ | ใช้เต็มที่ **(เหมือนกัน!)** |
| **Connection** | อิสระ | ต้องเชื่อมต่อ browser **(ต่างกัน!)** |
| **Timeout** | ไม่มี | มี **(ต่างกัน!)** |

**Notebook timeout เพราะ:**
- ❌ Connection management (ต้องเชื่อมต่อ browser)
- ❌ Kernel heartbeat (ต้องมี activity)
- ❌ Idle timeout (ไม่มี user interaction)

**ไม่ใช่เพราะ:**
- ✅ ช้ากว่า (เร็วเท่ากัน!)
- ✅ GPU น้อยกว่า (ใช้เต็มที่เท่ากัน!)
- ✅ ประสิทธิภาพต่ำกว่า (เหมือนกัน!)

---

### 🔬 Technical Deep Dive: ทำไม Notebook ถึงหาย?

**คำถาม:** "รันใน Notebook ถึงหยุด แต่ Terminal ไม่หยุด - ไม่เหมือนกันเหรอ?"

**คำตอบ:** ไม่เหมือนกันครับ! มาดูความแตกต่างแบบละเอียด:

---

#### 🏗️ Process Architecture

**Terminal Process:**
```
Terminal:
  python script.py
       ↓
  สร้าง Python Process (PID: 12345)
       ↓
  Process รัน "อิสระ" บน Linux kernel
       ↓
  ไม่ต้องการ browser connection
       ↓
  ✅ ปิด browser → Process ยังอยู่
```

```bash
# Process tree จริง:
bash (PID: 100)
  └─ python script.py (PID: 200)  ← Process อิสระ

# Process 200 ไม่ขึ้นกับ browser
# รันบน Paperspace server โดยตรง
```

**Notebook Kernel Process:**
```
Notebook Cell:
  รัน code ใน cell
       ↓
  Jupyter Kernel execute code
       ↓
  Kernel ต้องการ "heartbeat" จาก browser
       ↓
  Browser <─WebSocket─> Kernel
       ↓
  ❌ ปิด browser → WebSocket disconnect
       ↓
  ❌ Kernel timeout → execution หยุด
```

```bash
# Process tree จริง:
jupyter-notebook (PID: 50)
  └─ kernel (PID: 60)
       └─ python execution (PID: 70)

# Process 70 ขึ้นกับ Kernel (PID 60)
# Kernel ต้องการ WebSocket connection
# ไม่มี connection → Kernel ตาย → Process หยุด
```

---

#### 🔌 Connection Management

**Terminal:**
```
Browser
   ↓ (แค่แสดงผล - Display only)
Terminal UI
   ↓
bash process (รันอิสระ)
   ↓
python script.py

✅ ปิด browser = แค่หน้าจอหาย
✅ Process ยังรันต่อบน server
```

**Notebook:**
```
Browser
   ↕ (WebSocket - Two-way communication!)
Jupyter Server
   ↕ (Heartbeat every 30s)
Kernel
   ↓
python execution

❌ ปิด browser = WebSocket ขาด
❌ Kernel timeout → หยุดทันที
```

---

#### 📡 Heartbeat Mechanism

**Notebook มี "Heartbeat" ที่ Terminal ไม่มี:**

```javascript
// Browser ส่ง heartbeat ทุก 30 วินาที
setInterval(() => {
  websocket.send('ping');  // ส่งสัญญาณว่ายังอยู่
}, 30000);

// ถ้า Kernel ไม่ได้รับ ping 2-3 รอบ
// → คิดว่า browser disconnect
// → Kernel shutdown
```

**Terminal ไม่มี Heartbeat:**
```bash
# Terminal แค่ส่งคำสั่งไปครั้งเดียว:
python script.py

# หลังจากนั้น process รันเอง
# ไม่ต้องการสัญญาณจาก browser
```

---

#### 🧪 ทดสอบจริง (Proof)

**Test 1: Terminal (ไม่หาย)**

```bash
# 1. รันใน Terminal
cd /notebooks/thai-whisper
python scripts/whisper_transcribe.py videos/test.mp4 &
echo $!  # จด PID (เช่น 12345)

# 2. เช็ค process
ps aux | grep 12345
# Output: root 12345 python scripts/whisper_transcribe.py

# 3. ปิดบราวเซอร์ทิ้งไว้ 5 นาที

# 4. เปิดบราวเซอร์ใหม่ → Terminal
ps aux | grep 12345
# ✅ ยังเห็น! Process ยังทำงานอยู่!

# 5. เช็ค CPU/GPU
nvidia-smi
# ✅ ยังเห็น python ใช้ GPU!
```

**Test 2: Notebook Cell (หาย)**

```python
# 1. ใน Notebook cell รัน:
import time
import os
print(f"PID: {os.getpid()}")  # จด PID

for i in range(600):  # 10 นาที
    print(f"Running {i}...")
    time.sleep(1)
```

```bash
# 2. จด PID (เช่น 67890)

# 3. เปิด Terminal แยก เช็ค process
ps aux | grep 67890
# Output: root 67890 python (kernel)

# 4. ปิดบราวเซอร์ทิ้งไว้ 2 นาที

# 5. เปิด Terminal ใหม่ เช็คอีกรอบ
ps aux | grep 67890
# ❌ ไม่เห็น! Process หายไปแล้ว!

# 6. เปิดบราวเซอร์กลับมา
# ❌ Kernel disconnected!
# ❌ Cell หยุดทำงาน!
```

---

#### 📊 เปรียบเทียบโดยตรง

| Aspect | Terminal | Notebook Cell |
|--------|----------|---------------|
| **Process Type** | Independent (standalone) | Kernel-managed (dependent) |
| **Parent Process** | `bash` | `jupyter-kernel` |
| **ต้องการ Browser** | ❌ ไม่ต้องการ | ✅ ต้องการ (WebSocket) |
| **Heartbeat** | ❌ ไม่มี | ✅ มี (ส่งทุก 30s) |
| **Connection** | One-way (แค่ดู) | Two-way (ต้องคุยกัน) |
| **ปิด browser** | ✅ Process รันต่อ | ❌ Kernel ตาย |
| **Network ขาด** | ✅ Process รันต่อ | ❌ Timeout |
| **Idle timeout** | ✅ ไม่มี | ❌ มี (10-15 min) |
| **Kill ยังไง** | `kill -9 PID` | ปิด browser = ตายเอง |

---

#### 💡 อธิบายแบบ Analogy

**Terminal = ส่งของ Drop & Go 📦**
```
1. คุณส่งพัสดุที่ไปรษณีย์
2. จ่ายเงินเรียบร้อย
3. พนักงานรับไปจัดส่งเอง
4. คุณไปไหนก็ได้ (ปิดเบราว์เซอร์)
5. ของยังส่งต่อปกติ ✅
6. ไม่ต้องติดตามอะไร
```

**Notebook = แท็กซี่ต้องรอ 🚕**
```
1. คุณเรียกแท็กซี่มารอ
2. แท็กซี่ติดเครื่องยนต์รออยู่
3. ต้อง "ส่งสัญญาณ" ว่ายังอยู่ (heartbeat)
4. คนขับถามทุก 30 วิ: "คุณยังอยู่ไหม?"
5. ❌ คุณออกจากรถไป (ปิดเบราว์เซอร์)
6. ❌ คนขับคิดว่าคุณไม่กลับ → ขับไป!
7. ❌ คุณนอนหลับไม่ตอบ → คนขับคิดว่าไม่มีคน → ลงจากรถ
```

---

#### 🌍 Platform อื่นๆ ทำได้มั้ย?

**✅ ที่ทำได้เหมือน Paperspace (รัน Terminal ปิด browser ได้):**

**Cloud GPU Platforms:**
- **Paperspace Gradient** ✅ (ที่เราใช้อยู่)
- **AWS EC2** ✅ (SSH access)
- **Google Cloud Compute Engine** ✅ (SSH access)
- **Azure Virtual Machines** ✅ (SSH access)
- **Lambda Labs** ✅ (SSH access)
- **RunPod** ✅ (SSH + web terminal)
- **Vast.ai** ✅ (SSH access)

**VPS/Dedicated Server:**
- **DigitalOcean** ✅
- **Linode** ✅
- **Vultr** ✅
- **OVH** ✅
- **Server ตัวเองที่บ้าน** ✅ (SSH)

**Local:**
- **Mac Terminal** ✅
- **Linux Terminal** ✅
- **Windows WSL** ✅
- **Windows PowerShell** ✅

**หลักการ:** ถ้ามี **Terminal/SSH access** → ปิด browser ได้

---

**❌ ที่ทำไม่ได้ (หรือทำได้แต่ยาก):**

**Google Colab:**
```
❌ ปิด browser → runtime disconnect
❌ Idle 90 นาที → runtime stop
❌ ไม่มี SSH access โดยตรง

⚠️ แก้ได้แต่ยาก:
- ใช้ ngrok/cloudflare tunnel เชื่อม SSH (hack)
- ใช้ JavaScript คอยกด cell อัตโนมัติ (hack)
- ไม่แนะนำสำหรับงานยาว
```

**Kaggle Notebooks:**
```
❌ ปิด browser → runtime disconnect
❌ Idle timeout
❌ ไม่มี SSH access
```

**Jupyter Notebook (local):**
```
⚠️ ขึ้นอยู่กับวิธีรัน:
- รัน cell → ❌ ปิด browser = หยุด
- รัน %%bash cell → ✅ อาจรันต่อได้
- Terminal in JupyterLab → ✅ ปิดได้ (เหมือน Paperspace)
```

---

#### 🎯 สรุป Platform Comparison

| Platform | Terminal/SSH | ปิด Browser ได้ | Idle Timeout | GPU ฟรี |
|----------|--------------|-----------------|--------------|---------|
| **Paperspace** | ✅ มี | ✅ ได้ | ❌ ไม่มี | ✅ มี (Growth) |
| **AWS/GCP/Azure** | ✅ มี (SSH) | ✅ ได้ | ❌ ไม่มี | ❌ เสียเงิน |
| **RunPod/Vast** | ✅ มี (SSH) | ✅ ได้ | ❌ ไม่มี | ❌ เสียเงิน |
| **Local Server** | ✅ มี | ✅ ได้ | ❌ ไม่มี | ❌ ต้องมี GPU |
| **Google Colab** | ❌ ไม่มี | ❌ ไม่ได้ | ✅ มี (90 min) | ✅ มี (จำกัด) |
| **Kaggle** | ❌ ไม่มี | ❌ ไม่ได้ | ✅ มี | ✅ มี (จำกัด) |

**💡 กฎง่ายๆ:**
```
มี SSH/Terminal access → ปิด browser ได้ ✅
ไม่มี (Colab, Kaggle) → ปิดไม่ได้ ❌
```

**Paperspace ดีตรงที่:**
- ✅ มี Terminal access
- ✅ ไม่มี Idle timeout
- ✅ GPU ฟรี (Growth Plan)
- ✅ ปิด browser ได้
- ✅ รันงานยาวได้

---

#### 💡 Analogy (เปรียบเทียบ):

**Terminal = ส่งพัสดุ (Drop & Go)**
```
คุณส่งพัสดุ → ไปรษณีย์รับไว้ → คุณกลับบ้าน
→ พัสดุเดินทางต่อเอง (ไม่ต้องติดตาม)
→ ถึงปลายทางแน่นอน ✓
```

**Notebook = แท็กซี่ (Stay Connected)**
```
คุณเรียกแท็กซี่ → ขึ้นรถ → ระหว่างทาง...
→ คุณลงรถกลางทาง → แท็กซี่หยุด ✗
→ คุณนอนหลับ → คนขับคิดว่าไม่มีคน → หยุดรถ ✗
→ ต้องนั่งดูแลตลอด (มี activity) → ถึงปลายทาง ✓
```

---

#### 🔧 วิธีแก้ Notebook Timeout (ถ้าจะใช้):

**1. เปิด browser ค้าง + กดอะไรบางอย่างเป็นระยะ**
```python
# รัน cell นี้
!python whisper_transcribe.py video.mp4

# แล้วกด:
# - Space bar ทุก 30 วินาที
# - หรือ scroll หน้าจอ
# - หรือ click cell

→ Jupyter รู้ว่ามี activity → ไม่ timeout
```

**2. ใช้ nohup (แต่ยากกว่า Terminal)**
```python
%%bash
nohup python whisper_transcribe.py video.mp4 &
```

**3. หรือใช้ Terminal แทน (ง่ายที่สุด!)**
```bash
python whisper_transcribe.py video.mp4
→ ปล่อยไว้ได้เลย ✓
```

---

### 🎯 ทำไมคู่มือนี้ใช้ Terminal?

**1. เหมาะกับ Long-running Tasks**
```
Whisper ถอดเสียง 1 ชม. → ใช้เวลา 3-6 นาที
→ Terminal: ทำงานได้ต่อเนื่อง ✓
→ Notebook: อาจ timeout (ถ้า idle) ✗
```

**2. Production-ready Script**
```
Terminal: python script.py (professional)
Notebook: แบบเรียนรู้/ทดลอง (exploration)
```

**3. Copy-Paste ง่าย**
```
Terminal: copy คำสั่ง → paste → Enter
Notebook: ต้องสร้าง cell ก่อน
```

**4. ไม่กังวลเรื่อง Timeout**
```
Terminal: รัน background ได้ (nohup, screen)
Notebook: ต้องเปิดค้าง (ไม่งั้น disconnect)
```

---

### 💡 ถ้าอยากใช้ Notebook แทน Terminal ได้มั้ย?

**✅ ได้! แต่ต้องแก้เล็กน้อย:**

**Terminal command:**
```bash
python /notebooks/thai-whisper/scripts/whisper_transcribe.py video.mp4
```

**Notebook cell (เทียบเท่า):**
```python
!python /notebooks/thai-whisper/scripts/whisper_transcribe.py video.mp4
```

**หรือ:**
```python
%%bash
python /notebooks/thai-whisper/scripts/whisper_transcribe.py video.mp4
```

**⚠️ หมายเหตุ:**
- เพิ่ม `!` หรือ `%%bash` ข้างหน้า
- ประสิทธิภาพเหมือนกัน
- แต่อาจ timeout ถ้าไฟล์ใหญ่

---

### 📋 สรุป - ตอบคำถาม

**Q1: ทำใน Terminal หมดเลยเหรอ?**
- A: ใช่! ส่วนใหญ่ใช้ Terminal
- แต่ยังใช้ Jupyter UI (file browser) สร้าง/download ไฟล์

**Q2: ไม่ต้องใช้ Notebook (.ipynb) เลย?**
- A: ไม่ต้อง! คู่มือนี้ไม่ใช้ Notebook cells
- ใช้แค่ Terminal + Jupyter UI (file manager)

**Q3: ประสิทธิภาพต่างกันมั้ย?**
- A: **ไม่ต่างเลย!** ทั้งสองใช้ GPU เดียวกัน
- เร็วเท่ากัน, ใช้ RAM เท่ากัน

**Q4: ทำไมไม่ใช้ Notebook?**
- A: Terminal เหมาะกับ long tasks + production scripts
- Notebook เหมาะกับ exploration/learning

**Q5: ถ้าอยากใช้ Notebook ได้มั้ย?**
- A: ได้! เพิ่ม `!` ข้างหน้าคำสั่ง
- แต่ต้องระวังเรื่อง timeout

---

## 🎯 ข้อกำหนดเบื้องต้น

### ที่ต้องมี:

- ✅ Paperspace account (สมัครที่ paperspace.com)
- ✅ Growth Plan ($8/month) - subscribe แล้ว
- ✅ Notebook เปิดอยู่ (RTX A4000)
- ✅ วิดีโอภาษาไทยที่จะถอดเสียง

### ที่ไม่ต้องมี:

- ❌ ไม่ต้องรู้ Terminal commands มาก (copy-paste ได้)
- ❌ ไม่ต้องรู้ Python (มี script สำเร็จรูป)
- ❌ ไม่ต้องรู้เรื่อง /storage (ใช้ default location)

---

## PART 1: สร้างโครงสร้างโฟลเดอร์

**⚠️ สำคัญ: ทำใน Paperspace Notebook (ไม่ใช่เครื่องของคุณ!)**

```
📍 ทำที่ไหน: Paperspace Jupyter Lab (ใน browser)
❌ ไม่ใช่: เครื่องคอมพิวเตอร์ของคุณ
❌ ไม่ใช่: Local terminal

💡 โฟลเดอร์ที่สร้างจะอยู่ที่:
/notebooks/thai-whisper/  (ใน Paperspace cloud)
```

---

### ✅ STEP 1: เปิด Jupyter Lab

**เมื่อ Paperspace Notebook พร้อม:**

1. คลิกเข้า Notebook → เปิด Jupyter Lab
2. รอจนโหลดเสร็จ (เห็นหน้าจอ Jupyter Lab)
3. มองหา **File Browser** (ซ้ายมือ - icon โฟลเดอร์ 📁)

---

### ✅ STEP 2: สร้างโฟลเดอร์หลัก `thai-whisper`

**ใน File Browser:**

```
1. คลิกขวาในพื้นที่ว่าง
2. เลือก "New Folder"
3. ตั้งชื่อ: thai-whisper
4. กด Enter
```

✅ **ได้โฟลเดอร์ `thai-whisper` แล้ว**

---

### ✅ STEP 3: เข้าโฟลเดอร์ `thai-whisper`

```
1. Double-click โฟลเดอร์ thai-whisper
2. เข้าไปในโฟลเดอร์ (ควรเห็น path bar เปลี่ยนเป็น /thai-whisper หรือคล้ายๆ)
```

---

### ✅ STEP 4: สร้างโฟลเดอร์ย่อย (3 โฟลเดอร์)

**ในโฟลเดอร์ `thai-whisper` ที่เพิ่งเข้ามา:**

#### 4.1 สร้างโฟลเดอร์ `videos`

```
1. คลิกขวาในพื้นที่ว่าง
2. New Folder
3. ตั้งชื่อ: videos
4. กด Enter
```

#### 4.2 สร้างโฟลเดอร์ `transcripts`

```
1. คลิกขวาในพื้นที่ว่าง
2. New Folder
3. ตั้งชื่อ: transcripts
4. กด Enter
```

#### 4.3 สร้างโฟลเดอร์ `scripts`

```
1. คลิกขวาในพื้นที่ว่าง
2. New Folder
3. ตั้งชื่อ: scripts
4. กด Enter
```

---

### ✅ STEP 5: เช็คโครงสร้าง

**ตอนนี้ File Browser ควรเห็น:**

```
thai-whisper/
├── videos/
├── transcripts/
└── scripts/
```

**ถ้าเห็นครบ 3 โฟลเดอร์ → ✅ เสร็จ Part 1!**

---

## PART 2: ติดตั้ง Whisper

### ✅ STEP 6: เปิด Terminal

**ใน Jupyter Lab:**

```
1. ด้านล่าง File Browser → มีปุ่ม "+" (New Launcher)
2. คลิกปุ่ม "+"
3. ใน Launcher → มองหา "Other" section
4. คลิก "Terminal"
5. Terminal เปิดขึ้นมา (หน้าจอดำๆ มี prompt)
```

---

### ✅ STEP 7: เช็ค GPU 🔥 **สำคัญมาก!**

**⚠️ ขั้นตอนนี้สำคัญที่สุด! ถ้า GPU ไม่ทำงาน → จะ "Killed" ตอนถอดเสียง!**

```
🚨 ทำไมต้องเช็ค GPU?
- ถ้าไม่มี GPU → Script จะใช้ CPU
- CPU ไม่ได้รับ model large-v3 (2.88 GB)
- ผลลัพธ์: "Killed" (Out of Memory)
- ดู Troubleshooting → ปัญหา 1.6 สำหรับรายละเอียด

✅ มี GPU → ถอดเสียงได้ (เร็ว 10-20 เท่า)
❌ ไม่มี GPU → Killed (ไม่สามารถทำงานได้)
```

---

**ใน Terminal - Copy คำสั่งนี้แล้ว Paste:**

```bash
nvidia-smi
```

**กด Enter**

**ควรเห็น:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI xxx.xx       Driver Version: xxx.xx       CUDA Version: xx.x    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        ...          | ...                  | ...                  |
|   0  NVIDIA RTX A4000   ...   | ...                  | ...                  |
+-------------------------------+----------------------+----------------------+
```

**ถ้าเห็นข้อมูล GPU → ✅ พร้อมใช้งาน → ดำเนินการต่อได้**

**ถ้าไม่เห็น → ❌ STOP! ต้องแก้ก่อน:**
1. ปิด Notebook
2. Settings → Instance Type → เลือก "RTX A4000" (GPU)
3. Start Notebook ใหม่
4. รัน nvidia-smi อีกครั้ง → ต้องเห็น GPU

**💡 Double-check: เช็ค PyTorch เห็น GPU มั้ย**

```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

**ควรเห็น:**
```
CUDA available: True
```

**ถ้าเห็น False:**
```bash
# ติดตั้ง PyTorch แบบ CUDA
pip uninstall torch -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

### ✅ STEP 8: ติดตั้ง Whisper

**⚠️ สำคัญ: ติดตั้งที่ไหน? (ระดับไหน?)**

```
📍 ติดตั้งที่: Paperspace Notebook Terminal
❌ ไม่ใช่: เครื่องของคุณ (Local computer)
❌ ไม่ใช่: Virtual environment แยก

🔍 ติดตั้งที่ Path ไหน?
pip install = ติดตั้งที่ระดับ Python system packages
Path จริง: /usr/local/lib/python3.x/site-packages/

❌ ไม่ใช่ใน: /notebooks/thai-whisper/
❌ ไม่ใช่ใน: /notebooks/thai-whisper/videos/
❌ ไม่ใช่ใน: /notebooks/thai-whisper/scripts/

💡 ความแตกต่าง:
┌─────────────────────────────────────────────────┐
│ pip install openai-whisper                      │
│ → ติดตั้ง Python package (ระดับ system)         │
│ → ใช้ได้จากทุก directory                        │
│ → ไม่เกี่ยวกับโฟลเดอร์ที่คุณ cd อยู่            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ mkdir /notebooks/thai-whisper/                  │
│ → สร้างโฟลเดอร์ (ระดับไฟล์)                     │
│ → เฉพาะโฟลเดอร์นั้นๆ                            │
└─────────────────────────────────────────────────┘

💡 สรุป:
- Whisper ติดตั้งทั้ง Paperspace (ทุก directory ใช้ได้)
- ไม่ว่าจะ cd ไปที่ /notebooks/ หรือ /root/
  ก็ import whisper ได้เหมือนกัน
- ต้องติดตั้งใหม่ทุกครั้งที่เปิด notebook ใหม่
  (Paperspace ไม่เก็บ packages ไว้ถาวร)
```

**🎯 คำถามที่ถามบ่อย: ต้อง cd ไปที่โฟลเดอร์ไหนก่อน pip install มั้ย?**

```
❓ คำถาม:
ต้องรัน pip install ที่ path ไหน?
- root@nijgyuae9m:/notebooks# หรือ
- root@nijgyuae9m:/notebooks/thai-whisper# หรือ
- root@nijgyuae9m:/notebooks/thai-whisper/videos#

✅ คำตอบ: ที่ไหนก็ได้! ไม่สำคัญ!

🔍 อธิบาย:
pip install ติดตั้งแบบ system-wide (ทั้งระบบ)
→ ไม่ว่าคุณจะ cd อยู่ที่โฟลเดอร์ไหน
→ ติดตั้งที่เดียวกัน: /usr/local/lib/python3.x/site-packages/

📋 ตัวอย่าง (ทั้ง 3 แบบเหมือนกันหมด):

# แบบ 1: รันจาก /notebooks
root@nijgyuae9m:/notebooks# pip install openai-whisper
→ ✅ ติดตั้งที่ /usr/local/lib/.../site-packages/

# แบบ 2: รันจาก /notebooks/thai-whisper
root@nijgyuae9m:/notebooks/thai-whisper# pip install openai-whisper
→ ✅ ติดตั้งที่ /usr/local/lib/.../site-packages/ (เหมือนกัน!)

# แบบ 3: รันจาก /notebooks/thai-whisper/videos
root@nijgyuae9m:/notebooks/thai-whisper/videos# pip install openai-whisper
→ ✅ ติดตั้งที่ /usr/local/lib/.../site-packages/ (เหมือนกันอีก!)

💡 สรุป:
- Terminal prompt (root@...:/path/to/dir#) แสดง current directory
- แต่ pip install ไม่สนใจ current directory
- ติดตั้ง system-wide เสมอ
- ใช้คำสั่ง pwd เช็คว่าอยู่โฟลเดอร์ไหน (ถ้าอยากรู้)

⚠️ แต่ระวัง: การรัน script ต่างหาก!
python script.py → ต้องระบุ path ถูกต้อง
cd /path/to/script/ → แล้วค่อยรัน python script.py
```

---

**ใน Paperspace Terminal - Copy คำสั่งนี้:**

```bash
pip install -U openai-whisper ffmpeg-python
```

**กด Enter → รอติดตั้ง (30-60 วินาที)**

**ควรเห็นท้ายสุด:**
```
Successfully installed openai-whisper-...
```

✅ **ติดตั้งสำเร็จ! (ใน Paperspace Notebook นี้)**

---

### ✅ STEP 9: ทดสอบ Whisper

**ใน Terminal - Copy คำสั่งนี้:**

```bash
python -c "import whisper; print('✅ Whisper installed:', whisper.__version__)"
```

**กด Enter**

**ควรเห็น:**
```
✅ Whisper installed: 20231117
```

✅ **ทำงานได้!**

---

### ✅ STEP 10: Download Model (ครั้งแรก - ใช้เวลา 3-5 นาที)

**ใน Terminal - Copy คำสั่งทั้งหมดนี้:**

```bash
python << 'EOF'
import whisper
print("⏳ Downloading Whisper large-v3 model...")
print("   (This is one-time download, ~3 GB)")
model = whisper.load_model("large-v3")
print("✅ Model downloaded and cached!")
print("   Next time will be instant!")
EOF
```

**กด Enter → รอ download (3-5 นาที)**

**Progress:**
```
⏳ Downloading Whisper large-v3 model...
   (This is one-time download, ~3 GB)
100%|████████████████████| 2.87G/2.87G [03:24<00:00, 45.2MiB/s]
✅ Model downloaded and cached!
   Next time will be instant!
```

✅ **Download เสร็จ! (ครั้งต่อไปไม่ต้อง download ซ้ำ)**

---

## PART 3: สร้าง Python Script

### ✅ STEP 11: สร้างไฟล์ Script

**ใน Jupyter Lab File Browser:**

```
1. Navigate ไปที่โฟลเดอร์ thai-whisper/scripts/
   (Double-click thai-whisper → Double-click scripts)

2. คลิกขวาในพื้นที่ว่าง

3. เลือก "New File"

4. ตั้งชื่อ: whisper_transcribe.py

5. กด Enter
```

✅ **ได้ไฟล์ `whisper_transcribe.py` แล้ว**

---

### ✅ STEP 12: เปิดไฟล์และวาง Code

**ใน File Browser:**

```
1. Double-click ไฟล์ whisper_transcribe.py
   → เปิด Text Editor

2. Copy code ทั้งหมดด้านล่างนี้
   → Paste ลงในไฟล์

3. กด Ctrl+S (หรือ Cmd+S บน Mac) = Save
```

**Code ที่ต้อง Copy:**

```python
#!/usr/bin/env python3
"""
Paperspace Whisper Transcriber - Thai Optimized (Simple Version)
"""

import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

try:
    import whisper
    import torch
except ImportError as e:
    logger.error(f"Missing dependency: {e}")
    logger.error("Install: pip install openai-whisper torch")
    sys.exit(1)


def transcribe_video(video_path, output_path=None):
    """
    Transcribe Thai video with Whisper

    Args:
        video_path: Path to video file
        output_path: Output JSON path (optional)

    Returns:
        Path to output JSON file
    """
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    # Auto-detect device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    logger.info("="*70)
    logger.info("PAPERSPACE WHISPER TRANSCRIBER")
    logger.info("="*70)
    logger.info(f"Video: {video_path.name}")
    logger.info(f"Size: {video_path.stat().st_size / (1024*1024):.1f} MB")
    logger.info(f"Device: {device}")

    if device == "cuda":
        gpu_name = torch.cuda.get_device_name(0)
        logger.info(f"GPU: {gpu_name}")

    # Default output path
    if output_path is None:
        output_path = video_path.parent.parent / "transcripts" / f"{video_path.stem}_transcript.json"
    else:
        output_path = Path(output_path)

    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load model
    logger.info("\n⏳ Loading Whisper model...")
    start_load = time.time()
    model = whisper.load_model("large-v3", device=device)
    logger.info(f"✓ Model loaded in {time.time() - start_load:.1f}s")

    # Thai-optimized settings
    settings = {
        "language": "th",
        "task": "transcribe",
        "word_timestamps": True,
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8),
        "beam_size": 5,
        "best_of": 5,
        "compression_ratio_threshold": 2.4,
        "logprob_threshold": -1.0,
        "no_speech_threshold": 0.6,
        "condition_on_previous_text": True,
        "initial_prompt": "นี่คือการสอนเทรด Forex และการลงทุน ใช้ภาษาไทยธรรมดา"
    }

    # Transcribe
    logger.info("\n⏳ Starting transcription...")
    logger.info("   (This may take several minutes...)\n")

    start_time = time.time()

    result = model.transcribe(
        str(video_path),
        verbose=True,  # Show progress
        **settings
    )

    transcription_time = time.time() - start_time

    # Calculate stats
    segments = result['segments']
    duration = segments[-1]['end'] if segments else 0
    speed = duration / transcription_time if transcription_time > 0 else 0
    word_count = sum(len(seg.get('text', '').split()) for seg in segments)

    logger.info(f"\n✅ Transcription complete!")
    logger.info(f"   Duration: {int(duration // 60)}:{int(duration % 60):02d}")
    logger.info(f"   Segments: {len(segments)}")
    logger.info(f"   Words: {word_count}")
    logger.info(f"   Processing time: {transcription_time:.1f}s")
    logger.info(f"   Speed: {speed:.1f}x realtime")

    # Save JSON
    output_data = {
        'video_name': video_path.name,
        'timestamp': datetime.now().isoformat(),
        'metadata': {
            'language': 'th',
            'model_name': 'large-v3',
            'device': device,
            'duration': duration,
            'word_count': word_count,
            'segment_count': len(segments),
            'transcription_time': transcription_time,
            'speed': speed
        },
        'text': result['text'],
        'segments': segments
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    file_size = output_path.stat().st_size / 1024

    logger.info(f"\n📁 Output saved:")
    logger.info(f"   File: {output_path.name}")
    logger.info(f"   Path: {output_path}")
    logger.info(f"   Size: {file_size:.1f} KB")
    logger.info("="*70)

    return output_path


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Paperspace Whisper Transcriber")
    parser.add_argument('input', type=str, help='Input video file')
    parser.add_argument('-o', '--output', type=str, help='Output JSON file (optional)')

    args = parser.parse_args()

    try:
        output_file = transcribe_video(args.input, args.output)
        print(f"\n✅ SUCCESS! Transcript saved to: {output_file}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

**กด Ctrl+S (Save) อีกครั้ง**

✅ **Script พร้อมใช้งาน!**

---

## PART 4: Upload วิดีโอ

### ✅ STEP 13: ไปที่โฟลเดอร์ videos

**ใน File Browser:**

```
1. ถ้าอยู่ใน scripts/ → คลิกย้อนกลับ (ปุ่ม ←)
   หรือ คลิก "thai-whisper" ใน breadcrumb

2. Double-click โฟลเดอร์ "videos"

3. ควรอยู่ในโฟลเดอร์ videos/ (เปล่าๆ ยังไม่มีไฟล์)
```

---

### ✅ STEP 14: Upload วิดีโอ

**เลือกวิธีที่เหมาะกับคุณ:**

---

#### 🎯 วิธี A: Upload จาก Google Drive (แนะนำ - เร็วที่สุด!)

**เมื่อไฟล์อยู่ใน Google Drive แล้ว:**

##### 14A.1 ติดตั้ง gdown (ครั้งแรกครั้งเดียว)

**ใน Terminal:**
```bash
pip install gdown
```

##### 14A.2 เตรียม Google Drive Link

**บนเครื่องคุณ:**
```
1. เปิดไฟล์วิดีโอใน Google Drive
2. คลิกขวา → Share → Change to "Anyone with the link"
3. Copy link (จะได้แบบนี้):
   https://drive.google.com/file/d/1ZvlVweCL.../view?usp=drive_link
4. Copy เฉพาะ File ID (ตรงกลาง):
   1ZvlVweCL_KqGQWiAOw9-VSjZbol9n-tw
```

##### 14A.3 Download จาก Google Drive

**ใน Terminal:**

```bash
# เข้าโฟลเดอร์ videos
cd /notebooks/thai-whisper/videos/

# Download ด้วย gdown (ใช้ --fuzzy เพื่อ bypass restrictions)
gdown --fuzzy "https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=drive_link"

# หรือใช้ File ID อย่างเดียว
gdown YOUR_FILE_ID
```

**ตัวอย่างจริง:**
```bash
gdown --fuzzy "https://drive.google.com/file/d/1ZvlVweCL_KqGQWiAOw9-VSjZbol9n-tw/view?usp=drive_link"
```

**Progress:**
```
Downloading...
From: https://drive.google.com/uc?id=1ZvlVweCL...
To: /notebooks/thai-whisper/videos/video_name.mp4
100%|████████████████████| 1.5G/1.5G [02:30<00:00, 10.2MB/s]
```

✅ **ใช้เวลา 2-4 นาที สำหรับไฟล์ 1.5 GB!**

---

#### 📤 วิธี B: Upload จากเครื่อง (ผ่าน Jupyter UI)

**เมื่อไฟล์อยู่ในเครื่องคุณ:**

**ใน Jupyter File Browser:**

```
1. ไปที่โฟลเดอร์ videos/

2. มองหาปุ่ม Upload (ลูกศรชี้ขึ้น ↑)
   → ด้านบน File Browser

3. คลิก Upload Files

4. เลือกไฟล์วิดีโอจากเครื่อง

5. รอ upload เสร็จ...
   (ขึ้นกับขนาดไฟล์ + internet)

   Progress bar จะแสดง:
   [████████████░░░] 75%

6. เมื่อเสร็จ → เห็นไฟล์วิดีโอในโฟลเดอร์
```

---

#### 🌐 วิธี C: Download จาก URL ตรงๆ

**เมื่อมี direct link:**

**ใน Terminal:**
```bash
cd /notebooks/thai-whisper/videos/

# ใช้ wget
wget https://your-server.com/video.mp4

# หรือใช้ curl
curl -o video.mp4 https://your-server.com/video.mp4
```

---

#### 📁 วิธี D: จาก Dropbox/OneDrive

**Dropbox:**
```bash
# แก้ link: เปลี่ยน dl=0 → dl=1
wget "https://www.dropbox.com/s/xxx/video.mp4?dl=1" -O video.mp4
```

**OneDrive:**
```bash
# ใช้ direct download link generator
# เช่น: https://onedrive.live.com/download?...
wget "ONEDRIVE_DIRECT_LINK" -O video.mp4
```

---

#### ⚡ วิธี E: rclone (สำหรับไฟล์ใหญ่ หรือใช้บ่อย)

**ข้อดี:**
- ✅ Resume ได้ถ้าขาด (ไฟล์ใหญ่มาก)
- ✅ Setup ครั้งเดียว ใช้ต่อได้เรื่อยๆ
- ✅ รองรับหลาย cloud: Google Drive, Dropbox, OneDrive, S3, etc.
- ✅ Progress bar ชัดเจน

**ข้อเสีย:**
- ⚠️ Setup ครั้งแรกใช้เวลา 5-7 นาที (ต้อง auth)

---

##### E.1 ติดตั้ง rclone (ครั้งแรกครั้งเดียว)

**ใน Terminal:**
```bash
curl https://rclone.org/install.sh | sudo bash
```

**ควรเห็น:**
```
rclone v1.xx.x has successfully installed.
```

---

##### E.2 Config rclone กับ Google Drive

**ใน Terminal:**
```bash
rclone config
```

**ตอบตามนี้:**
```
Current remotes:

n) New remote
s) Set configuration password
q) Quit config
n/s/q> n         ← พิมพ์ n

name> gdrive     ← ตั้งชื่อ (ใช้ชื่ออะไรก็ได้)

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
...
15 / Google Drive
   \ (drive)
...
Storage> drive   ← พิมพ์ drive (หรือเลข 15)

Option client_id.
Google Application Client Id
Leave blank normally.
client_id> [กด Enter]

Option client_secret.
client_secret> [กด Enter]

Option scope.
1 / Full access all files
   \ (drive)
2 / Read-only access to file metadata
   \ (drive.readonly)
...
scope> 1         ← พิมพ์ 1 (Full access)

Option root_folder_id.
root_folder_id> [กด Enter]

Option service_account_file.
service_account_file> [กด Enter]

Edit advanced config?
y) Yes
n) No (default)
y/n> n           ← พิมพ์ n

Use auto config?
y) Yes (default)
n) No
y/n> n           ← สำคัญ! พิมพ์ n (เพราะ Paperspace ไม่มี browser)

Option config_token.
For this to work, you will need rclone available on a machine that has
a web browser available.
...
Execute the following on the machine with the web browser:
    rclone authorize "drive"

Then paste the result below:
config_token> [จะได้ link ออกมา - อ่านขั้นตอนถัดไป]
```

---

##### E.3 Auth บนเครื่องคุณ (ที่มี Browser)

**ใน Terminal บนเครื่องคุณ** (ไม่ใช่ Paperspace):

```bash
# ถ้าไม่มี rclone บนเครื่อง ติดตั้งก่อน:
# Mac: brew install rclone
# Linux: curl https://rclone.org/install.sh | sudo bash
# Windows: ดาวน์โหลดจาก rclone.org

# รันคำสั่งนี้:
rclone authorize "drive"
```

**จะเปิด Browser:**
1. Login Google account ที่มีไฟล์
2. คลิก "Allow"
3. เสร็จแล้วจะได้ code ยาวๆ ใน Terminal

**Copy code ทั้งหมด** (ตัวอย่าง):
```json
{"access_token":"ya29.xxx...","token_type":"Bearer",...}
```

---

##### E.4 Paste Token กลับไป Paperspace

**กลับไปที่ Paperspace Terminal:**
```
config_token> [Paste code ที่ได้จาก E.3]

Configure this as a team drive?
y) Yes
n) No (default)
y/n> n           ← พิมพ์ n

Configuration complete.
Options:
- type: drive
- scope: drive
Keep this "gdrive" remote?
y) Yes (default)
e) Edit
d) Delete
y/e/d> y         ← พิมพ์ y

Current remotes:
Name                 Type
====                 ====
gdrive               drive

e) Edit existing remote
n) New remote
d) Delete remote
q) Quit config
e/n/d/q> q       ← พิมพ์ q (Quit)
```

✅ **Setup เสร็จ! ครั้งต่อไปไม่ต้อง config ซ้ำ**

---

##### E.5 List ไฟล์ใน Google Drive (เช็คว่าเชื่อมต่อสำเร็จ)

**ใน Terminal:**
```bash
# ดูไฟล์ทั้งหมด
rclone ls gdrive:

# หรือค้นหาไฟล์เฉพาะ
rclone ls gdrive: | grep mp4
```

**ควรเห็น:**
```
1524288000 video-ep-02.mp4
 987654321 another-video.mp4
```

---

##### E.6 Copy ไฟล์จาก Google Drive → Paperspace

**ใน Terminal:**

```bash
# รูปแบบ:
# rclone copy gdrive:/path/to/file.mp4 /notebooks/thai-whisper/videos/ --progress

# ตัวอย่าง 1: Copy ไฟล์ที่อยู่ root ของ Drive
rclone copy gdrive:/video.mp4 /notebooks/thai-whisper/videos/ --progress

# ตัวอย่าง 2: Copy ไฟล์ที่อยู่ในโฟลเดอร์
rclone copy "gdrive:/My Videos/ep-02.mp4" /notebooks/thai-whisper/videos/ --progress

# ตัวอย่าง 3: Copy ทั้งโฟลเดอร์
rclone copy "gdrive:/My Videos/" /notebooks/thai-whisper/videos/ --progress

# ตัวอย่าง 4: Copy หลายไฟล์ (wildcard)
rclone copy gdrive:/ /notebooks/thai-whisper/videos/ --include "*.mp4" --progress
```

**Progress:**
```
Transferred:        1.452 GiB / 1.500 GiB, 97%, 12.5 MiB/s, ETA 5s
Transferred:            1 / 1, 100%
Elapsed time:       1m58.2s
```

✅ **เสร็จ! เร็วและมี progress bar**

---

##### E.7 ใช้ครั้งต่อไป (ง่ายมาก!)

**ครั้งต่อไปไม่ต้อง setup - แค่ copy เลย:**

```bash
# List ไฟล์
rclone ls gdrive: | grep mp4

# Copy
rclone copy gdrive:/your-video.mp4 /notebooks/thai-whisper/videos/ --progress
```

---

##### 💡 rclone Tips

**Resume การ download:**
```bash
# ถ้าขาดตอน download
# แค่รันคำสั่งเดิมอีกครั้ง → มัน resume เองอัตโนมัติ!
rclone copy gdrive:/big-video.mp4 /notebooks/thai-whisper/videos/ --progress
```

**ใช้กับ cloud อื่นๆ:**
```bash
# Dropbox
rclone config  # เลือก dropbox แทน drive
rclone copy dropbox:/video.mp4 /notebooks/thai-whisper/videos/

# OneDrive
rclone config  # เลือก onedrive
rclone copy onedrive:/video.mp4 /notebooks/thai-whisper/videos/
```

**ตัวเลือกเพิ่มเติม:**
```bash
# แสดง progress + bandwidth
rclone copy gdrive:/video.mp4 /notebooks/thai-whisper/videos/ \
  --progress \
  --stats 1s

# จำกัด bandwidth (ถ้า internet ช้า)
rclone copy gdrive:/video.mp4 /notebooks/thai-whisper/videos/ \
  --progress \
  --bwlimit 5M  # จำกัด 5 MB/s
```

---

### ✅ เช็คว่าได้ไฟล์แล้ว

**ใน Terminal:**
```bash
ls -lh /notebooks/thai-whisper/videos/
```

**ควรเห็น:**
```
-rw-r--r-- 1 root root 1.5G Oct  7 10:30 video.mp4
```

✅ **มีไฟล์แล้ว - พร้อมถอดเสียง!**

---

### ⏱️ เปรียบเทียบเวลา Upload

| วิธี | ไฟล์ 1.5 GB | ความเร็ว | ความง่าย | Resume | เหมาะกับ |
|------|------------|---------|---------|--------|----------|
| **Google Drive (gdown)** | 2-4 นาที | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ใช้ครั้งเดียว |
| **rclone** | 2-4 นาที | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ไฟล์ใหญ่/ใช้บ่อย |
| **Jupyter UI** | 15-30 นาที | ⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | มือใหม่ |
| **wget/curl** | 3-5 นาที | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | มี direct URL |
| **Dropbox** | 3-5 นาที | ⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | ใช้ Dropbox อยู่แล้ว |

**🎯 แนะนำ:**
- **ครั้งแรก/ใช้นานๆครั้ง**: gdown (ง่าย + เร็ว)
- **ใช้บ่อย/ไฟล์ใหญ่**: rclone (setup ครั้งเดียว + resume ได้)

---

## PART 5: ถอดเสียง

### ✅ STEP 15: หา Path ของวิดีโอ

**⚠️ สำคัญ: เรื่อง `~` (Home Directory) ใน Paperspace**

```
ใน Paperspace, ~ ชี้ไปที่ /root/ ไม่ใช่ /notebooks/
ดังนั้น: find ~ จะไม่เจอไฟล์ที่อยู่ใน /notebooks/

✅ ใช้ /notebooks/ แทน (absolute path)
❌ ห้ามใช้ ~/thai-whisper/
```

---

#### วิธีที่ 1: ใช้ find (ค้นหาทั้ง notebooks)

**ใน Terminal:**

```bash
# หาไฟล์วิดีโอใน /notebooks
find /notebooks -name "*.mp4" -type f 2>/dev/null
```

**กด Enter**

**ควรเห็น:**
```
/notebooks/thai-whisper/videos/ep-02(061024).mp4
```

---

#### วิธีที่ 2: ใช้ ls (ถ้ารู้ path อยู่แล้ว - เร็วกว่า)

**ใน Terminal:**

```bash
# ดูไฟล์ใน videos folder
ls -lh /notebooks/thai-whisper/videos/
```

**ควรเห็น:**
```
-rw-r--r-- 1 root root 1.5G Oct  7 10:30 ep-02(061024).mp4
```

---

**📝 จดไว้ → จะใช้ในขั้นตอนถัดไป**

**ตัวอย่าง path ที่ได้:**
```
/notebooks/thai-whisper/videos/ep-02(061024).mp4
```

---

### ✅ STEP 16: รัน Transcription

**ใน Terminal:**

**รูปแบบ:**
```bash
python /notebooks/thai-whisper/scripts/whisper_transcribe.py \
  [PATH_ของวิดีโอที่ได้จาก_STEP_15]
```

**ตัวอย่างจริง:**

```bash
# ใช้ absolute path /notebooks/ (แนะนำ - ใช้ได้เสมอ)
python /notebooks/thai-whisper/scripts/whisper_transcribe.py \
  /notebooks/thai-whisper/videos/ep-02(061024).mp4
```

**⚠️ หมายเหตุสำคัญ:**

1. **ต้องใช้ `/notebooks/` ไม่ใช่ `~/`**
   ```bash
   # ✅ ถูกต้อง
   /notebooks/thai-whisper/videos/video.mp4

   # ❌ ผิด (จะไม่เจอไฟล์)
   ~/thai-whisper/videos/video.mp4
   ```

2. **ชื่อไฟล์มีวงเล็บ/ช่องว่าง → ใส่ `" "` (double quotes)**
   ```bash
   # ถ้าชื่อไฟล์: ep-02(061024).mp4
   # ใส่ quotes:
   python /notebooks/thai-whisper/scripts/whisper_transcribe.py \
     "/notebooks/thai-whisper/videos/ep-02(061024).mp4"
   ```

3. **Absolute Path vs Relative Path - ต่างกันอย่างไร?**

   **✅ Absolute Path (แนะนำ - ปลอดภัยกว่า):**
   ```bash
   # เริ่มจาก / (root) → ใช้ได้เสมอ ไม่ว่าจะ cd อยู่ที่ไหน
   python /notebooks/thai-whisper/scripts/whisper_transcribe.py \
     /notebooks/thai-whisper/videos/ep-02061024.mp4
   ```

   **Relative Path (ใช้ ./ - ขึ้นกับ current directory):**
   ```bash
   # ใช้ ./ (current directory) → ต้อง cd ไปยัง /notebooks ก่อน!
   cd /notebooks
   python /notebooks/thai-whisper/scripts/whisper_transcribe.py \
     ./thai-whisper/videos/ep-02061024.mp4
   ```

   **🔍 อธิบาย:**

   | | Absolute Path | Relative Path |
   |---|---------------|---------------|
   | **รูปแบบ** | `/notebooks/...` | `./thai-whisper/...` |
   | **เริ่มจาก** | Root (/) | Current directory (pwd) |
   | **ใช้ได้เมื่อ** | ทุกที่ (ไม่ว่า cd ไหน) | pwd = /notebooks เท่านั้น |
   | **ความปลอดภัย** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

   **ตัวอย่างที่เห็นความแตกต่าง:**

   ```bash
   # กรณี 1: อยู่ที่ /notebooks
   root@xxx:/notebooks# pwd
   /notebooks

   root@xxx:/notebooks# python script.py ./thai-whisper/videos/video.mp4
   # ./thai-whisper = /notebooks/thai-whisper  ← ✅ ถูก!

   # กรณี 2: อยู่ที่ /root (ย้ายไปที่อื่น)
   root@xxx:/notebooks# cd /root
   root@xxx:/root# pwd
   /root

   root@xxx:/root# python script.py ./thai-whisper/videos/video.mp4
   # ./thai-whisper = /root/thai-whisper  ← ❌ ผิด! (ไม่มีโฟลเดอร์นี้)
   ```

   **💡 สรุป:**
   - **Absolute path** (`/notebooks/...`) = ปลอดภัย, ใช้ได้เสมอ
   - **Relative path** (`./...`) = สั้นกว่า แต่ต้องระวัง pwd
   - **`./`** = current directory (เท่ากับ `pwd`)

   **🎯 แนะนำ:**
   - มือใหม่ → ใช้ **absolute path** (`/notebooks/...`) เสมอ
   - มือเก่า → ใช้ relative path ได้ (ถ้า cd ถูก)

---

### 💡 วิธีป้องกัน Copy/Paste ผิด (แนะนำ!)

**ปัญหาที่พบบ่อย:**
```bash
# Copy ไม่ครบ → ขาด /notebooks
python /notebooks/thai-whisper/scripts/whisper_transcribe.py \
  /thai-whisper/videos/video.mp4  ← ❌ ผิด! ขาด /notebooks

# ผลลัพธ์:
❌ ERROR: Video not found: /thai-whisper/videos/video.mp4
```

---

**✅ วิธีที่ 1: ใช้ตัวแปร (ป้องกัน typo)**

```bash
# 1. เก็บ path ไว้ในตัวแปร
video_path="/notebooks/thai-whisper/videos/ep-02061024.mp4"

# 2. รันด้วยตัวแปร (แน่ใจว่าไม่มี typo)
python /notebooks/thai-whisper/scripts/whisper_transcribe.py "$video_path"
```

**ข้อดี:**
- Copy path ครั้งเดียว → ใช้หลายครั้ง
- ถ้า path ผิด → แก้ที่เดียว
- Tab completion ใช้ได้

---

**✅ วิธีที่ 2: หา Path อัตโนมัติ (สำหรับมือใหม่)**

```bash
# วิธีนี้หา path เองอัตโนมัติ → ไม่ต้อง copy/paste
video_path=$(find /notebooks -name "ep-02061024.mp4" -type f 2>/dev/null | head -1)
python /notebooks/thai-whisper/scripts/whisper_transcribe.py "$video_path"
```

**ข้อดี:**
- ไม่ต้อง copy path เอง
- แก้ชื่อไฟล์อย่างเดียว (ep-02061024.mp4)
- ไม่มีทาง typo

**ตัวอย่างสำหรับไฟล์มีวงเล็บ:**
```bash
# ไฟล์: ep-02(061024).mp4
video_path=$(find /notebooks -name "ep-02(061024).mp4" -type f 2>/dev/null | head -1)
python /notebooks/thai-whisper/scripts/whisper_transcribe.py "$video_path"
```

---

**✅ วิธีที่ 3: Tab Completion (เร็วที่สุด!)**

```bash
# พิมพ์บางส่วน แล้วกด Tab → auto-complete
python /notebooks/thai-whisper/scripts/whisper_transcribe.py /notebooks/thai-w[TAB]

# กด Tab อีกครั้ง:
python /notebooks/thai-whisper/scripts/whisper_transcribe.py /notebooks/thai-whisper/videos/ep-[TAB]

# ผลลัพธ์:
python /notebooks/thai-whisper/scripts/whisper_transcribe.py /notebooks/thai-whisper/videos/ep-02061024.mp4
```

**ข้อดี:**
- เร็วที่สุด (ไม่ต้อง copy/paste)
- ไม่มีทาง typo
- ใช้ได้กับทุก shell

**⚠️ หมายเหตุ:** Tab completion ใช้ได้ดีกับไฟล์ไม่มีช่องว่าง/วงเล็บ

---

**✅ วิธีที่ 4: ใช้ Wildcard (ถ้าไฟล์เดียวในโฟลเดอร์)**

```bash
# ถ้ามีแค่ 1 ไฟล์ mp4 ใน videos/
python /notebooks/thai-whisper/scripts/whisper_transcribe.py \
  /notebooks/thai-whisper/videos/*.mp4
```

**ข้อดี:**
- ไม่ต้องพิมพ์ชื่อไฟล์เต็ม
- ใช้ได้ถ้ามีไฟล์เดียว

**⚠️ ระวัง:** ถ้ามีหลายไฟล์ จะ error!

---

**📋 สรุป - เลือกวิธีที่ชอบ:**

| วิธี | ความง่าย | ความปลอดภัย | เหมาะกับ |
|------|---------|-------------|----------|
| **ตัวแปร** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ใช้ซ้ำหลายครั้ง |
| **หาอัตโนมัติ** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | มือใหม่, ขี้เกียจ |
| **Tab Completion** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | มือเก่า, เร็ว |
| **Wildcard** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 1 ไฟล์ในโฟลเดอร์ |

**🎯 แนะนำ:** ใช้ **วิธีที่ 2 (หาอัตโนมัติ)** สำหรับมือใหม่ - ไม่ต้อง copy/paste เลย!

---

**กด Enter → รอถอดเสียง...**

---

### 📺 Output ที่จะเห็น

```
======================================================================
PAPERSPACE WHISPER TRANSCRIBER
======================================================================
Video: ep-02(061024).mp4
Size: 1518.6 MB
Device: cuda
GPU: NVIDIA RTX A4000

⏳ Loading Whisper model...
✓ Model loaded in 2.8s

⏳ Starting transcription...
   (This may take several minutes...)

[00:00.000 --> 00:05.200] สวัสดีครับ วันนี้เราจะมาพูดถึง...
[00:05.200 --> 00:10.500] การเทรด Forex แบบ Price Action...
[00:10.500 --> 00:15.800] เริ่มจากการดูที่แท่งเทียนก่อน...
...

✅ Transcription complete!
   Duration: 59:23
   Segments: 277
   Words: 8,543
   Processing time: 189.4s
   Speed: 18.8x realtime

📁 Output saved:
   File: ep-02(061024)_transcript.json
   Path: /home/jovyan/thai-whisper/transcripts/ep-02(061024)_transcript.json
   Size: 234.5 KB
======================================================================

✅ SUCCESS! Transcript saved to: ...
```

---

### 🔌 ปิดบราวเซอร์ระหว่างรันได้ไหม?

**✅ ได้ครับ! ปิดได้เลย - ไม่หยุดทำงาน**

เพราะรันใน **Terminal** (ไม่ใช่ Notebook cell) → Process ทำงานบน Paperspace server โดยอิสระ

---

#### 💡 ทำไมปิดบราวเซอร์แล้วไม่หยุด?

```
┌─────────────────────────────────────────────┐
│         Terminal Process (ที่คุณใช้)         │
├─────────────────────────────────────────────┤
│  Browser → Paperspace Server               │
│              ↓                              │
│         Terminal (bash)                     │
│              ↓                              │
│    python script.py (รันอิสระ)             │
│              ↓                              │
│            GPU ⚡                            │
│                                             │
│  ✅ ปิด browser → process ยังทำงานต่อ!      │
│  ✅ Network ขาด → process ยังทำงานต่อ!       │
│  ✅ หลับคอม → process ยังทำงานต่อ!          │
│  ✅ ไปทำอะไรต่อ → process ยังทำงานต่อ!      │
└─────────────────────────────────────────────┘
```

**หลักการ:**
- Process รันบน **Paperspace server** (ในคลาวด์)
- **ไม่ได้** รันบนคอมคุณ
- Browser เป็นแค่ "หน้าต่างดู" ไม่ใช่ตัวรัน

---

#### ✅ สิ่งที่ทำได้ระหว่างรัน Whisper

1. **ปิดบราวเซอร์**
2. **ปิดแท็บ Paperspace**
3. **ปิดคอมพิวเตอร์**
4. **ไปทำอะไรต่อ** (กินข้าว, นอน, ทำงานอื่น)
5. **กลับมาเช็คทีหลัง**

---

#### 🔍 วิธีเช็คสถานะเมื่อกลับมา

```bash
# 1. เข้า Paperspace ใหม่ → เปิด Terminal

# 2. เช็คว่า Whisper ยังทำงานอยู่ไหม
ps aux | grep whisper

# ถ้าเห็นแบบนี้ = ยังทำงานอยู่
# root  12345  98.5  15.2  python scripts/whisper_transcribe.py

# ถ้าไม่เห็น = เสร็จแล้ว

# 3. เช็คไฟล์ output (ดูว่าเสร็จหรือยัง)
ls -lh /notebooks/thai-whisper/transcripts/*.json

# ถ้าเห็นไฟล์ขนาดใหญ่ (เช่น 234 KB) = เสร็จแล้ว

# 4. ดู GPU usage
nvidia-smi

# ถ้าเห็น python ใช้ GPU memory = กำลังทำงาน
# ถ้าไม่เห็น = เสร็จแล้ว
```

---

#### 🛡️ (Optional) ใช้ tmux เพื่อความมั่นใจเพิ่ม

ถ้าต้องการมั่นใจยิ่งขึ้น ใช้ **tmux** (Terminal multiplexer):

```bash
# ก่อนรัน Whisper: สร้าง tmux session
tmux new -s whisper

# รัน Whisper ตามปกติ
cd /notebooks/thai-whisper
python scripts/whisper_transcribe.py videos/ep-02061024.mp4

# ปิดบราวเซอร์ได้เลย!
# กด: Ctrl+B แล้วกด D (detach session)

# ─── เมื่อกลับมา ───

# Attach session กลับมา (จะเห็นหน้าจอเดิม)
tmux attach -t whisper

# ดู session ทั้งหมด
tmux ls
```

**ข้อดีของ tmux:**
- เห็นหน้าจอเดิมเมื่อกลับมา
- รันหลาย task พร้อมกัน (แยก window)
- ป้องกัน accidental disconnect

---

#### 📊 ระยะเวลาที่คาดการณ์ (สำหรับวางแผน)

**ตัวอย่าง: ไฟล์ 1518.6 MB (~1.5 ชม. วิดีโอ) + GPU RTX 5000**

```
คาดการณ์:
- วิดีโอยาว: ~90 นาที (1.5 ชม.)
- เวลาถอดข้อความ: 3.5-5 นาที
- คุณปิดบราวเซอร์ไปทำอะไรได้เลย
- 5-10 นาทีกลับมาเช็คก็พอ!
```

**ดูเวลาโดยประมาณแต่ละ GPU:**
- **RTX 5000 Ada**: 1 ชม. วิดีโอ → **2.5-3 นาที**
- **RTX 4000 Ada**: 1 ชม. วิดีโอ → **3-4 นาที**
- **RTX A4000**: 1 ชม. วิดีโอ → **3-6 นาที**
- **P5000**: 1 ชม. วิดีโอ → **5-8 นาที**

---

#### 🎯 สรุป

| สถานการณ์ | ได้หรือไม่ | หมายเหตุ |
|-----------|-----------|---------|
| ปิดบราวเซอร์ | ✅ ได้ | Process รันบน server |
| ปิดคอมพิวเตอร์ | ✅ ได้ | ไม่กระทบ server |
| Network ขาด | ✅ ไม่เป็นไร | Process ยังรันต่อ |
| ปิดแท็บ Paperspace | ✅ ได้ | กลับมาเปิดใหม่ได้ |
| Disconnect terminal accidentally | ✅ ไม่เป็นไร | Process ยังรันต่อ |

**💡 คำแนะนำ:**
- ถ้างานสั้น (< 5 นาที): เปิดบราวเซอร์ดูได้เลย
- ถ้างานยาว (> 10 นาที): ปิดไปทำอะไรต่อได้ กลับมาเช็ค
- ถ้าต้องการมั่นใจ: ใช้ tmux

---

### ⏱️ เวลาที่ใช้ Transcribe - เปรียบเทียบ GPU

**🎯 สำหรับ Whisper large-v3 (2.88 GB model)**

#### ตารางเปรียบเทียบ GPU ต่างๆ

| GPU | VRAM | Architecture | Speed | **1 ชม. → เวลาถอด** | ค่าใช้จ่าย/ชม. | สถานะ |
|-----|------|--------------|-------|---------------------|----------------|-------|
| **RTX 5000 Ada** | 32 GB | Ada Lovelace | 18-25x | **2.5-3 นาที** | ~$1.10 | ⭐⭐⭐⭐⭐ เร็วที่สุด |
| **RTX 4000 Ada** | 20 GB | Ada Lovelace | 15-20x | **3-4 นาที** | ~$0.76 | ⭐⭐⭐⭐⭐ แนะนำ |
| **RTX A4000** | 16 GB | Ampere | 10-20x | **3-6 นาที** | ~$0.76 | ⭐⭐⭐⭐⭐ ดี (ใช้ในคู่มือนี้) |
| **P5000** | 16 GB | Pascal | 8-12x | **5-8 นาที** | ~$0.51 | ⭐⭐⭐ ช้ากว่า |
| **P4000** | 8 GB | Pascal | 6-10x | **6-10 นาที** | ~$0.51 | ⭐⭐ ช้า, VRAM น้อย |

**📊 คำอธิบาย:**
- **Speed**: เร็วกว่า realtime กี่เท่า (ยิ่งสูงยิ่งเร็ว)
- **1 ชม. → เวลาถอด**: วิดีโอ 1 ชั่วโมงใช้เวลาถอดเท่าไหร่
- **ค่าใช้จ่าย**: ประมาณการจาก Paperspace pricing

---

#### ตัวอย่างเวลาถอดเสียงแต่ละ GPU

**📹 วิดีโอ 1 ชั่วโมง (60 นาที):**

| GPU | เวลาถอดเสียง | ตัวอย่าง |
|-----|-------------|---------|
| **RTX 5000 Ada** | 2.5-3 นาที | 60 min ÷ 21.5x = 2.8 min |
| **RTX 4000 Ada** | 3-4 นาที | 60 min ÷ 17.5x = 3.4 min |
| **RTX A4000** | 3-6 นาที | 60 min ÷ 15x = 4 min |
| **P5000** | 5-8 นาที | 60 min ÷ 10x = 6 min |
| **P4000** | 6-10 นาที | 60 min ÷ 8x = 7.5 min |

**📹 วิดีโอความยาวต่างๆ (RTX A4000):**

| ความยาววิดีโอ | เวลาถอดเสียง | Speed |
|--------------|-------------|-------|
| 10 นาที | 30-60 วินาที | 10-20x |
| 30 นาที | 1.5-3 นาที | 10-20x |
| 1 ชั่วโมง | 3-6 นาที | 10-20x |
| 2 ชั่วโมง | 6-12 นาที | 10-20x |

---

#### 🎯 คำแนะนำการเลือก GPU

**🆓 ถ้า Growth Plan ($8/month) ให้ใช้ GPU ฟรีทุกตัว:**

```
🎉 ไม่ต้องคิดเรื่องราคา → เลือกเร็วที่สุด!

แนะนำเรียงตามความเร็ว:
1️⃣ RTX 5000 Ada  ← เร็วที่สุด (2.5-3 นาที/1 ชม.)
2️⃣ RTX 4000 Ada  ← เร็วรองลงมา (3-4 นาที/1 ชม.)
3️⃣ RTX A4000     ← เร็วพอใช้ (3-6 นาที/1 ชม.)

💡 เคล็ดลับ:
- เลือกเร็วสุดที่มีให้ใช้ (RTX 5000 Ada หรือ RTX 4000 Ada)
- ถ้าไม่มี → ใช้ RTX A4000 (ตามคู่มือนี้)
- หลีกเลี่ยง P4000 (VRAM 8GB น้อยเกินไป)

⚠️ หมายเหตุ:
- GPU รุ่นใหม่ (Ada) อาจไม่มีทุก region
- เช็คว่ามีให้ใช้ก่อน: Dashboard → Instance Type
```

---

**💰 ถ้าต้องจ่ายเพิ่มต่อชั่วโมง (Pay-as-you-go):**

**✅ แนะนำ (เร็ว + คุ้มค่า):**
- **RTX 4000 Ada** - สมดุลที่สุด (เร็ว, ราคาพอดี, VRAM 20GB)
- **RTX A4000** - ดีมาก (ใช้ในคู่มือนี้, เร็วพอ, ราคาดี)

**⭐ เร็วที่สุด (ถ้างบพอ):**
- **RTX 5000 Ada** - เร็วที่สุด แต่แพงกว่า (~$1.10/ชม.)

**💰 ประหยัด (ถ้างบน้อย):**
- **P5000** - ช้ากว่า แต่ถูกกว่า (~$0.51/ชม.)
- **P4000** - ไม่แนะนำ (VRAM 8GB อาจไม่พอ, ช้า)

---

#### ⚠️ GPU ที่ต้องระวัง

**P4000 (8 GB VRAM):**
```
🚨 คำเตือน: VRAM เพียง 8 GB อาจไม่พอสำหรับ large-v3!

อาจเกิดปัญหา:
- CUDA out of memory
- ต้องใช้ base/small/medium model แทน
- หรือใช้ CPU mode (ช้ามาก + อาจ Killed)

แนะนำ: เลือก GPU ที่มี VRAM ≥ 16 GB
```

---

#### 💡 เคล็ดลับ: เลือก GPU ใน Paperspace

**วิธีดู GPU ที่มี:**
1. ไป Paperspace Dashboard
2. Create Notebook → เลือก Instance Type
3. ดู GPU options ที่มี

**วิธีเปลี่ยน GPU (ถ้าต้องการ):**
1. Stop Notebook
2. Settings → Instance Type
3. เลือก GPU รุ่นใหม่ (RTX 4000 Ada / RTX 5000 Ada)
4. Start Notebook ใหม่

**⚠️ หมายเหตุ:**
- GPU รุ่นใหม่ (Ada) อาจไม่มีทุก region
- ราคาแตกต่างกันตาม GPU
- Performance อาจแตกต่างตามภาระงานของ Paperspace

---

#### 📋 สรุป: ควรเลือก GPU ไหน?

**🔍 เช็คก่อนว่า Growth Plan ของคุณครอบคลุมอะไรบ้าง:**

```bash
# วิธีเช็ค:
1. ไป Paperspace Dashboard
2. Create/Edit Notebook
3. ดู Instance Type → GPU options
4. สังเกต "Included" หรือ "$X.XX/hr"

ถ้าเห็น "Included" → ฟรี! ใช้ GPU นั้นได้เลย
ถ้าเห็น "$X.XX/hr" → ต้องจ่ายเพิ่ม
```

---

**🆓 กรณีที่ 1: ถ้าใช้ GPU ฟรีทุกตัว (หรือไม่สนราคา)**

| GPU | ความเร็ว | แนะนำ | เหตุผล |
|-----|---------|-------|--------|
| **RTX 5000 Ada** | ⭐⭐⭐⭐⭐ | 🏆 **เลือกนี้!** | เร็วที่สุด (2.5-3 นาที/1 ชม.) |
| **RTX 4000 Ada** | ⭐⭐⭐⭐⭐ | 🥈 รองลงมา | เร็วมาก (3-4 นาที/1 ชม.) |
| **RTX A4000** | ⭐⭐⭐⭐ | ✅ ดี | เร็วพอใช้ (3-6 นาที/1 ชม.) |
| **P5000** | ⭐⭐⭐ | ⚠️ ไม่แนะนำ | ช้ากว่า (5-8 นาที/1 ชม.) |
| **P4000** | ⭐⭐ | ❌ หลีกเลี่ยง | ช้า + VRAM น้อย |

**🎯 สรุป:** เลือกเร็วที่สุดที่มีให้ใช้ → **RTX 5000 Ada** > **RTX 4000 Ada** > **RTX A4000**

---

**💰 กรณีที่ 2: ถ้าต้องจ่ายเพิ่มต่อชั่วโมง**

| GPU | คุ้มค่า | เหตุผล |
|-----|---------|--------|
| **RTX 4000 Ada** | ⭐⭐⭐⭐⭐ | เร็ว + VRAM เยอะ + ราคาพอดี |
| **RTX A4000** | ⭐⭐⭐⭐⭐ | สมดุล (ใช้ในคู่มือนี้) |
| **RTX 5000 Ada** | ⭐⭐⭐⭐ | เร็วที่สุด แต่แพงกว่า |
| **P5000** | ⭐⭐⭐ | ถูกกว่า แต่ช้ากว่า |
| **P4000** | ⭐⭐ | VRAM น้อย, ไม่แนะนำ |

**🎯 คำแนะนำ:**
- **มือใหม่**: ใช้ **RTX A4000** (ตามคู่มือนี้) - สมดุลดี
- **ใช้บ่อย**: ใช้ **RTX 4000 Ada** - เร็วกว่า, คุ้มค่าในระยะยาว
- **งบน้อย**: ใช้ **P5000** - ช้ากว่าแต่ยังใช้ได้

---

**💡 Quick Decision Guide:**

```
คำถาม: GPU ที่เลือกเป็น "Included" ไหม?

✅ ใช่ (ฟรี):
   → เลือกเร็วที่สุด: RTX 5000 Ada หรือ RTX 4000 Ada

❌ ไม่ (ต้องจ่ายเพิ่ม):
   → เลือกคุ้มค่า: RTX 4000 Ada หรือ RTX A4000

🚫 ไม่มีทั้ง 3 ตัว:
   → เลือก P5000 (แต่ช้ากว่า)
   → หลีกเลี่ยง P4000 (VRAM น้อย)
```

---

✅ **ถอดเสียงเสร็จ!**

---

## PART 6: Download ผลลัพธ์

### ✅ STEP 17: ไปที่โฟลเดอร์ transcripts

**ใน File Browser:**

```
1. Navigate ไปที่ thai-whisper/transcripts/

2. ควรเห็นไฟล์ JSON:
   ep-02(061024)_transcript.json
```

---

### ✅ STEP 18: Download ไฟล์

```
1. คลิกขวาที่ไฟล์ JSON

2. เลือก "Download"

3. เลือกที่จะบันทึกในเครื่อง

4. รอ download เสร็จ (ไฟล์เล็ก < 1 MB ใช้เวลาไม่กี่วินาที)
```

✅ **ได้ไฟล์ Transcript แล้ว!**

---

### ✅ STEP 19: ตรวจสอบไฟล์ (Optional)

**เปิดไฟล์ JSON ด้วย Text Editor:**

**ควรเห็น:**
```json
{
  "video_name": "ep-02(061024).mp4",
  "timestamp": "2025-10-07T10:30:15.123456",
  "metadata": {
    "language": "th",
    "model_name": "large-v3",
    "duration": 3563.2,
    "segment_count": 277,
    "word_count": 8543
  },
  "text": "สวัสดีครับ วันนี้เราจะมาพูดถึง...",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.2,
      "text": "สวัสดีครับ วันนี้เราจะมาพูดถึง...",
      "words": [...]
    },
    ...
  ]
}
```

✅ **ไฟล์ถูกต้อง พร้อมใช้งาน!**

---

## PART 7: ใช้ Transcript ต่อ (แปลเป็นภาษาอังกฤษ)

**⚠️ สำคัญ: PART นี้ทำในเครื่องของคุณ (ไม่ใช่ Paperspace!)**

```
📍 ทำที่ไหน: เครื่องคอมพิวเตอร์ของคุณ (Local)
❌ ไม่ใช่: Paperspace Notebook

💡 หมายเหตุ:
- ใช้ Terminal บนเครื่องของคุณ (Mac/Linux/WSL)
- ~ ในส่วนนี้ใช้ได้ (ชี้ไปที่ home directory ของคุณ)
- ต้องมี video-translater project ติดตั้งไว้แล้ว
- ต้องมี .venv (virtual environment) setup แล้ว
```

---

### ✅ STEP 20: ใช้กับ video-translater Project

**ในเครื่องของคุณ (Local Terminal):**

```bash
# 1. ย้ายไฟล์ transcript ที่ download จาก Paperspace มา
mv ~/Downloads/ep-02_transcript.json \
   ~/projects/video-translater/workflow/01_transcripts/

# 2. สร้าง batch สำหรับแปล
cd ~/projects/video-translater/
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/ep-02_transcript.json

# 3. แปลด้วย Claude Code (manual)
# - เปิด workflow/02_for_translation/ep-02_batch.txt
# - Copy Thai text → Paste to Claude Code
# - แปลเป็นภาษาอังกฤษ (casual teaching tone)
# - Save to workflow/03_translated/ep-02_translated.txt

# 4. สร้าง SRT
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/ep-02_transcript.json \
  workflow/03_translated/ep-02_translated.txt \
  -o workflow/04_final_srt/ep-02_english.srt
```

✅ **ได้ English SRT พร้อมใช้!**

---

## 📊 สรุป Workflow ทั้งหมด

```
┌─────────────────────────────────────────────────────────┐
│ PAPERSPACE (Cloud GPU)                                  │
├─────────────────────────────────────────────────────────┤
│ 1. สร้างโฟลเดอร์ (Jupyter UI)          → 5 นาที       │
│ 2. ติดตั้ง Whisper (Terminal)           → 5 นาที       │
│ 3. สร้าง Script (Jupyter UI)            → 5 นาที       │
│ 4. gdown จาก Google Drive ⭐            → 2-4 นาที     │
│ 5. ถอดเสียง (Terminal)                  → 3-8 นาที     │
│ 6. Download JSON (Jupyter UI)           → 1 นาที       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ LOCAL (Your Computer)                                   │
├─────────────────────────────────────────────────────────┤
│ 7. สร้าง batch (Python script)          → 10 วินาที    │
│ 8. แปลด้วย Claude Code (Manual)         → 10-15 นาที   │
│ 9. สร้าง SRT (Python script)            → 10 วินาที    │
└─────────────────────────────────────────────────────────┘
                          ↓
                   ✅ English SRT
```

**รวมทั้งหมด:**
- **ครั้งแรก**: 25-35 นาที (รวม setup)
- **ครั้งต่อไป**: 8-15 นาที (ไม่ต้อง setup)
- **ต้นทุน**: ~$0.10/วิดีโอ (ใช้ gdown) 💰

---

## 💰 ค่าใช้จ่าย

### Paperspace Costs (RTX A4000 @ $0.76/hour)

**ตัวอย่าง 1 วิดีโอ (1 ชั่วโมง, 1.5 GB):**

**ใช้ Google Drive + gdown (แนะนำ):**
```
Setup (ครั้งแรก):      15 นาที  = $0.19
gdown:                  3 นาที  = $0.04
Transcribe:             5 นาที  = $0.06
Download:               2 นาที  = $0.03
────────────────────────────────────────
รวม (ครั้งแรก):       25 นาที  = $0.32

ครั้งต่อไป (ไม่ต้อง setup):
gdown + Transcribe:     8 นาที  = $0.10
────────────────────────────────────────
```

**ใช้ Jupyter UI Upload (ช้ากว่า):**
```
Setup (ครั้งแรก):      15 นาที  = $0.19
Upload UI:             20 นาที  = $0.25
Transcribe:             5 นาที  = $0.06
Download:               2 นาที  = $0.03
────────────────────────────────────────
รวม (ครั้งแรก):       42 นาที  = $0.53

ครั้งต่อไป:
Upload + Transcribe:   25 นาที  = $0.32
────────────────────────────────────────
```

**10 วิดีโอ/เดือน (ใช้ gdown):**
```
ครั้งแรก:    $0.32
อีก 9 ครั้ง:  $0.10 × 9 = $0.90
────────────────────────────────────
รวม:         ~$1.22
เหลือ credits: $8.00 - $1.22 = $6.78
```

**💡 ประหยัดมาก!**
- **ใช้ gdown**: $0.10-0.12/วิดีโอ ⭐⭐⭐⭐⭐
- **ใช้ UI upload**: $0.32/วิดีโอ (แพงกว่า 3 เท่า)

---

## 💡 Tips & Best Practices

### 1. **ปิด Notebook เมื่อไม่ใช้** ⚠️

```
⚠️ สำคัญที่สุด!

Paperspace คิดเงินต่อชั่วโมงที่ notebook รันอยู่

ทำเสร็จแล้ว → ปิดทันที!

Dashboard → Notebooks → [Your Notebook] → Stop
```

### 2. **ใช้ Google Drive + gdown แทน Upload UI** ⭐

```
ประหยัดเวลา 75-80%!

แทนที่จะ Upload ผ่าน Jupyter UI (15-30 นาที)
→ ใช้ gdown (2-4 นาที)

วิธี:
1. Upload วิดีโอไป Google Drive ก่อน (ทำที่บ้าน)
2. ใน Paperspace: gdown --fuzzy "DRIVE_LINK"
3. เร็วกว่า + ประหยัดค่า GPU time!
```

### 2.5 **ถ้าใช้บ่อย → Setup rclone ครั้งเดียว** 🚀

```
ข้อดี rclone:
✅ Setup ครั้งเดียว ใช้ตลอด
✅ Resume ได้ (ไฟล์ใหญ่มาก)
✅ Progress bar ชัดเจน
✅ รองรับทุก cloud

เหมาะกับ:
- มีหลายวิดีโอต้องถอดเสียงบ่อยๆ
- ไฟล์ใหญ่ > 5 GB
- ต้องการ resume (internet ไม่เสถียร)

Setup: 5-7 นาที ครั้งแรก
ใช้ครั้งต่อไป: 10 วินาที (แค่ rclone copy)

ดูวิธี: PART 4 → วิธี E
```

### 3. **ใช้ Auto-shutdown**

```
Notebook Settings → Auto-shutdown: 6 hours

ถ้าลืมปิด จะปิดเองหลัง 6 ชั่วโมง (ประหยัดเงิน)
```

### 3.5 **⚠️ ระวัง `~` (Tilde) ใน Paperspace!**

```
🚨 สำคัญมาก - อย่าใช้ ~ ใน Paperspace!

❌ ผิด:
cd ~/thai-whisper/
python ~/thai-whisper/scripts/script.py
find ~ -name "*.mp4"

✅ ถูกต้อง:
cd /notebooks/thai-whisper/
python /notebooks/thai-whisper/scripts/script.py
find /notebooks -name "*.mp4"

🔍 ทำไม?
~ ใน Paperspace ชี้ไปที่ /root/ ไม่ใช่ /notebooks/
ดังนั้น ~/thai-whisper/ จริงๆ คือ /root/thai-whisper/ (ไม่มีโฟลเดอร์!)

💡 วิธีเช็ค:
echo ~        # จะได้ /root
pwd           # ดู path ปัจจุบัน

💡 แนะนำ:
- ใช้ absolute path /notebooks/ เสมอ
- หรือ relative path (ถ้าอยู่ใน /notebooks/ แล้ว)
- อย่าใช้ ~ เลยใน Paperspace!

ดูเพิ่มเติม: Troubleshooting → ปัญหา 2.2 และ 2.2.1
```

### 4. **🚨 ตรวจสอบ Whisper Hallucination/Repetition** (สำคัญ!)

**ปัญหา: Whisper ถอดเสียงผิด - ออกมาซ้ำๆ กันหรือเพี้ยน**

```
❌ ตัวอย่างปัญหา:
[19:01.860 --> 19:31.840] แสดงสันแสดงแสดงแสดงแสดงแสดง...
(ซ้ำกันตลอด 30 วินาที!)

หรือ:
[05:23.000 --> 05:55.000] ครับครับครับครับครับครับครับ...
[10:12.000 --> 10:45.000] ขอบคุณขอบคุณขอบคุณขอบคุณ...
[15:30.000 --> 16:20.000] Thank you for watching. Thank you for...
```

---

#### 🔍 สาเหตุที่เกิด Hallucination:

**1. Silent/Pause ยาว**
```
วิดีโอเงียบเกิน 10-30 วินาที → Whisper พยายามถอดเสียง
→ เกิด hallucination (สร้างคำขึ้นมาเอง)
```

**2. Background Noise**
```
เสียงรบกวน/เสียงหึ่งๆ → Whisper คิดว่าเป็นคำพูด
→ ถอดออกมาเป็นคำซ้ำๆ
```

**3. Audio Quality ไม่ดี**
```
เสียงตัด, เสียงเบา, คุณภาพต่ำ
→ Whisper งง → เกิด repetition
```

**4. ท้ายวิดีโอ (outro music/credits)**
```
มีแต่เพลง/เสียงพื้นหลัง ไม่มีคำพูด
→ Whisper พยายามถอด → เกิด hallucination
```

---

#### ✅ วิธีตรวจสอบหลังถอดเสียงเสร็จ:

**Method 1: ใช้ grep หา patterns ผิดปกติ**

```bash
# 1. หาข้อความที่ยาวผิดปกติ (> 1000 characters)
cat transcript.json | grep -o '"text": "[^"]*"' | awk 'length > 1000'

# 2. หาคำที่ซ้ำมาก (เช่น ซ้ำ > 10 ครั้ง)
cat transcript.json | grep -o '"text": "[^"]*"' | grep -E '(\b\w+\b)(\s+\1){10,}'

# 3. เช็คว่ามี segment ยาวผิดปกติ (> 60 วินาที)
cat transcript.json | grep -E '"start": [0-9]+\.[0-9]+, "end": [0-9]+\.[0-9]+'
```

**Method 2: ตรวจสอบด้วยตา**

```bash
# ดู transcript แบบอ่านง่าย
cat transcript.json | jq '.segments[] | "\(.start) - \(.end): \(.text)"' | less

# หา segment ที่ยาว
cat transcript.json | jq '.segments[] | select((.end - .start) > 30)'
```

**🚩 Red Flags ที่ต้องระวัง:**
- ข้อความซ้ำๆ เหมือนกันยาวเกิน 5 วินาที
- Segment ยาวเกิน 60 วินาที (ปกติ 5-15 วินาที)
- คำเดียวซ้ำ > 10 ครั้งติดกัน
- ข้อความภาษาอังกฤษปนเยอะ (ในวิดีโอไทย)
- "Thank you for watching" ซ้ำๆ

---

#### 🛠️ วิธีแก้ไขหลังเจอปัญหา:

**Option 1: แก้ใน whisper_transcribe.py Script (แนะนำ!)**

**🎯 แก้ไข script ตั้งแต่แรก - ป้องกันดีที่สุด!**

ไฟล์: `/notebooks/thai-whisper/scripts/whisper_transcribe.py`

**หา code block นี้:**
```python
# ในส่วน transcribe
result = model.transcribe(
    str(audio_path),
    language="th",
    task="transcribe",
    word_timestamps=True,
    temperature=(0.0, 0.2, 0.4, 0.6, 0.8),
    beam_size=5,
    best_of=5,
)
```

**แก้เป็น (เพิ่ม anti-hallucination parameters):**
```python
result = model.transcribe(
    str(audio_path),
    language="th",
    task="transcribe",
    word_timestamps=True,

    # Temperature
    temperature=(0.0, 0.2, 0.4, 0.6, 0.8),

    # Beam search
    beam_size=5,
    best_of=5,

    # 🚨 เพิ่มการป้องกัน hallucination/repetition
    compression_ratio_threshold=2.2,    # เข้มงวดกว่าปกติ (default: 2.4)
    logprob_threshold=-1.5,             # กรองคำที่ไม่แน่ใจ (default: -1.0)
    no_speech_threshold=0.7,            # ตรวจจับเงียบดีขึ้น (default: 0.6)

    # ป้องกัน repetition
    condition_on_previous_text=True,    # ใช้ context จาก segment ก่อนหน้า
    prompt_reset_on_temperature=0.5,    # Reset prompt ถ้า temperature สูง

    # Initial prompt (ช่วยให้ Whisper เข้าใจ context)
    initial_prompt="นี่คือการสอนเทรด Forex และการลงทุน",
)
```

**💡 อธิบาย parameters:**

| Parameter | ค่า | ทำอะไร |
|-----------|-----|--------|
| `compression_ratio_threshold` | 2.2 | ถ้าข้อความซ้ำมาก (ratio สูง) → ปฏิเสธ |
| `logprob_threshold` | -1.5 | ถ้า model ไม่แน่ใจ (prob ต่ำ) → ปฏิเสธ |
| `no_speech_threshold` | 0.7 | ถ้าเงียบ → ไม่ต้องถอด (ป้องกัน hallucination) |
| `condition_on_previous_text` | True | ใช้ข้อความก่อนหน้าช่วยตัดสินใจ |
| `prompt_reset_on_temperature` | 0.5 | Reset context ถ้า temperature สูง |
| `initial_prompt` | "..." | บอก context ให้ Whisper |

---

**📝 วิธีแก้ไข Script ใน Paperspace:**

**1. เปิดไฟล์ (ใน Jupyter UI):**
```
File Browser → thai-whisper/scripts/whisper_transcribe.py
→ Double-click เปิด
```

**2. หาบรรทัดที่มี `model.transcribe(`**
```
ใช้ Ctrl+F → ค้นหา "model.transcribe"
```

**3. แก้ไข parameters:**
```
เพิ่ม 5 บรรทัดใหม่ (ตามด้านบน)
```

**4. Save:**
```
Ctrl+S หรือ File → Save
```

**5. ถอดเสียงใหม่:**
```bash
python /notebooks/thai-whisper/scripts/whisper_transcribe.py video.mp4
```

---

**🎯 ถ้าต้องการ parameters เข้มงวดมากกว่า (สำหรับวิดีโอที่เจอปัญหาบ่อย):**

```python
result = model.transcribe(
    str(audio_path),
    language="th",
    task="transcribe",
    word_timestamps=True,

    # ใช้ temperature ต่ำกว่า (แน่นอนขึ้น)
    temperature=0.0,  # แทน tuple

    # Beam search
    beam_size=5,
    best_of=5,

    # เข้มงวดมาก!
    compression_ratio_threshold=2.0,    # เข้มงวดมากกว่าปกติ
    logprob_threshold=-2.0,             # กรองเข้มงวดกว่า
    no_speech_threshold=0.8,            # เช็คเงียบเข้มงวดกว่า

    condition_on_previous_text=True,
    prompt_reset_on_temperature=0.5,
    initial_prompt="นี่คือการสอนเทรด Forex และการลงทุน",
)
```

**⚠️ หมายเหตุ:**
- ค่าเข้มงวดเกินไป → อาจตัดคำที่ถูกต้องทิ้งด้วย
- ลองใช้ค่าปกติก่อน (2.2, -1.5, 0.7)
- ถ้ายังเจอปัญหา → ใช้ค่าเข้มงวดกว่า

---

**✅ ผลลัพธ์หลังแก้:**
- ✅ ลด hallucination/repetition ลง 80-90%
- ✅ Segment ที่เงียบไม่ถูกถอด (ถูกต้อง)
- ✅ คำที่ไม่แน่ใจถูกข้าม (ดีกว่าผิด)

---

**Option 2: ตัด segment ที่ผิดออก (Manual)**

```python
# ถ้าเจอแค่ 2-3 segments ผิด
# แก้ใน transcript JSON โดยตรง

import json

# โหลด transcript
with open('transcript.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ลบ segment ที่ผิด (เช่น segment ที่ 125)
data['segments'] = [s for s in data['segments'] if s['id'] not in [125, 126, 127]]

# บันทึก
with open('transcript_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

**Option 3: ใช้ script กรอง hallucination อัตโนมัติ**

```python
# สร้างไฟล์: clean_hallucination.py

import json
import re

def is_hallucination(text):
    """ตรวจสอบว่าเป็น hallucination มั้ย"""

    # 1. เช็คคำซ้ำมาก
    words = text.split()
    if len(words) > 10:
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
        max_repeat = max(word_counts.values())
        if max_repeat > len(words) * 0.5:  # ถ้าคำซ้ำเกิน 50%
            return True

    # 2. เช็คข้อความยาวผิดปกติ
    if len(text) > 500 and len(set(text.split())) < 20:
        return True

    # 3. เช็ค common hallucination phrases
    hallucination_patterns = [
        r'(ขอบคุณ\s*){5,}',
        r'(ครับ\s*){8,}',
        r'(แสดง\S*\s*){5,}',
        r'(Thank you for watching.*){2,}',
    ]
    for pattern in hallucination_patterns:
        if re.search(pattern, text):
            return True

    return False

def clean_transcript(input_file, output_file):
    """ทำความสะอาด transcript"""

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_count = len(data['segments'])

    # กรอง segment ที่เป็น hallucination ออก
    clean_segments = []
    removed_segments = []

    for segment in data['segments']:
        duration = segment['end'] - segment['start']
        text = segment['text'].strip()

        # เช็คเงื่อนไข
        if (is_hallucination(text) or
            duration > 60 or  # ยาวเกิน 1 นาที
            (duration > 30 and len(text) < 20)):  # ยาว 30 วิ แต่มีคำน้อย
            removed_segments.append({
                'id': segment['id'],
                'text': text[:100] + '...' if len(text) > 100 else text,
                'reason': 'hallucination'
            })
        else:
            clean_segments.append(segment)

    data['segments'] = clean_segments

    # บันทึก
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Report
    print(f"✅ Original: {original_count} segments")
    print(f"✅ Cleaned: {len(clean_segments)} segments")
    print(f"🗑️  Removed: {len(removed_segments)} segments")

    if removed_segments:
        print("\n🚨 Removed segments:")
        for seg in removed_segments[:5]:  # แสดงแค่ 5 ตัวแรก
            print(f"  - Segment {seg['id']}: {seg['text']}")

# ใช้งาน
if __name__ == '__main__':
    clean_transcript(
        'transcript.json',
        'transcript_clean.json'
    )
```

**รันคำสั่ง:**
```bash
python clean_hallucination.py
```

---

#### 🛡️ วิธีป้องกันตั้งแต่แรก:

**1. ตัดส่วนท้ายวิดีโอออกก่อน (ถ้ามี outro music)**
```bash
# ใช้ ffmpeg ตัดท้ายออก
ffmpeg -i input.mp4 -t 00:58:30 -c copy output.mp4
# ตัดเหลือแค่ 58:30 (ไม่เอา 2 นาทีท้าย)
```

**2. ใช้ Whisper parameters ที่ดี**
```python
# ใส่ใน whisper_transcribe.py
result = model.transcribe(
    audio_path,
    temperature=0.0,           # แน่นอนที่สุด
    no_speech_threshold=0.7,   # เข้มงวดการตรวจจับเงียบ
)
```

**3. เช็ค transcript ทันทีหลังถอดเสร็จ**
```bash
# ดูผลลัพธ์แบบรวดเร็ว
cat transcript.json | jq '.segments[].text' | less

# ถ้าเห็นผิดปกติ → แก้ทันที
```

---

#### 📋 Checklist - หลังถอดเสียงเสร็จ:

- [ ] เปิดดู transcript (jq หรือ text editor)
- [ ] เช็คว่ามี segment ซ้ำๆ ไหม
- [ ] เช็คว่า segment ท้ายสุด (outro) เป็น hallucination ไหม
- [ ] ถ้าเจอปัญหา → ใช้ clean_hallucination.py
- [ ] ถ้ายังไม่ดี → ถอดใหม่ด้วย parameters เข้มงวดกว่า

---

### 5. **Batch Processing - ถอดหลายไฟล์พร้อมกัน**

```bash
# ถ้ามีหลายวิดีโอ → gdown ทั้งหมดก่อน
cd /notebooks/thai-whisper/videos/

# Download จาก Google Drive (หลายไฟล์)
gdown --fuzzy "LINK_1"
gdown --fuzzy "LINK_2"
gdown --fuzzy "LINK_3"

# แล้ว loop ถอดทีเดียว:
for video in /notebooks/thai-whisper/videos/*.mp4; do
  python /notebooks/thai-whisper/scripts/whisper_transcribe.py "$video"
done

# ประหยัดเวลาเปิด-ปิด notebook
# Example: 10 วิดีโอ → เปิด 1 ครั้ง แทน 10 ครั้ง!
```

### 5. **ลบวิดีโอหลังถอดเสร็จ**

```bash
# เพื่อประหยัด storage (200 GB limit)

# ย้ายวิดีโอออก (ดาวน์โหลดก่อนลบ)
rm /notebooks/thai-whisper/videos/*.mp4

# เก็บแค่ transcript JSON (เล็กกว่ามาก - 1.5GB → 200KB!)
```

### 6. **Backup Transcript**

```
Download transcript JSON เก็บไว้หลายที่:
- เครื่องคุณ
- Google Drive
- Dropbox

เพราะ Paperspace notebook อาจถูกลบได้
```

---

## 🐛 Troubleshooting

### ปัญหา 1: ไม่เห็น GPU

```
❌ ปัญหา: nvidia-smi แสดง "command not found" หรือไม่เห็น GPU

✅ แก้:
1. ปิด Notebook
2. Notebook Settings → Instance Type → RTX A4000 (GPU)
3. Start Notebook ใหม่
4. รัน nvidia-smi อีกครั้ง
```

### ปัญหา 1.5: Server Connection Error (ระหว่างติดตั้ง/ใช้งาน)

```
❌ ปัญหา:
Server Connection Error
A connection to the Jupyter server could not be established.
JupyterLab will continue trying to reconnect.
Check your network connection or Jupyter server configuration.

🔍 สาเหตุ:
- Internet connection ขาด (ของคุณหรือของ Paperspace)
- Jupyter session timeout (ไม่ได้ใช้งานนาน)
- Notebook idle เกิน timeout limit
- การติดตั้ง package ใช้เวลานาน → session timeout

💡 ปัญหานี้เกิดได้ตอนไหน?
✓ ระหว่างติดตั้ง Whisper (pip install)
✓ ระหว่าง download model (3-5 นาที)
✓ ระหว่างถอดเสียง (ไฟล์ยาว)
✓ เปิดทิ้งไว้ไม่ได้ใช้งาน

✅ แก้:

วิธี 1: Refresh Browser (ลองก่อน - ง่ายที่สุด)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# กด F5 หรือ Ctrl+R (Cmd+R บน Mac)
# รอ 5-10 วินาที → ดูว่า connection กลับมามั้ย

ถ้ากลับมา → ✅ ดำเนินการต่อได้
ถ้ายังไม่กลับมา → ไปวิธี 2

วิธี 2: เช็ค Notebook Status (ใน Paperspace Dashboard)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# เปิดแท็บใหม่ → ไป paperspace.com
# Dashboard → Notebooks → เช็ค notebook ของคุณ

สถานะ "Running" (สีเขียว):
  → Notebook ยังทำงานอยู่
  → กลับไปหน้า JupyterLab → Refresh (F5)

สถานะ "Stopped" (สีแดง):
  → Notebook หยุดแล้ว (เกิน timeout หรือ error)
  → ต้อง Start ใหม่ → ดูวิธี 3

วิธี 3: Start Notebook ใหม่ + ตรวจสอบ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ใน Paperspace Dashboard
1. คลิก notebook → Start
2. รอจน status เป็น "Running"
3. เปิด JupyterLab ใหม่

# เช็คว่าเสียอะไรมั้ย:

1. เช็คโฟลเดอร์ (ไม่เสีย - persistent storage)
   ls -la /notebooks/thai-whisper/

2. เช็ค Whisper ติดตั้งอยู่มั้ย (เสีย - ต้องติดตั้งใหม่)
   python -c "import whisper; print('OK')"

   ถ้า error → ติดตั้งใหม่:
   pip install -U openai-whisper torch

3. เช็ค Model download มั้ย (อาจเสีย - ต้อง download ใหม่)
   python -c "import whisper; whisper.load_model('large-v3'); print('OK')"

   ถ้า error → download ใหม่ (3-5 นาที)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 สรุป: ต้องทำใหม่อะไรบ้าง?

ถ้า error ระหว่าง:              | ต้องทำใหม่:
---------------------------------|---------------------------
สร้างโฟลเดอร์ (PART 1)          | ❌ ไม่ต้อง (ยังอยู่)
ติดตั้ง Whisper (PART 2)        | ✅ ต้อง (เสีย - ติดตั้งใหม่)
สร้าง Script (PART 3)           | ❌ ไม่ต้อง (ยังอยู่)
Upload วิดีโอ (PART 4)           | ❌ ไม่ต้อง (ยังอยู่)
ถอดเสียง (PART 5)                | ✅ ต้อง (ถ้ายังไม่เสร็จ)
Download transcript (PART 6)    | ❌ ไม่ต้อง (ถ้าเสร็จแล้ว)

💡 เคล็ดลับป้องกัน:
- ติดตั้ง Whisper เสร็จ → ถอดเสียงทันที (อย่าทิ้งไว้)
- ไฟล์ใหญ่ → เปิด Terminal แยก → monitor progress
- Auto-shutdown: ตั้งไว้ 6 ชม. (ป้องกันค่าใช้จ่าย)
```

### ปัญหา 1.6: "Killed" (ระหว่าง Download หรือ Load Model)

```
❌ ปัญหา:
⏳ Downloading large-v3...
100%|█████████████████████████████| 2.88G/2.88G [00:52<00:00, 59.2MiB/s]
Killed

หรือ:

INFO: Device: cpu
⏳ Loading Whisper model...
Killed

🔍 สาเหตุ:
Out of Memory (OOM) - ระบบหมดหน่วยความจำ
→ Process ถูกฆ่าโดย system (OOM Killer)

🚨 สาเหตุที่แท้จริง: กำลังใช้ CPU แทน GPU!

ปัญหานี้เกิดเพราะ:
1. Script detect "Device: cpu" แทน "Device: cuda"
2. Whisper large-v3 (2.88 GB) ใหญ่เกินไปสำหรับ RAM
3. ควรใช้ GPU VRAM (16 GB) แทน CPU RAM (8-16 GB)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ แก้: เช็คและแก้ไข GPU Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: เช็ค GPU ทำงานหรือไม่
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ใน Terminal
nvidia-smi

✅ ถ้าเห็น:
+-----------------------------------------------------------------------------+
| NVIDIA-SMI xxx.xx       Driver Version: xxx.xx       CUDA Version: xx.x    |
|-------------------------------+----------------------+----------------------+
|   0  NVIDIA RTX A4000   ...   |                      |                      |
+-------------------------------+----------------------+----------------------+

→ GPU มีอยู่ แต่ script ไม่เจอ → ไป STEP 2

❌ ถ้าเห็น:
nvidia-smi: command not found
หรือ
Failed to initialize NVML

→ GPU ไม่ได้เปิด → ไป STEP 3 (ต้อง restart notebook)

STEP 2: เช็ค PyTorch เห็น GPU มั้ย
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ใน Terminal
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"

✅ ถ้าได้:
CUDA available: True
Device: NVIDIA RTX A4000

→ GPU พร้อมใช้ → ถอดเสียงได้เลย!

❌ ถ้าได้:
CUDA available: False
Device: CPU only

→ PyTorch ไม่เห็น GPU → ติดตั้ง PyTorch ใหม่:

# ถอนและติดตั้งใหม่ (CUDA version)
pip uninstall torch -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# เช็คอีกครั้ง
python -c "import torch; print('CUDA:', torch.cuda.is_available())"

STEP 3: เปิด GPU ใน Paperspace (ถ้า nvidia-smi ไม่ทำงาน)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ไปที่ Paperspace Dashboard (paperspace.com)
2. Notebooks → เลือก notebook ของคุณ
3. คลิก "Stop" (ถ้ากำลังรันอยู่)
4. คลิก "Settings" หรือ "Edit"
5. Instance Type → เลือก "RTX A4000" (GPU)
6. Save → Start Notebook
7. เปิด Terminal ใหม่ → รัน nvidia-smi → ควรเห็น GPU

⚠️ หมายเหตุ:
- ต้องติดตั้ง Whisper ใหม่ (ไม่เก็บหลัง restart)
- โฟลเดอร์และไฟล์ยังอยู่ (ไม่เสีย)

STEP 4: ตรวจสอบ Device ก่อนถอดเสียง
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# รัน script → ดูบรรทัด "INFO: Device: ..."

python /notebooks/thai-whisper/scripts/whisper_transcribe.py video.mp4

✅ ถ้าเห็น:
INFO: Device: cuda
→ กำลังใช้ GPU ✓ → ปลอดภัย

❌ ถ้าเห็น:
INFO: Device: cpu
→ กำลังใช้ CPU ✗ → จะ Killed! → กลับไป STEP 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 สรุป: ทำไมต้องใช้ GPU?

Model Size    | CPU RAM | GPU VRAM | ผลลัพธ์
--------------|---------|----------|------------------
large-v3      | 8-16 GB | 16 GB    |
Load to CPU   | ❌ OOM  | -        | Killed (เมมอรี่เกิน)
Load to GPU   | 2 GB    | ✅ 6 GB  | ทำงานปกติ (เร็ว 10x)

💡 อธิบาย:
- Model 2.88 GB + Processing = ใช้ RAM ~10-12 GB (เกินที่มี)
- ใช้ GPU → Model โหลดใน VRAM 16 GB (เหลือเยอะ)
- GPU ประมวลผลเร็วกว่า CPU 10-20 เท่า

🔍 วิธีป้องกัน:
1. เช็ค GPU ก่อนเสมอ (STEP 7 ในคู่มือ)
2. ติดตั้ง PyTorch กับ CUDA support
3. ดู "Device: cuda" ใน log ก่อนเริ่มถอดเสียง
4. ถ้าเห็น "Device: cpu" → หยุดทันที → แก้ GPU

⚠️ ปัญหาที่มักเจอ:
- Paperspace notebook เปิดโหมด CPU (ไม่เลือก GPU)
- PyTorch ติดตั้งแบบ CPU-only (ไม่มี CUDA)
- GPU Driver ไม่ load (restart notebook แก้)

💡 Quick Check (ก่อนเริ่มทุกครั้ง):
# 3 คำสั่งนี้ต้องผ่านทั้งหมด:
nvidia-smi                           # ✅ เห็น GPU
python -c "import torch; print(torch.cuda.is_available())"  # ✅ True
python script.py | grep "Device:"    # ✅ Device: cuda
```

### ปัญหา 2: Upload ช้ามาก

```
❌ ปัญหา: Upload วิดีโอช้า > 1 ชั่วโมง (ผ่าน Jupyter UI)

✅ แก้:
- ใช้ Google Drive + gdown แทน (เร็วกว่า 10-20 เท่า!)
- ดูวิธีใน PART 4 → วิธี A
- หรือใช้ wget/curl ถ้ามี direct URL
```

### ปัญหา 2.1: gdown - Access Denied

```
❌ ปัญหา:
Access denied with the following error:
Cannot retrieve the public link of the file...

✅ แก้:
# ใช้ --fuzzy flag (วิธีที่ได้ผลดีที่สุด!)
gdown --fuzzy "https://drive.google.com/file/d/FILE_ID/view?usp=drive_link"

# หรือ อัพเดท gdown
pip install --upgrade gdown
gdown --fuzzy "YOUR_GOOGLE_DRIVE_LINK"

# หรือตรวจสอบ sharing settings:
Google Drive → คลิกขวาไฟล์ → Share → "Anyone with the link"
```

### ปัญหา 2.2: โฟลเดอร์หาไม่เจอ (cd: No such file or directory)

```
❌ ปัญหา:
cd ~/thai-whisper/videos/
bash: cd: /root/thai-whisper/videos/: No such file or directory

🔍 สาเหตุ:
ใน Paperspace, ~ (tilde) ชี้ไปที่ /root/ ไม่ใช่ /notebooks/
ดังนั้น ~/thai-whisper/ จริงๆ คือ /root/thai-whisper/ (ไม่มีโฟลเดอร์นี้!)

✅ แก้:
# 1. เช็คว่า ~ ชี้ไปที่ไหน
echo ~
# จะได้: /root  ← ไม่ใช่ /notebooks!

# 2. เช็ค path ปัจจุบัน
pwd
# เช่น: /notebooks/thai-whisper

# 3. ใช้ absolute path /notebooks/ (วิธีที่ดีที่สุด)
cd /notebooks/thai-whisper/videos/

# หรือใช้ relative path (ถ้าอยู่ใน /notebooks/thai-whisper/ แล้ว):
cd videos/

# 4. สำหรับคำสั่งอื่นๆ - ใช้ absolute path เสมอ
gdown FILE_ID -O /notebooks/thai-whisper/videos/video.mp4

💡 เคล็ดลับ:
- ใช้ /notebooks/ แทน ~/ เสมอใน Paperspace
- ถ้าไม่แน่ใจ → ใช้ pwd เช็คก่อน
```

### ปัญหา 2.2.1: find ~ ไม่เจออะไรเลย / ไม่แสดงผล

```
❌ ปัญหา:
find ~ -name "*.mp4" -type f
# ไม่แสดงผลอะไรเลย (blank) แต่รู้ว่ามีไฟล์!

🔍 สาเหตุ (เหมือนปัญหา 2.2):
~ ชี้ไป /root/ แต่ไฟล์อยู่ที่ /notebooks/
find ~ จึงค้นหาแต่ /root/ → ไม่เจอไฟล์

✅ แก้:
# วิธีที่ 1: ใช้ /notebooks แทน ~ (แนะนำ)
find /notebooks -name "*.mp4" -type f 2>/dev/null

# ควรเห็น:
# /notebooks/thai-whisper/videos/ep-02(061024).mp4

# วิธีที่ 2: ใช้ ls ถ้ารู้ path อยู่แล้ว (เร็วกว่า)
ls -lh /notebooks/thai-whisper/videos/*.mp4

# วิธีที่ 3: เช็คว่า ~ ชี้ไปที่ไหนจริงๆ
echo ~
# จะได้: /root  ← ต่างจาก /notebooks!

📋 สรุป:
Command                          | ทำงาน | เหตุผล
---------------------------------|-------|------------------------
find ~ -name "*.mp4"             | ❌    | ~ = /root/ (ไม่มีไฟล์)
find /notebooks -name "*.mp4"    | ✅    | absolute path ถูกต้อง
ls /notebooks/thai-whisper/videos/ | ✅  | ถ้ารู้ path (เร็วกว่า)
```

### ปัญหา 2.3: rclone - Failed to configure

```
❌ ปัญหา:
Failed to configure token: invalid token
หรือ authentication failed

✅ แก้:
# 1. ลบ config เก่า แล้ว config ใหม่
rclone config
d) Delete remote → เลือก gdrive → ลบ
q) Quit

# 2. Config ใหม่อีกครั้ง
rclone config
n) New remote → ทำตาม PART 4 → วิธี E.2

# 3. ตรวจสอบว่า token ยังใช้ได้
rclone lsd gdrive:
# ถ้าเห็นโฟลเดอร์ → OK
# ถ้า error → ทำ step 1-2 ใหม่
```

### ปัญหา 2.4: rclone - ช้ามาก / หยุดค้าง

```
❌ ปัญหา:
rclone copy ช้ามาก < 1 MB/s
หรือ progress หยุดค้าง

✅ แก้:
# 1. ใช้ --transfers flag (เพิ่มจำนวน connections)
rclone copy gdrive:/video.mp4 /notebooks/thai-whisper/videos/ \
  --progress \
  --transfers 8 \
  --checkers 16

# 2. ตรวจสอบ internet speed ของ Paperspace
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 -

# 3. หรือใช้ --bwlimit เพื่อจำกัดแบนด์วิธ (บางครั้งช่วยให้เสถียร)
rclone copy gdrive:/video.mp4 /notebooks/thai-whisper/videos/ \
  --progress \
  --bwlimit 10M
```

### ปัญหา 2.5: rclone - ไม่เห็นไฟล์ใน Drive

```
❌ ปัญหา:
rclone ls gdrive: ไม่แสดงไฟล์อะไรเลย
หรือไม่เห็นไฟล์บางไฟล์

✅ แก้:
# 1. ตรวจสอบว่าไฟล์อยู่ใน Google Drive จริงๆ
# เปิด drive.google.com ใน browser → ดูว่ามีไฟล์

# 2. ใช้ full path ถ้าไฟล์อยู่ในโฟลเดอร์
rclone ls "gdrive:/My Videos/"

# 3. List แบบ recursive (ดูทุกโฟลเดอร์ย่อย)
rclone ls gdrive: --recursive

# 4. ถ้ายังไม่เห็น → ตรวจสอบ scope ตอน config
rclone config
e) Edit existing remote → gdrive
scope> 1  # ต้องเป็น "Full access"
```

### ปัญหา 3: Out of Memory

```
❌ ปัญหา: CUDA out of memory

✅ แก้:
1. รีสตาร์ท Kernel:
   Kernel → Restart Kernel

2. หรือใช้ CPU mode:
   # แก้ใน script บรรทัด 47:
   device = "cpu"  # แทน "cuda"

   (ช้ากว่า แต่ใช้ได้)
```

### ปัญหา 4: Script error - No module named 'whisper'

```
❌ ปัญหา:
python /notebooks/thai-whisper/scripts/whisper_transcribe.py video.mp4
ERROR: Missing dependency: No module named 'whisper'
ERROR: Install: pip install openai-whisper torch

🔍 สาเหตุ:
Whisper ยังไม่ได้ติดตั้งใน Paperspace Notebook นี้

💡 ทำไมถึงเกิด?
- Paperspace ไม่เก็บ packages ไว้ถาวร
- ทุกครั้งที่เปิด notebook ใหม่ → ต้องติดตั้งใหม่
- หรือข้าม PART 2 ไป

🤔 งง? ทำไมต้องติดตั้งใหม่?
Q: "แต่ฉันสร้างโฟลเดอร์ /notebooks/thai-whisper/ แล้วนะ?"
A: โฟลเดอร์ ≠ Python packages!

   การสร้างโฟลเดอร์:
   mkdir /notebooks/thai-whisper/  ← สร้างที่เก็บไฟล์

   การติดตั้ง package:
   pip install openai-whisper  ← ติดตั้ง Python library
   → ติดตั้งที่: /usr/local/lib/python3.x/site-packages/
   → ไม่ได้อยู่ในโฟลเดอร์โปรเจค

✅ แก้:
# ติดตั้ง Whisper ใน Paperspace Terminal
# (ไม่ว่าจะ cd อยู่ที่ไหนก็ได้ - ติดตั้งทั้ง system)
pip install -U openai-whisper torch

# รอ 30-60 วินาที แล้วทดสอบ:
python -c "import whisper; print('✅ Whisper OK')"

# ถ้าใช้ครั้งแรก ต้อง download model ด้วย (3-5 นาที):
python << 'EOF'
import whisper
print("⏳ Downloading large-v3...")
model = whisper.load_model("large-v3")
print("✅ Done!")
EOF

📍 หมายเหตุ:
- ติดตั้งที่: Paperspace Terminal (ไม่ใช่เครื่องของคุณ!)
- ติดตั้งระดับ: Python system packages (ใช้ได้ทุก directory)
- ไม่ได้ติดตั้งใน: /notebooks/thai-whisper/ (ไม่ใช่ในโฟลเดอร์โปรเจค)
- กลับไปดู: PART 2 - ติดตั้ง Whisper (STEP 8-10)
```

### ปัญหา 5: ไฟล์หาไม่เจอ - FileNotFoundError

```
❌ ปัญหา:
FileNotFoundError: [Errno 2] No such file or directory:
'/notebooks/thai-whisper/videos/video.mp4'

✅ แก้:
# หา path ที่ถูกต้อง (ใช้ /notebooks ไม่ใช่ ~)
find /notebooks -name "*.mp4" -type f 2>/dev/null

# หรือใช้ ls ถ้ารู้โฟลเดอร์:
ls -lh /notebooks/thai-whisper/videos/

# ใช้ path ที่ได้จาก command ข้างบน
# หมายเหตุ: ถ้าชื่อไฟล์มีวงเล็บ/ช่องว่าง ใส่ " " ด้วย
python script.py "/notebooks/thai-whisper/videos/ep-02(061024).mp4"

💡 เคล็ดลับ:
- ดู STEP 15 วิธีหา path ของวิดีโอ
- อย่าใช้ ~ (จะชี้ไป /root/ ไม่ใช่ /notebooks/)
```

---

## 📋 Checklist

### ก่อนเริ่ม:

- [ ] Paperspace account พร้อม
- [ ] Growth Plan ($8/month) subscribe แล้ว
- [ ] Notebook เปิดอยู่ (RTX A4000)
- [ ] วิดีโอพร้อม upload

### หลังเสร็จ:

- [ ] Download transcript JSON แล้ว
- [ ] เก็บไฟล์หลายที่ (backup)
- [ ] **ปิด Notebook** ← อย่าลืม!
- [ ] ลบวิดีโอออกจาก Paperspace (ถ้าไม่ต้องการแล้ว)

---

## 🎯 เปรียบเทียบ: Paperspace vs Kaggle

| ฟีเจอร์ | **Paperspace** | **Kaggle** |
|---------|---------------|-----------|
| **ค่าใช้จ่าย** | $0.15/video (RTX A4000) | **ฟรี $0** |
| **GPU** | RTX A4000 (16GB) | P100/T4 (16GB) |
| **ความเร็ว** | ⭐⭐⭐⭐ (10-20x) | ⭐⭐⭐⭐ (15-20x P100) |
| **Setup** | กลาง | ง่าย |
| **Timeout** | ไม่มี (แต่คิดเงิน) | 9h/12h |
| **Storage** | 200 GB ถาวร | ชั่วคราว |
| **เหมาะสำหรับ** | มีงบ, ต้องการ storage | ทดลอง, ไม่มีงบ |

**คำแนะนำ:**
- 🧪 **ทดลอง/เรียนรู้** → ใช้ Kaggle (ฟรี)
- 💼 **ใช้จริงบ่อยๆ** → ใช้ Paperspace (มี storage ถาวร)
- 🚀 **ต้องการเร็ว** → ทั้ง 2 อันเร็วพอๆ กัน

---

## 📚 เอกสารเพิ่มเติม

### ในโปรเจคนี้:

- **PAPERSPACE_WHISPER_GUIDE.md** - คู่มือละเอียด (advanced topics)
- **CLAUDE.md** - คู่มือหลักของโปรเจค
- **kaggle/README_KAGGLE.md** - สำหรับ Kaggle workflow
- **workflow/README.md** - การใช้ transcript ต่อ

### External:

- **Paperspace Docs**: https://docs.paperspace.com/gradient/
- **Whisper Docs**: https://github.com/openai/whisper
- **FFmpeg Guide**: https://ffmpeg.org/documentation.html

---

## ✅ Success Checklist

**โปรเจคสำเร็จเมื่อ:**

- [x] สร้างโฟลเดอร์ครบ 3 โฟลเดอร์
- [x] ติดตั้ง Whisper สำเร็จ
- [x] Download model large-v3 แล้ว
- [x] สร้าง script เรียบร้อย
- [x] Upload วิดีโอสำเร็จ
- [x] Transcribe ได้ (accuracy > 95%)
- [x] Download transcript JSON
- [x] ใช้ transcript ได้จริง
- [x] **ปิด Notebook เพื่อประหยัดเงิน**

---

## 🎉 ยินดีด้วย!

**คุณถอดเสียงวิดีโอภาษาไทยสำเร็จแล้ว!**

**ขั้นตอนถัดไป:**
1. ใช้ transcript กับ video-translater project
2. แปลเป็นภาษาอังกฤษด้วย Claude Code
3. สร้าง SRT ไฟล์
4. ได้ English subtitles พร้อมใช้!

---

**Created**: 2025-10-07
**Updated**: 2025-10-07
**Version**: 3.7 - Added Terminal vs Notebook explanation
**Author**: Claude Code
**Project**: Thai Video Translator - Paperspace Simple Guide
**Status**: ✅ Production Ready

**📝 Changelog:**

**v3.7 (2025-10-07):**
- 🤔 **Terminal vs Notebook Section**: ใหม่ - อธิบายความแตกต่างชัดเจน
  - 📊 Diagram: Paperspace Jupyter Lab มี 3 ส่วน (UI, Terminal, Notebook)
  - ✅ ตารางสรุป: คู่มือนี้ใช้อะไรบ้าง (แต่ละ PART)
  - 🎯 ชี้แจง: ใช้ Terminal เป็นหลัก + Jupyter UI (file manager)
  - ❌ ไม่ใช้ Notebook (.ipynb) เลย!
  - 📋 ตารางเปรียบเทียบ: Terminal vs Notebook (8 aspects)
  - ⚡ **ประสิทธิภาพเหมือนกัน!** - ทั้งสองใช้ GPU เดียวกัน
  - 🎯 เหตุผล 4 ข้อ: ทำไมใช้ Terminal (long tasks, production, copy-paste, timeout)
  - 💡 วิธีใช้ Notebook แทน: เพิ่ม `!` หรือ `%%bash`
  - 📋 Q&A: ตอบคำถาม 5 ข้อ (Terminal หมดเลย? ประสิทธิภาพต่างมั้ย?)

**v3.6 (2025-10-07):**
- 🎮 **GPU Comparison Section**: ใหม่ - เปรียบเทียบ GPU หลายรุ่น
  - 📊 ตารางเปรียบเทียบ: RTX 5000 Ada, RTX 4000 Ada, RTX A4000, P5000, P4000
  - ⏱️ เวลาถอดเสียง: วิดีโอ 1 ชม. ใช้เวลากี่นาที (แต่ละ GPU)
  - 💰 ค่าใช้จ่าย: ประมาณการจาก Paperspace pricing
  - 🎯 คำแนะนำ: GPU ไหนเหมาะกับใคร (มือใหม่, ใช้บ่อย, งบน้อย)
  - 🆓 **กรณีใช้ฟรี**: ถ้า Growth Plan ให้ใช้ฟรีทุกตัว → เลือกเร็วที่สุด (RTX 5000 Ada)
  - 💰 **กรณีจ่ายเพิ่ม**: ถ้าต้องจ่ายต่อชั่วโมง → เลือกคุ้มค่า (RTX 4000 Ada / RTX A4000)
  - 🔍 **วิธีเช็ค**: ดู "Included" vs "$X.XX/hr" ใน Dashboard
  - ⚠️ คำเตือน: P4000 (8GB VRAM) อาจไม่พอสำหรับ large-v3
  - 💡 วิธีเปลี่ยน GPU ใน Paperspace
  - 📋 ตารางคุ้มค่า: เปรียบเทียบ 2 กรณี (ฟรี vs จ่ายเพิ่ม)
  - 🏆 Quick Decision Guide: ตัดสินใจเร็วตามสถานการณ์

**v3.5 (2025-10-07):**
- 🔥 **STEP 7 Enhanced**: เพิ่มเน้นความสำคัญของ GPU check
  - ⚠️ คำเตือน: ไม่มี GPU → "Killed" (OOM)
  - 💡 Double-check: เพิ่ม PyTorch CUDA detection
  - 🚨 Clear consequences: ไม่มี GPU = ไม่สามารถทำงานได้
- 🆕 **Troubleshooting 1.6**: ใหม่ - "Killed" Error (Out of Memory)
  - 🔍 Root cause: ใช้ CPU แทน GPU (Model ใหญ่เกิน RAM)
  - ✅ 4 STEPs แก้: nvidia-smi → PyTorch check → Restart → Verify
  - 📋 ตารางเปรียบเทียบ: CPU vs GPU memory usage
  - 💡 Quick Check: 3 คำสั่งที่ต้องผ่านก่อนเริ่ม
  - ⚠️ ปัญหาที่พบบ่อย + วิธีป้องกัน
- 📍 **STEP 8 Clarification**: pip install path - ตอบคำถาม "ติดตั้งที่ระดับไหน?"
  - 🎯 FAQ: ต้อง cd ไปโฟลเดอร์ไหนก่อน pip install?
  - ✅ คำตอบ: ที่ไหนก็ได้! (system-wide installation)
  - 📋 ตัวอย่าง: รันจาก 3 paths ต่างกัน → ผลเหมือนกัน
  - 💡 อธิบาย: Terminal prompt vs pip install location
  - ⚠️ แยกแยะ: pip vs python script.py (ต่างกัน!)
- 💡 **STEP 16 Enhancement**: วิธีป้องกัน Copy/Paste ผิด (ใหม่!)
  - 🎯 4 วิธี: ตัวแปร, หาอัตโนมัติ, Tab completion, Wildcard
  - ✅ แก้ปัญหา: path copy ไม่ครบ → ขาด /notebooks
  - 📋 ตารางเปรียบเทียบ: ความง่าย vs ความปลอดภัย
  - 🏆 แนะนำ: วิธีที่ 2 (หาอัตโนมัติ) สำหรับมือใหม่
- 📚 **STEP 16 Enhancement**: Absolute Path vs Relative Path (ใหม่!)
  - 🔍 อธิบายความแตกต่าง: `/notebooks/` vs `./`
  - 📋 ตารางเปรียบเทียบ: absolute vs relative path
  - 💡 ตัวอย่างชัดเจน: pwd = /notebooks vs /root
  - 🎯 แนะนำ: ใช้ absolute path สำหรับมือใหม่ (ปลอดภัย)

**v3.4 (2025-10-07):**
- ➕ Troubleshooting 1.5: ใหม่ - Server Connection Error
  - 🔍 อธิบายสาเหตุ: timeout, internet, idle
  - ✅ 3 วิธีแก้: Refresh → Check Status → Restart
  - 📋 ตารางสรุป: ต้องทำใหม่อะไรบ้าง (แต่ละ PART)
  - 💡 เคล็ดลับป้องกัน
- 💾 ชี้แจง: โฟลเดอร์/ไฟล์ไม่เสีย (persistent) แต่ packages เสีย

**v3.3 (2025-10-07):**
- 📍 PART 1: เพิ่มคำชี้แจง "ทำใน Paperspace ไม่ใช่เครื่องตัวเอง"
- 📍 PART 2 (STEP 8): ชี้แจงชัดเจน "ติดตั้งใน Paperspace Terminal"
  - 🔍 เพิ่มอธิบาย: `pip install` ติดตั้งที่ระดับไหน (path level)
  - 💡 อธิบายความแตกต่าง: โฟลเดอร์ vs Python packages
  - 📊 ตาราง: `/notebooks/thai-whisper/` (โฟลเดอร์) ≠ `pip install` (system packages)
- 📍 PART 7 (STEP 20): ชี้แจงชัดเจน "ทำในเครื่องตัวเอง (Local)"
- 🔧 Troubleshooting 4: เพิ่มรายละเอียดว่าทำไมต้องติดตั้ง Whisper ใหม่
  - 🤔 เพิ่ม Q&A: "ทำไมสร้างโฟลเดอร์แล้วยังต้องติดตั้ง?"
  - 📍 ระบุชัดเจน: ติดตั้งที่ `/usr/local/lib/python3.x/site-packages/`
- 🔧 Troubleshooting 5: แก้ไข `find ~` → `find /notebooks`
- 💡 เพิ่มคำอธิบาย: ~ ใช้ได้ใน Local แต่ไม่ได้ใน Paperspace

**v3.2 (2025-10-07):**
- 🐛 แก้ไขปัญหา `~` ชี้ไป `/root/` แทน `/notebooks/`
- 🔧 STEP 15: เปลี่ยน `find ~` → `find /notebooks` + เพิ่ม 2 วิธี
- 🔧 STEP 16: ลบตัวอย่างที่ใช้ `~/` + เพิ่มคำเตือน
- ➕ Troubleshooting 2.2: เพิ่มคำอธิบาย root cause + วิธีเช็ค `echo ~`
- ➕ Troubleshooting 2.2.1: ใหม่ - แก้ `find ~` ไม่เจออะไร
- ⚠️ Tips 3.5: ใหม่ - คำเตือน "ระวัง ~ ใน Paperspace!"
- 📊 เพิ่มตารางเปรียบเทียบคำสั่ง (ถูก/ผิด)

**v3.1 (2025-10-07):**
- ➕ เพิ่มวิธี E: rclone (สำหรับไฟล์ใหญ่/ใช้บ่อย)
- ➕ Troubleshooting สำหรับ rclone (5 ปัญหาหลัก)
- ➕ Tips: เมื่อไหร่ควรใช้ rclone vs gdown
- 🔧 อัพเดทตารางเปรียบเทียบ (เพิ่ม Resume column)
- 📊 อัพเดทต้นทุน + เวลา (แม่นยำจากการใช้งานจริง)

---

**Happy Transcribing! 🚀**

*Paperspace + Whisper + rclone/gdown + Claude Code = Perfect Thai Video Translation*
