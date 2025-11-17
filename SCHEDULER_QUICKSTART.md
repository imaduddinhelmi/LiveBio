# ⚡ Quick Start: Automatic Batch Scheduler

## 5-Minute Setup Guide

### Prerequisites ✅
- [x] Authenticated YouTube account
- [x] Excel file loaded in "Import & Run" tab
- [x] Application running

### Quick Steps

#### 1️⃣ Navigate to Import & Run Tab
```
Open application → Click "Import & Run" tab
```

#### 2️⃣ Load Your Excel File
```
Click "Select Excel File" → Choose your broadcasts file → Preview loaded
```

#### 3️⃣ Configure Scheduler
```
Look at the RIGHT PANEL (blue colored)
Find "⏰ Automatic Daily Scheduling" section
Set time → Example: 09:00 (9 AM)
```

#### 4️⃣ Enable Scheduler
```
Click "▶ Enable Scheduler" button
Confirm the popup → Done! ✅
```

### Status Indicators

| Icon | Status | Meaning |
|------|--------|---------|
| 🟢 | Active | Scheduler is running |
| 🟡 | Configured | Set but not started |
| ⚪ | Disabled | Not active |

### Example: Daily 9 AM Upload

```
Settings:
├─ Daily Run Time: 09:00
├─ Excel File: my_broadcasts.xlsx
├─ Base Time: +30 min
├─ Interval: 0 min (all same)
└─ Result: Broadcasts created at 9 AM, scheduled for 9:30 AM
```

### Common Commands

| Action | How To |
|--------|--------|
| Enable | Click "▶ Enable Scheduler" |
| Disable | Click "⏸ Disable Scheduler" |
| Change Time | Update time → Click "🔄 Update Time" |
| Check Status | Look at status indicator |
| View Logs | Go to "Logs" tab |

### Tips for Success 💡

1. **Test First**
   - Run "Process Batch" manually once
   - Verify everything works correctly

2. **Keep Running**
   - Don't close the application
   - Prevent computer sleep/hibernate

3. **Monitor Logs**
   - Check "Logs" tab after scheduled run
   - Verify success/error messages

4. **Update Excel**
   - Update Excel file anytime
   - Scheduler will reload automatically

### Time Format Examples

| Input | Execution Time |
|-------|----------------|
| 09:00 | 9:00 AM |
| 14:30 | 2:30 PM |
| 18:00 | 6:00 PM |
| 23:45 | 11:45 PM |

### Troubleshooting Quick Fix

**Problem**: Scheduler not working?

**Solution**:
```
1. Check: Is app running? ✅
2. Check: Is status "🟢 Active"? ✅
3. Check: Is Excel file still there? ✅
4. Check: Still logged in to YouTube? ✅
```

**Still not working?**
- See detailed guide: SCHEDULER_GUIDE.md
- Check logs in "Logs" tab
- Restart application

### Next Steps
- Read full guide: [SCHEDULER_GUIDE.md](SCHEDULER_GUIDE.md)
- Explore advanced settings in Import & Run tab
- Set up PM2 for 24/7 running (optional): [PM2_SETUP_GUIDE.md](PM2_SETUP_GUIDE.md)

---

**Need Help?** Check [SCHEDULER_GUIDE.md](SCHEDULER_GUIDE.md) for detailed documentation
