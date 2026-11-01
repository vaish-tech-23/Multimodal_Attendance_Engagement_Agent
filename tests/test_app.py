import unittest
import os
import sys

# Ensure parent directory is in module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database import get_db_connection

class TestMultimodalAgent(unittest.TestCase):
    def setUp(self):
        """Set up test client and configure test mode."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_health_check(self):
        """Test API health check returns 200."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "online")

    def test_dashboard_route(self):
        """Test dashboard page loads with statistics."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Classroom Overview Dashboard", response.data)
        self.assertIn(b"DEMO MODE ACTIVE", response.data)

    def test_attendance_page(self):
        """Test attendance checklist page renders."""
        response = self.client.get("/attendance")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Attendance Management", response.data)

    def test_mark_attendance(self):
        """Test toggling student attendance status."""
        response = self.client.post("/attendance/mark", data={
            "participant_id": 1,
            "status": "Absent"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Status updated to &#39;Absent&#39;.", response.data)

    def test_add_student(self):
        """Test registering a new student."""
        import time
        test_roll = f"TEST-CS-{int(time.time() * 1000)}"
        response = self.client.post("/students/add", data={
            "name": "Test Student",
            "roll_no": test_roll,
            "department": "AI & Robotics",
            "email": "test@campus.edu"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student added successfully.", response.data)

    def test_engagement_page(self):
        """Test multimodal engagement analysis page."""
        response = self.client.get("/engagement")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Multimodal Engagement Analysis", response.data)
        self.assertIn(b"Head Pose Orientation", response.data)

    def test_suggestions_page_and_refresh(self):
        """Test AI teaching suggestions and refresh trigger."""
        response = self.client.get("/suggestions")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"AI Teaching Suggestions", response.data)

        refresh_res = self.client.post("/suggestions/refresh", follow_redirects=True)
        self.assertEqual(refresh_res.status_code, 200)
        self.assertIn(b"AI rules evaluated", refresh_res.data)

    def test_reports_page_and_csv_download(self):
        """Test historical reports and CSV file download."""
        response = self.client.get("/reports")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Attendance Reports & Audit History", response.data)

        csv_res = self.client.get("/reports/download")
        self.assertEqual(csv_res.status_code, 200)
        self.assertEqual(csv_res.headers["Content-Type"], "text/csv; charset=utf-8")
        self.assertIn(b"Session Date,Student Name,Roll Number", csv_res.data)

if __name__ == "__main__":
    unittest.main()
