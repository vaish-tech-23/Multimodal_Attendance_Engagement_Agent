import sqlite3
from datetime import datetime, date, timedelta
from config import Config

def get_db_connection():
    """Create and return a thread-safe connection to the SQLite database."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables for participants, attendance, engagement, and AI suggestions."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Participants / Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            email TEXT,
            department TEXT DEFAULT 'Computer Science',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Attendance records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER NOT NULL,
            session_date DATE NOT NULL,
            first_seen TEXT,
            last_seen TEXT,
            total_duration_minutes INTEGER DEFAULT 50,
            status TEXT CHECK(status IN ('Present', 'Absent', 'Late')) DEFAULT 'Present',
            sustained_presence TEXT DEFAULT 'Verified (45m+)',
            FOREIGN KEY (participant_id) REFERENCES participants (id) ON DELETE CASCADE,
            UNIQUE(participant_id, session_date)
        )
    ''')

    # 3. Engagement logs table (Demo & simulated vision/audio metrics)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS engagement_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            participant_id INTEGER NOT NULL,
            session_date DATE NOT NULL,
            head_pose TEXT DEFAULT 'Attentive (Forward)',
            movement_level TEXT DEFAULT 'Normal',
            inactivity_flag INTEGER DEFAULT 0,
            audio_activity TEXT DEFAULT 'Moderate',
            engagement_score INTEGER NOT NULL,
            attention_status TEXT DEFAULT 'High',
            FOREIGN KEY (participant_id) REFERENCES participants (id) ON DELETE CASCADE
        )
    ''')

    # 4. AI Teaching Suggestions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rule_name TEXT NOT NULL,
            suggestion_type TEXT NOT NULL,
            message TEXT NOT NULL,
            severity TEXT DEFAULT 'info'
        )
    ''')

    conn.commit()
    seed_demo_data(conn)
    conn.close()

def seed_demo_data(conn):
    """Seed realistic initial data so the application is immediately presentable."""
    cursor = conn.cursor()

    # Check if participants already exist
    cursor.execute("SELECT COUNT(*) FROM participants")
    if cursor.fetchone()[0] > 0:
        return  # Already seeded

    # Seed 8 realistic student profiles
    initial_students = [
        ("Aarav Sharma", "CS-2024-001", "aarav.sharma@campus.edu", "Artificial Intelligence"),
        ("Priya Patel", "CS-2024-002", "priya.patel@campus.edu", "Data Science"),
        ("Rohan Mehta", "CS-2024-003", "rohan.mehta@campus.edu", "Computer Science"),
        ("Ananya Iyer", "CS-2024-004", "ananya.iyer@campus.edu", "Artificial Intelligence"),
        ("Vikram Singh", "CS-2024-005", "vikram.singh@campus.edu", "Information Technology"),
        ("Sneha Reddy", "CS-2024-006", "sneha.reddy@campus.edu", "Computer Science"),
        ("Arjun Nair", "CS-2024-007", "arjun.nair@campus.edu", "Data Science"),
        ("Kavya Joshi", "CS-2024-008", "kavya.joshi@campus.edu", "Information Technology"),
    ]

    cursor.executemany(
        "INSERT INTO participants (name, roll_no, email, department) VALUES (?, ?, ?, ?)",
        initial_students
    )

    today = date.today()
    dates = [today - timedelta(days=i) for i in range(3, -1, -1)]

    # Demo status assignments for past and today
    # (Student Index, Day Index) -> (Status, Duration, Engagement Score, Head Pose, Movement)
    sample_engagement = [
        (1, 92, "Attentive (Forward)", "Optimal", 0, "High"),
        (2, 88, "Attentive (Forward)", "Normal", 0, "High"),
        (3, 54, "Looking Down", "Inactive", 1, "Needs Attention"),
        (4, 95, "Attentive (Forward)", "Normal", 0, "High"),
        (5, 76, "Looking Left/Right", "Normal", 0, "Moderate"),
        (6, 84, "Attentive (Forward)", "Normal", 0, "High"),
        (7, 48, "Looking Down (Phone)", "Very Low", 1, "Needs Attention"),
        (8, 91, "Attentive (Forward)", "Optimal", 0, "High"),
    ]

    for d_idx, d in enumerate(dates):
        d_str = d.isoformat()
        for s_idx, (p_id, score, head, mov, inact, att) in enumerate(sample_engagement, start=1):
            # Vary status slightly across days
            if s_idx in [3, 7] and d_idx == 2:
                status = "Absent"
                first_seen, last_seen, duration, pres = None, None, 0, "Not Detected"
            elif s_idx == 5 and d_idx == 3:
                status = "Late"
                first_seen = f"{d_str} 09:18:00"
                last_seen = f"{d_str} 10:00:00"
                duration = 42
                pres = "Partial Presence"
            else:
                status = "Present"
                first_seen = f"{d_str} 09:02:15"
                last_seen = f"{d_str} 10:00:00"
                duration = 58
                pres = "Verified (45m+)"

            cursor.execute('''
                INSERT OR IGNORE INTO attendance_records 
                (participant_id, session_date, first_seen, last_seen, total_duration_minutes, status, sustained_presence)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (p_id, d_str, first_seen, last_seen, duration, status, pres))

            # Add today's engagement metrics
            if d == today:
                cursor.execute('''
                    INSERT INTO engagement_logs 
                    (participant_id, session_date, head_pose, movement_level, inactivity_flag, engagement_score, attention_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (p_id, d_str, head, mov, inact, score, att))

    # Seed AI teaching suggestions
    initial_suggestions = [
        ("Engagement Rule #1", "Engagement Warning", 
         "Classroom engagement dropped around 09:35 AM (avg 68%). Consider introducing a 2-minute peer discussion or quick poll to re-focus students.", "warning"),
        ("Presence Rule #2", "Punctuality Alert", 
         "1 student arrived more than 15 minutes late today. Review session start cues and recap key initial objectives.", "info"),
        ("Sustained Focus Rule #3", "Teaching Optimization", 
         "High engagement (90%+) observed during the live problem-solving segment. Students respond strongly to hands-on visual walkthroughs.", "success"),
        ("Inactivity Rule #4", "Passive Posture Detected", 
         "Two participants (Rohan Mehta, Arjun Nair) showed prolonged static gaze/head-down posture. Prompt for direct vocal participation.", "warning")
    ]

    for rule, stype, msg, sev in initial_suggestions:
        cursor.execute(
            "INSERT INTO ai_suggestions (rule_name, suggestion_type, message, severity) VALUES (?, ?, ?, ?)",
            (rule, stype, msg, sev)
        )

    conn.commit()

# --- Helper Query Functions for Application Views ---

def get_dashboard_stats():
    """Retrieve summarized statistics for the dashboard."""
    conn = get_db_connection()
    today_str = date.today().isoformat()

    total_students = conn.execute("SELECT COUNT(*) FROM participants").fetchone()[0]

    # Today's attendance stats
    today_records = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM attendance_records WHERE session_date = ? GROUP BY status",
        (today_str,)
    ).fetchall()

    status_counts = {"Present": 0, "Absent": 0, "Late": 0}
    for row in today_records:
        status_counts[row["status"]] = row["cnt"]

    total_marked = sum(status_counts.values())
    present_total = status_counts["Present"] + status_counts["Late"]
    attendance_rate = round((present_total / total_students * 100), 1) if total_students > 0 else 0

    # Today's average engagement
    avg_eng = conn.execute(
        "SELECT AVG(engagement_score) FROM engagement_logs WHERE session_date = ?",
        (today_str,)
    ).fetchone()[0]
    avg_engagement = round(avg_eng, 1) if avg_eng else 78.5

    # Recent AI suggestions (top 3)
    recent_suggestions = conn.execute(
        "SELECT * FROM ai_suggestions ORDER BY timestamp DESC LIMIT 3"
    ).fetchall()

    conn.close()
    return {
        "total_students": total_students,
        "present_count": status_counts["Present"],
        "absent_count": status_counts["Absent"],
        "late_count": status_counts["Late"],
        "attendance_rate": attendance_rate,
        "avg_engagement": avg_engagement,
        "today_date": today_str,
        "recent_suggestions": recent_suggestions
    }

def get_today_attendance_list():
    """Fetch all students and their attendance status for today."""
    conn = get_db_connection()
    today_str = date.today().isoformat()

    query = '''
        SELECT 
            p.id, p.name, p.roll_no, p.department,
            COALESCE(a.status, 'Absent') AS status,
            a.first_seen, a.last_seen, a.total_duration_minutes, a.sustained_presence
        FROM participants p
        LEFT JOIN attendance_records a 
            ON p.id = a.participant_id AND a.session_date = ?
        ORDER BY p.roll_no ASC
    '''
    records = conn.execute(query, (today_str,)).fetchall()
    conn.close()
    return records

def mark_student_attendance(participant_id, new_status):
    """Update or insert attendance status for a student for today."""
    conn = get_db_connection()
    today_str = date.today().isoformat()
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    duration = 55 if new_status == "Present" else (30 if new_status == "Late" else 0)
    pres = "Verified (45m+)" if new_status == "Present" else ("Partial" if new_status == "Late" else "Not Detected")
    first = now_time if new_status in ["Present", "Late"] else None
    last = now_time if new_status in ["Present", "Late"] else None

    conn.execute('''
        INSERT INTO attendance_records 
            (participant_id, session_date, first_seen, last_seen, total_duration_minutes, status, sustained_presence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(participant_id, session_date) DO UPDATE SET
            status = excluded.status,
            total_duration_minutes = excluded.total_duration_minutes,
            sustained_presence = excluded.sustained_presence,
            last_seen = excluded.last_seen
    ''', (participant_id, today_str, first, last, duration, new_status, pres))

    conn.commit()
    conn.close()

def add_new_student(name, roll_no, email, department):
    """Add a new student participant and auto-register attendance for today."""
    conn = get_db_connection()
    today_str = date.today().isoformat()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO participants (name, roll_no, email, department) VALUES (?, ?, ?, ?)",
            (name.strip(), roll_no.strip(), email.strip() if email else None, department.strip())
        )
        new_id = cursor.lastrowid
        # Default attendance to Present upon onboarding
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO attendance_records 
            (participant_id, session_date, first_seen, last_seen, total_duration_minutes, status, sustained_presence)
            VALUES (?, ?, ?, ?, 50, 'Present', 'Verified (45m+)')
        ''', (new_id, today_str, now_time, now_time))

        # Demo engagement score for newly added student
        cursor.execute('''
            INSERT INTO engagement_logs 
            (participant_id, session_date, head_pose, movement_level, inactivity_flag, engagement_score, attention_status)
            VALUES (?, ?, 'Attentive (Forward)', 'Normal', 0, 85, 'High')
        ''', (new_id, today_str))

        conn.commit()
        return True, "Student added successfully."
    except sqlite3.IntegrityError:
        return False, f"Roll Number '{roll_no}' already exists in the system."
    finally:
        conn.close()

def get_engagement_records():
    """Retrieve engagement metrics for participants."""
    conn = get_db_connection()
    today_str = date.today().isoformat()
    query = '''
        SELECT 
            p.name, p.roll_no, p.department,
            e.head_pose, e.movement_level, e.inactivity_flag, 
            e.engagement_score, e.attention_status
        FROM participants p
        JOIN engagement_logs e ON p.id = e.participant_id
        WHERE e.session_date = ?
        ORDER BY e.engagement_score DESC
    '''
    rows = conn.execute(query, (today_str,)).fetchall()
    conn.close()
    return rows

def generate_ai_suggestions_from_rules():
    """Evaluate current attendance and engagement metrics against rule heuristics."""
    stats = get_dashboard_stats()
    conn = get_db_connection()
    new_suggestions = []

    # Rule 1: Attendance threshold check
    if stats["attendance_rate"] < 75.0:
        new_suggestions.append((
            "Rule #1 - Attendance Deficit", "Attendance Alert",
            f"Attendance rate is currently {stats['attendance_rate']}%. Share meeting recordings and lecture slides to help absent students catch up.",
            "warning"
        ))
    else:
        new_suggestions.append((
            "Rule #1 - Punctuality Healthy", "Attendance Status",
            f"Strong attendance today ({stats['attendance_rate']}%). All registered core group members are present.",
            "success"
        ))

    # Rule 2: Engagement score check
    if stats["avg_engagement"] < 70.0:
        new_suggestions.append((
            "Rule #2 - Engagement Dip", "Pedagogical Tip",
            f"Classroom attention index is {stats['avg_engagement']}%. Insert a 3-minute interactive question-and-answer or group challenge now.",
            "warning"
        ))
    else:
        new_suggestions.append((
            "Rule #2 - High Attention", "Optimal Focus Zone",
            f"Attention is high ({stats['avg_engagement']}%). Recommended time to deliver challenging, high-depth course concepts.",
            "success"
        ))

    # Rule 3: Dynamic Inactivity check
    inactivity_count = conn.execute(
        "SELECT COUNT(*) FROM engagement_logs WHERE inactivity_flag = 1 AND session_date = ?",
        (stats["today_date"],)
    ).fetchone()[0]

    if inactivity_count > 0:
        new_suggestions.append((
            "Rule #3 - Inactivity Heuristic", "Participation Prompt",
            f"{inactivity_count} student(s) currently display prolonged head-down or low movement patterns. Consider a cold-call question or group check-in.",
            "info"
        ))

    for rule, stype, msg, sev in new_suggestions:
        conn.execute(
            "INSERT INTO ai_suggestions (rule_name, suggestion_type, message, severity) VALUES (?, ?, ?, ?)",
            (rule, stype, msg, sev)
        )

    conn.commit()
    conn.close()

def get_all_suggestions():
    """Retrieve all AI suggestions ordered by most recent."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM ai_suggestions ORDER BY timestamp DESC").fetchall()
    conn.close()
    return rows

def get_attendance_history(date_filter=None):
    """Retrieve full attendance history, optionally filtered by date."""
    conn = get_db_connection()
    if date_filter:
        query = '''
            SELECT 
                a.session_date, p.name, p.roll_no, p.department,
                a.status, a.first_seen, a.last_seen, a.total_duration_minutes, a.sustained_presence
            FROM attendance_records a
            JOIN participants p ON a.participant_id = p.id
            WHERE a.session_date = ?
            ORDER BY a.session_date DESC, p.roll_no ASC
        '''
        rows = conn.execute(query, (date_filter,)).fetchall()
    else:
        query = '''
            SELECT 
                a.session_date, p.name, p.roll_no, p.department,
                a.status, a.first_seen, a.last_seen, a.total_duration_minutes, a.sustained_presence
            FROM attendance_records a
            JOIN participants p ON a.participant_id = p.id
            ORDER BY a.session_date DESC, p.roll_no ASC
        '''
        rows = conn.execute(query).fetchall()
    conn.close()
    return rows
