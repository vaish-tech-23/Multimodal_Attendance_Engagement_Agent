import io
import csv
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from config import Config
from database import (
    init_db,
    get_dashboard_stats,
    get_today_attendance_list,
    mark_student_attendance,
    add_new_student,
    get_engagement_records,
    get_all_suggestions,
    generate_ai_suggestions_from_rules,
    get_attendance_history
)

def create_app():
    """Application factory for Multimodal Attendance & Engagement Agent."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database and seed realistic demo data on startup
    init_db()

    @app.route("/")
    def index():
        """Main dashboard view with summary cards, metrics, and quick actions."""
        stats = get_dashboard_stats()
        return render_template("index.html", stats=stats)

    @app.route("/attendance")
    def attendance():
        """Attendance management view for listing students and toggling status."""
        students = get_today_attendance_list()
        stats = get_dashboard_stats()
        return render_template("attendance.html", students=students, stats=stats)

    @app.route("/attendance/mark", methods=["POST"])
    def mark_attendance():
        """Handle updating a student's attendance status."""
        participant_id = request.form.get("participant_id")
        status = request.form.get("status")

        if participant_id and status in ["Present", "Absent", "Late"]:
            mark_student_attendance(int(participant_id), status)
            flash(f"Status updated to '{status}'.", "success")
        else:
            flash("Invalid attendance update request.", "danger")

        return redirect(url_for("attendance"))

    @app.route("/students/add", methods=["POST"])
    def add_student():
        """Handle registering a new student in the system."""
        name = request.form.get("name")
        roll_no = request.form.get("roll_no")
        email = request.form.get("email")
        department = request.form.get("department") or "Computer Science"

        if not name or not roll_no:
            flash("Student Name and Roll Number are required.", "danger")
            return redirect(url_for("attendance"))

        success, message = add_new_student(name, roll_no, email, department)
        if success:
            flash(message, "success")
        else:
            flash(message, "danger")

        return redirect(url_for("attendance"))

    @app.route("/engagement")
    def engagement():
        """Multimodal engagement view displaying head pose, movement, and attention levels."""
        records = get_engagement_records()
        stats = get_dashboard_stats()
        return render_template("engagement.html", records=records, stats=stats)

    @app.route("/suggestions")
    def suggestions():
        """AI Teaching Suggestions view driven by rule heuristics."""
        all_suggestions = get_all_suggestions()
        stats = get_dashboard_stats()
        return render_template("suggestions.html", suggestions=all_suggestions, stats=stats)

    @app.route("/suggestions/refresh", methods=["POST"])
    def refresh_suggestions():
        """Trigger rule heuristic re-evaluation based on current classroom metrics."""
        generate_ai_suggestions_from_rules()
        flash("AI rules evaluated against current session metrics. New insights generated!", "info")
        return redirect(url_for("suggestions"))

    @app.route("/reports")
    def reports():
        """Historical attendance reports view with date filtering."""
        selected_date = request.args.get("date") or ""
        history = get_attendance_history(selected_date if selected_date else None)
        return render_template("reports.html", history=history, selected_date=selected_date)

    @app.route("/reports/download")
    def download_csv():
        """Generate and stream a downloadable CSV report of attendance history."""
        selected_date = request.args.get("date") or None
        records = get_attendance_history(selected_date)

        output = io.StringIO()
        writer = csv.writer(output)

        # Write CSV header
        writer.writerow([
            "Session Date", 
            "Student Name", 
            "Roll Number", 
            "Department", 
            "Attendance Status", 
            "First Seen", 
            "Last Seen", 
            "Duration (Minutes)", 
            "Sustained Presence"
        ])

        # Write data rows
        for row in records:
            writer.writerow([
                row["session_date"],
                row["name"],
                row["roll_no"],
                row["department"],
                row["status"],
                row["first_seen"] or "N/A",
                row["last_seen"] or "N/A",
                row["total_duration_minutes"],
                row["sustained_presence"]
            ])

        output.seek(0)
        filename = f"attendance_report_{selected_date or date.today().isoformat()}.csv"

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    @app.route("/api/health")
    def health():
        """Health check endpoint."""
        return jsonify({
            "status": "online",
            "app": "Multimodal Attendance & Engagement Agent MVP",
            "version": "1.0.0",
            "mode": "Demonstration / Local SQLite"
        })

    return app

if __name__ == "__main__":
    app = create_app()
    print("\n" + "="*60)
    print(" Multimodal Attendance & Engagement Agent is running!")
    print(" Local URL: http://127.0.0.1:5000")
    print(" Press Ctrl+C in this terminal to stop the server.")
    print("="*60 + "\n")
    app.run(debug=True, host="127.0.0.1", port=5000)
