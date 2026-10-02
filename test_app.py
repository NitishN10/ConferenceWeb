import io
import unittest
from app import create_app
from models import db, Registration, PaperSubmission, ContactMessage, Admin

class ConferenceAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_01_public_pages(self):
        routes = [
            '/',
            '/about',
            '/tracks',
            '/call-for-papers',
            '/speakers',
            '/committee',
            '/schedule',
            '/fees',
            '/venue',
            '/contact',
            '/faq'
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with {response.status_code}")
            self.assertIn(b'Sapthagiri NPS University', response.data)
            print(f"Verified {route} -> 200 OK")

    def test_02_template_download(self):
        response = self.client.get('/download-template')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/vnd.openxmlformats-officedocument.wordprocessingml.document', response.content_type)
        print("Verified /download-template -> 200 OK (Word Document)")

    def test_03_contact_submission(self):
        response = self.client.post('/contact', data={
            'name': 'Prof. John Doe',
            'email': 'johndoe@mit.edu',
            'phone': '+1 555 123456',
            'subject': 'Special Session Inquiry',
            'message': 'We would like to organize a special session on Distributed Graph Analytics.'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        msg = ContactMessage.query.filter_by(email='johndoe@mit.edu').first()
        self.assertIsNotNone(msg)
        self.assertEqual(msg.subject, 'Special Session Inquiry')
        print("Verified /contact submission & persistence in DB")

    def test_04_registration_flow(self):
        response = self.client.post('/registration', data={
            'name': 'Dr. Kavitha Raman',
            'email': 'kavitha.raman@iisc.ac.in',
            'phone': '+91 98450 11223',
            'institution': 'Indian Institute of Science (IISc)',
            'department': 'Department of Computational and Data Sciences',
            'designation': 'Assistant Professor',
            'participant_type': 'Faculty / Academician',
            'country': 'India',
            'payment_mode': 'NEFT/RTGS Bank Transfer',
            'transaction_ref': 'UTR9988776655',
            'dietary_pref': 'Vegetarian'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration Confirmed', response.data)
        
        reg = Registration.query.filter_by(email='kavitha.raman@iisc.ac.in').first()
        self.assertIsNotNone(reg)
        self.assertTrue(reg.registration_id.startswith('SNPSU-BDTT-REG-'))
        print(f"Verified /registration flow -> Generated {reg.registration_id}")

    def test_04b_project_team_registration_flow(self):
        import json
        team_members = [
            {'id': 2, 'name': 'Ananya Rao', 'srn': '1RV23CS045', 'email': 'ananya12@gmail.com', 'department': 'Computer Science & Engineering', 'semester': '6th Semester'},
            {'id': 3, 'name': 'Karthik S', 'srn': '1RV23CS088', 'email': 'karthik34@gmail.com', 'department': 'Computer Science & Engineering', 'semester': '6th Semester'}
        ]
        response = self.client.post('/registration', data={
            'name': 'Nitish N',
            'srn': '1RV23CS001',
            'email': 'nitish12@gmail.com',
            'phone': '9845012345',
            'department': 'Computer Science & Engineering',
            'semester': '6th Semester',
            'participant_type': 'Project Team Entry (2-5 Students)',
            'project_title': 'Real-Time Distributed Traffic Flow Optimization using Big Data & AI',
            'project_category': 'Track 1: Big Data Analytics & Distributed Systems',
            'technologies': 'Apache Spark, Python, PyTorch, React, Docker',
            'project_abstract': 'This project formulates an intelligent distributed traffic management system leveraging real-time stream analytics and deep reinforcement learning on distributed edge nodes.',
            'mentor_name': 'Dr. Ramesh Kumar, Professor',
            'team_members': json.dumps(team_members),
            'amount_paid': '₹ 500',
            'payment_mode': 'UPI / QR Code',
            'transaction_ref': 'UPI889977665544'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration Confirmed', response.data)
        self.assertIn(b'Nitish N', response.data)
        self.assertIn(b'1RV23CS001', response.data)
        self.assertIn(b'Ananya Rao', response.data)
        self.assertIn(b'1RV23CS045', response.data)
        self.assertIn(b'500', response.data)

        team_reg = Registration.query.filter_by(email='nitish12@gmail.com').first()
        self.assertIsNotNone(team_reg)
        self.assertEqual(team_reg.srn, '1RV23CS001')
        self.assertEqual(team_reg.amount_paid, '₹ 500')
        self.assertEqual(len(team_reg.team_members), 2)
        print(f"Verified /registration project team entry flow -> Generated {team_reg.registration_id}")

    def test_04c_invalid_email_format_rejected(self):
        # Test rejection of improper email formats (e.g. missing domain, missing @, etc.)
        invalid_emails = ['notanemail', 'user@', 'user@domain', 'user@.com', 'user@domain.']
        for bad_email in invalid_emails:
            response = self.client.post('/registration', data={
                'name': 'Invalid Email Test',
                'email': bad_email,
                'phone': '9845012345',
                'department': 'Computer Science & Engineering',
                'semester': '6th Semester',
                'participant_type': 'Project Team Entry (2-5 Students)'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'format name12@gmail.com is required', response.data)
        print("Verified invalid email format rejection for team leader and members.")

    def test_05_paper_submission_flow(self):
        dummy_file = (io.BytesIO(b"%PDF-1.4 Mock manuscript content for ICBDTT-2026 conference research paper testing."), "scalable_lakehouse_paper.pdf")
        response = self.client.post('/submission', data={
            'corresponding_author': 'Dr. Vikram Chandra',
            'email': 'vikram.chandra@snpsu.edu.in',
            'phone': '+91 99000 88776',
            'institution': 'Sapthagiri NPS University',
            'department': 'Computer Science & Engineering',
            'country': 'India',
            'title': 'High-Throughput Lakehouse Partitioning on Distributed Clusters',
            'track': 'Big Data Technologies & Distributed Infrastructure',
            'abstract': 'This research paper investigates real-time distributed data partitioning in multi-tier cloud lakehouse architectures. We formulate a novel adaptive partition re-balancing mechanism for Apache Spark that dynamically responds to memory pressure and skew. Experimental evaluations conducted on a 64-node cluster show a 38% reduction in latency and significant throughput enhancements over existing baseline techniques.',
            'keywords': 'Big Data, Lakehouse, Apache Spark, Query Optimization, Distributed Computing',
            'declaration': 'on',
            'paper_file': dummy_file
        }, content_type='multipart/form-data', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Submission Confirmation', response.data)

        paper = PaperSubmission.query.filter_by(email='vikram.chandra@snpsu.edu.in').order_by(PaperSubmission.id.desc()).first()
        self.assertIsNotNone(paper)
        self.assertTrue(paper.paper_id.startswith('SNPSU-BDTT-P-'))
        self.assertEqual(paper.status, 'Submitted')
        print(f"Verified /submission flow -> Generated {paper.paper_id}")

        # Test Status Tracking
        status_resp = self.client.post('/submission/status', data={
            'paper_id': paper.paper_id,
            'email': 'vikram.chandra@snpsu.edu.in'
        })
        self.assertEqual(status_resp.status_code, 200)
        self.assertIn(b'High-Throughput Lakehouse Partitioning', status_resp.data)
        print("Verified /submission/status tracking lookup")

    def test_06_admin_flow(self):
        # 1. Login
        login_resp = self.client.post('/admin/login', data={
            'username': 'admin',
            'password': 'Admin@SNPSU2026!'
        }, follow_redirects=True)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn(b'Dashboard Overview', login_resp.data)
        print("Verified admin login -> 200 OK")

        # 2. View Registrations & CSV Export
        reg_resp = self.client.get('/admin/registrations')
        self.assertEqual(reg_resp.status_code, 200)

        csv_resp = self.client.get('/admin/registrations/export')
        self.assertEqual(csv_resp.status_code, 200)
        self.assertEqual(csv_resp.content_type, 'text/csv; charset=utf-8')
        self.assertIn(b'Registration ID,Full Name,Email', csv_resp.data)
        print("Verified /admin/registrations and CSV export")

        # 3. View Submissions & Change Status
        sub_resp = self.client.get('/admin/submissions')
        self.assertEqual(sub_resp.status_code, 200)

        paper = PaperSubmission.query.order_by(PaperSubmission.id.desc()).first()
        if paper:
            status_update_resp = self.client.post(f'/admin/submissions/{paper.id}/status', data={
                'status': 'Accepted',
                'reviewer_comments': 'Excellent contributions to big data lakehouse architectures. Formally accepted.'
            }, follow_redirects=True)
            self.assertEqual(status_update_resp.status_code, 200)
            
            db.session.refresh(paper)
            self.assertEqual(paper.status, 'Accepted')
            print(f"Verified admin status update -> {paper.paper_id} marked as Accepted")

            # Download submitted paper
            dl_resp = self.client.get(f'/admin/submissions/{paper.id}/download')
            self.assertEqual(dl_resp.status_code, 200)
            print("Verified admin paper download")

if __name__ == '__main__':
    unittest.main()
