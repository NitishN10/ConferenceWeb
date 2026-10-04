import os
from flask import Flask
from config import Config
from models.db import db
from models.admin import Admin
from models.track import ConferenceTrack
from models.dates import ImportantDate
from models.speaker import Speaker
from models.schedule import ScheduleItem
from models.fee import RegistrationFee
from models.faq import FAQItem

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    is_vercel = bool(
        os.environ.get('VERCEL') == '1'
        or os.environ.get('VERCEL_ENV')
        or os.environ.get('AWS_LAMBDA_FUNCTION_NAME')
    )
    if not is_vercel:
        try:
            db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
            if db_uri.startswith('sqlite:') and 'instance' in db_uri:
                os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
            if app.config.get('UPLOAD_FOLDER'):
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            if app.config.get('SPEAKER_UPLOAD_FOLDER'):
                os.makedirs(app.config['SPEAKER_UPLOAD_FOLDER'], exist_ok=True)
        except OSError:
            pass
    db.init_app(app)
    return app

def populate_seed_data(app=None):
    """Populates conference reference data without dropping existing tables."""
    ctx = app.app_context() if app else None
    if ctx:
        ctx.push()
    try:
        # 1. Admin User
        admin = Admin(
            username='admin',
            full_name='Conference Administrator',
            email='icbdtt@snpsu.edu.in'
        )
        admin.set_password('Admin@SNPSU2026!')
        db.session.add(admin)
        print("Created default admin user: admin / Admin@SNPSU2026!")

        # 2. Conference Tracks (Core requested academic topics)
        tracks_data = [
            {
                "track_number": 1,
                "code": "TRACK-01",
                "title": "Artificial Intelligence and Machine Learning",
                "short_title": "AI & ML",
                "icon": "bi-cpu",
                "description": "Deep learning architectures, neural networks, reinforcement learning, predictive algorithms, explainable AI, and autonomous decision systems.",
                "topics": "Deep Learning\nMachine Learning Algorithms\nExplainable AI (XAI)\nReinforcement Learning\nIntelligent Optimization"
            },
            {
                "track_number": 2,
                "code": "TRACK-02",
                "title": "Data Science, Big Data and Data Analytics",
                "short_title": "Data Science & Analytics",
                "icon": "bi-bar-chart-steps",
                "description": "Large-scale data pipelines, statistical modeling, data lakes, business intelligence, streaming analytics, and knowledge graph engineering.",
                "topics": "Big Data Pipelines\nStatistical Modelling\nData Mining\nStreaming Analytics\nPredictive Modeling"
            },
            {
                "track_number": 3,
                "code": "TRACK-03",
                "title": "Computer Vision and Image Processing",
                "short_title": "Computer Vision",
                "icon": "bi-camera",
                "description": "Object detection, medical imaging analytics, pattern recognition, image segmentation, video surveillance, and biometric visual processing.",
                "topics": "Object Detection\nMedical Imaging Analysis\nImage Segmentation\nBiometric Vision\nVideo Telemetry"
            },
            {
                "track_number": 4,
                "code": "TRACK-04",
                "title": "Natural Language Processing and Generative AI",
                "short_title": "NLP & Generative AI",
                "icon": "bi-chat-square-quote",
                "description": "Large Language Models (LLMs), semantic analysis, machine translation, generative multi-modal agents, sentiment analysis, and speech processing.",
                "topics": "Large Language Models (LLMs)\nGenerative AI Models\nSemantic Parsing\nMachine Translation\nConversational Agents"
            },
            {
                "track_number": 5,
                "code": "TRACK-05",
                "title": "Cybersecurity, Privacy and Digital Forensics",
                "short_title": "Cybersecurity & Forensics",
                "icon": "bi-shield-lock",
                "description": "Threat modeling, intrusion detection systems, differential privacy, forensic data recovery, cryptography, and secure software architectures.",
                "topics": "Network Security & IDS\nDifferential Privacy\nCryptographic Protocols\nDigital Forensics\nSecure Data Architectures"
            },
            {
                "track_number": 6,
                "code": "TRACK-06",
                "title": "Internet of Things and Edge Computing",
                "short_title": "IoT & Edge Computing",
                "icon": "bi-router",
                "description": "Smart sensory networks, edge intelligence, fog computing topologies, stream processing at scale, and low-latency cyber-physical systems.",
                "topics": "Edge Intelligence\nIoT Sensor Streams\nFog Computing\nCyber-Physical Systems\nEmbedded AI"
            },
            {
                "track_number": 7,
                "code": "TRACK-07",
                "title": "Cloud Computing and Distributed Systems",
                "short_title": "Cloud & Distributed Systems",
                "icon": "bi-cloud-arrow-up",
                "description": "Serverless computing, multi-cloud orchestration, microservices, containerization, distributed consensus, and fault-tolerant cloud clusters.",
                "topics": "Serverless Architectures\nMicroservices & Containers\nMulti-Cloud Orchestration\nDistributed Consensus\nFault-Tolerant Clusters"
            },
            {
                "track_number": 8,
                "code": "TRACK-08",
                "title": "Blockchain and Emerging Computing Technologies",
                "short_title": "Blockchain & Emerging Tech",
                "icon": "bi-boxes",
                "description": "Distributed ledgers, smart contracts, decentralized applications (dApps), quantum computing paradigms, and decentralized identity governance.",
                "topics": "Smart Contracts & DeFi\nDistributed Ledger Tech\nQuantum Algorithms\nDecentralized Identity\nConsensus Protocols"
            },
            {
                "track_number": 9,
                "code": "TRACK-09",
                "title": "Computer Networks and Communication Systems",
                "short_title": "Networks & Communications",
                "icon": "bi-diagram-3",
                "description": "5G/6G wireless networks, software-defined networking (SDN), network telemetry, latency optimization, and next-generation protocols.",
                "topics": "5G/6G Wireless Networks\nSoftware-Defined Networking\nNetwork Telemetry\nTraffic Engineering\nOptical & Sensor Comms"
            },
            {
                "track_number": 10,
                "code": "TRACK-10",
                "title": "Software Engineering, Testing and Agile Development",
                "short_title": "Software Engineering",
                "icon": "bi-code-slash",
                "description": "DevOps/MLOps automation, automated regression verification, software architecture metrics, code smells detection, and continuous delivery.",
                "topics": "DevOps & MLOps Pipelines\nAutomated Testing\nSoftware Quality Metrics\nMicroservice Refactoring\nAgile Engineering"
            },
            {
                "track_number": 11,
                "code": "TRACK-11",
                "title": "Human–Computer Interaction and User Experience",
                "short_title": "HCI & UX",
                "icon": "bi-person-bounding-box",
                "description": "Accessibility engineering, multimodal interaction design, cognitive load modeling, user telemetry, and intuitive assistive user interfaces.",
                "topics": "Multimodal Interfaces\nAccessibility Engineering\nCognitive Ergonomics\nUser Telemetry & Analytics\nAssistive Technology"
            },
            {
                "track_number": 12,
                "code": "TRACK-12",
                "title": "Extended Reality, Virtual Reality and Spatial Computing",
                "short_title": "XR & Spatial Computing",
                "icon": "bi-headset-vr",
                "description": "Immersive 3D environments, spatial mapping, augmented reality applications, digital twins, haptic feedback systems, and holographic visualization.",
                "topics": "Virtual & Augmented Reality\nSpatial Computing\nDigital Twins\nHaptic Feedback Interfaces\nImmersive 3D Simulation"
            },
            {
                "track_number": 13,
                "code": "TRACK-13",
                "title": "Robotics, Automation and Intelligent Systems",
                "short_title": "Robotics & Automation",
                "icon": "bi-robot",
                "description": "Autonomous mobile robots, industrial automation, sensory perception, drone navigation algorithms, swarm intelligence, and robotic process automation.",
                "topics": "Autonomous Mobile Robotics\nIndustrial Automation\nSensory Perception\nDrone Navigation\nSwarm Intelligence"
            }
        ]
        for td in tracks_data:
            db.session.add(ConferenceTrack(**td))
        print(f"Seeded {len(tracks_data)} Conference Tracks.")

        # 3. Important Dates (Only official confirmed dates; others pending)
        dates_data = [
            {
                "title": "Conference Dates",
                "date_value": "November 20–21, 2026",
                "description": "Inauguration, Keynotes, Student Presentations & Valedictory (10:00 AM – 4:00 PM)",
                "is_extended": False,
                "status_badge": "Confirmed",
                "display_order": 1
            },
            {
                "title": "Full Paper Submission Deadline",
                "date_value": "To be announced",
                "description": "Manuscript submission deadline will be updated upon official brochure release",
                "is_extended": False,
                "status_badge": "Pending Release",
                "display_order": 2
            },
            {
                "title": "Notification of Acceptance",
                "date_value": "To be announced",
                "description": "Double-blind peer review feedback and acceptance notices",
                "is_extended": False,
                "status_badge": "Pending",
                "display_order": 3
            },
            {
                "title": "Camera Ready Paper & Copyright",
                "date_value": "To be announced",
                "description": "Final formatted manuscript submission and copyright clearance",
                "is_extended": False,
                "status_badge": "Pending",
                "display_order": 4
            },
            {
                "title": "Author / Delegate Registration Deadline",
                "date_value": "To be announced",
                "description": "Mandatory registration deadline for presenting authors and attendees",
                "is_extended": False,
                "status_badge": "Pending",
                "display_order": 5
            }
        ]
        for dd in dates_data:
            db.session.add(ImportantDate(**dd))
        print("Seeded Important Dates.")

        # 4. Speakers & Guests (Schema-ready placeholders pending official release)
        speakers_data = [
            {
                "name": "Guest Speaker – Inaugural Session",
                "designation": "Eminent Scholar / Industry Luminary",
                "institution": "Profile Pending Official Announcement",
                "country": "India / International",
                "biography": "Official guest speaker details, designation, and inaugural address topic (~30 minutes) will be updated upon confirmation by the organizing committee.",
                "photo": "speaker_placeholder.svg",
                "speaker_type": "Inaugural Guest",
                "session_topic": "Inaugural Address on Trends in Big Data Tools & Computing Systems",
                "display_order": 1
            },
            {
                "name": "Keynote Speaker 1",
                "designation": "Distinguished Academician / Fellow",
                "institution": "Profile Pending Official Announcement",
                "country": "India / International",
                "biography": "Keynote profile and plenary lecture abstract will be published once officially confirmed by the conference editorial board.",
                "photo": "speaker_placeholder.svg",
                "speaker_type": "Keynote",
                "session_topic": "Scalable Big Data Architectures & Next-Generation Analytics",
                "display_order": 2
            },
            {
                "name": "Keynote Speaker 2",
                "designation": "Senior Research Scientist / Architect",
                "institution": "Profile Pending Official Announcement",
                "country": "India / International",
                "biography": "Keynote profile, research contributions, and invited talk details will be posted upon official confirmation.",
                "photo": "speaker_placeholder.svg",
                "speaker_type": "Keynote",
                "session_topic": "Applied Machine Intelligence, Cloud Platforms & Scalable Systems",
                "display_order": 3
            },
            {
                "name": "Guest Speaker – Valedictory Session",
                "designation": "Distinguished Guest of Honour",
                "institution": "Profile Pending Official Announcement",
                "country": "India / International",
                "biography": "Valedictory address speaker profile (~15 minutes) and citation will be shared prior to the conference.",
                "photo": "speaker_placeholder.svg",
                "speaker_type": "Valedictory Guest",
                "session_topic": "Valedictory Address & Future Frontiers in Big Data Engineering",
                "display_order": 4
            }
        ]
        for sd in speakers_data:
            db.session.add(Speaker(**sd))
        print("Seeded Speakers.")

        # 5. Registration Fees
        fees_data = [
            {
                "category": "Students (UG / PG)",
                "inr_early": "₹ 1,500",
                "inr_regular": "₹ 2,000",
                "usd_early": "$ 50",
                "usd_regular": "$ 70",
                "benefits": "Conference Kit, Official Certificate, Lunch & Access to All Technical Sessions",
                "display_order": 1
            },
            {
                "category": "Research Scholars / Ph.D.",
                "inr_early": "₹ 2,500",
                "inr_regular": "₹ 3,000",
                "usd_early": "$ 75",
                "usd_regular": "$ 100",
                "benefits": "Proceedings Inclusion, Author Presentation Slot, Kit, Certificate & Lunch",
                "display_order": 2
            },
            {
                "category": "Faculty / Academicians",
                "inr_early": "₹ 3,500",
                "inr_regular": "₹ 4,000",
                "usd_early": "$ 100",
                "usd_regular": "$ 130",
                "benefits": "Full Conference Access, Presentation Slot, Certificate, Conference Kit & Proceedings",
                "display_order": 3
            },
            {
                "category": "Industry Professionals",
                "inr_early": "₹ 5,000",
                "inr_regular": "₹ 6,000",
                "usd_early": "$ 150",
                "usd_regular": "$ 180",
                "benefits": "Corporate Delegate Pass, Networking Sessions, Full Conference Kit & Certificate",
                "display_order": 4
            },
            {
                "category": "International Participants",
                "inr_early": "$ 120",
                "inr_regular": "$ 150",
                "usd_early": "$ 120",
                "usd_regular": "$ 150",
                "benefits": "International Delegate Pass, Hybrid/In-Person Presentation, Proceedings & Certificate",
                "display_order": 5
            }
        ]
        for fd in fees_data:
            db.session.add(RegistrationFee(**fd))
        print("Seeded Registration Fees.")

        # 6. Schedule Items (Strictly based on confirmed timings and parallel tracks)
        schedule_data = [
            # Day 1 - November 20, 2026
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "09:45 AM",
                "end_time": "11:45 AM",
                "session_type": "Student Presentation",
                "session_title": "University Student Project & Paper Presentations",
                "speaker": "42 Sections (10 mins per batch)",
                "topic": "Parallel presentations across respective existing classrooms on Floors 2–4. Allied branches on Floors 5–6 (Room allocations to be announced).",
                "venue": "Floors 2–4 (Allied Branches: Floors 5–6)",
                "display_order": 1
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "10:00 AM",
                "end_time": "11:15 AM",
                "session_type": "Inauguration",
                "session_title": "Official Conference Inauguration Ceremony",
                "speaker": "Guest Speaker (~30 min) & University Dignitaries (~10 min each)",
                "topic": "Inaugural address, lighting of the lamp & conference launch (Speakers to be officially announced)",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 2
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "11:15 AM",
                "end_time": "01:00 PM",
                "session_type": "Keynote",
                "session_title": "Guest and Plenary Speaker Sessions",
                "speaker": "Distinguished Guest Speakers (To be announced)",
                "topic": "Plenary lectures on Big Data Tools, Next-Gen Architectures, and Intelligent Analytics",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 3
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "11:30 AM",
                "end_time": "11:45 AM",
                "session_type": "Break",
                "session_title": "Break for Outside Participants",
                "speaker": None,
                "topic": "Dedicated morning refreshment break for external participants",
                "venue": "6th Floor Delegate Area",
                "display_order": 4
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "12:00 PM",
                "end_time": "01:00 PM",
                "session_type": "Technical Session",
                "session_title": "Outside Participant Project & Paper Presentations",
                "speaker": "External College & Institution Delegates",
                "topic": "Oral paper and technical project presentations by registered outside participants",
                "venue": "6th Floor Classrooms (Room allocation to be announced)",
                "display_order": 5
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "01:00 PM",
                "end_time": "02:00 PM",
                "session_type": "Break",
                "session_title": "Conference Lunch Break",
                "speaker": None,
                "topic": "Buffet networking lunch for delegates, presenters, and guests",
                "venue": "Campus Dining Area",
                "display_order": 6
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "03:00 PM",
                "end_time": "04:00 PM",
                "session_type": "Valedictory",
                "session_title": "Valedictory Ceremony & Prize Distribution",
                "speaker": "Guest Speaker (15 min) & Dignitaries",
                "topic": "Guest Speaker Address (15 mins), Best Presentation Prize Distribution (30 mins), and Conference Report Reading (10 mins)",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 7
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "04:00 PM",
                "end_time": "04:00 PM",
                "session_type": "Conclusion",
                "session_title": "Conference Concludes",
                "speaker": "Secretariat",
                "topic": "Adjournment of Day 1 proceedings",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 8
            },
            # Day 2 - November 21, 2026
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "09:45 AM",
                "end_time": "11:45 AM",
                "session_type": "Student Presentation",
                "session_title": "University Student Presentations (Advanced Tracks)",
                "speaker": "Student Batches (10 mins per batch)",
                "topic": "Evaluations in respective classrooms across Floors 2–4. Allied branches on Floors 5–6.",
                "venue": "Floors 2–4 (Allied Branches: Floors 5–6)",
                "display_order": 9
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "10:00 AM",
                "end_time": "11:15 AM",
                "session_type": "Keynote",
                "session_title": "Plenary Research Address",
                "speaker": "Invited Scholar (To be announced)",
                "topic": "Emerging Frontiers in Distributed Computing & Scalable Intelligent Systems",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 10
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "11:30 AM",
                "end_time": "11:45 AM",
                "session_type": "Break",
                "session_title": "Break for Outside Participants",
                "speaker": None,
                "topic": "Refreshment break for external attendees",
                "venue": "6th Floor Delegate Area",
                "display_order": 11
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "12:00 PM",
                "end_time": "01:00 PM",
                "session_type": "Technical Session",
                "session_title": "Outside Participant Technical Presentations (Track B)",
                "speaker": "External College & Institution Presenters",
                "topic": "Presentations of big data and AI research by outside delegates",
                "venue": "6th Floor Classrooms (Room allocation to be announced)",
                "display_order": 12
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "01:00 PM",
                "end_time": "02:00 PM",
                "session_type": "Break",
                "session_title": "Conference Lunch Break",
                "speaker": None,
                "topic": "Buffet networking lunch",
                "venue": "Campus Dining Area",
                "display_order": 13
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "03:00 PM",
                "end_time": "04:00 PM",
                "session_type": "Valedictory",
                "session_title": "Grand Valedictory Ceremony & Best Paper Awards",
                "speaker": "Valedictory Guest Speaker (15 min) & Dignitaries",
                "topic": "Guest Speaker Address (15 mins), Best Paper & Project Awards (30 mins), and Comprehensive Conference Report Reading (10 mins)",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 14
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "04:00 PM",
                "end_time": "04:00 PM",
                "session_type": "Conclusion",
                "session_title": "Conference Concludes",
                "speaker": "Secretariat",
                "topic": "Official adjournment of ICBDTT-2026",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 15
            }
        ]
        for s in schedule_data:
            db.session.add(ScheduleItem(**s))
        print("Seeded Conference Schedule Items.")

        # 7. FAQs (Clean and factual without invented dates or fake partners)
        faq_data = [
            {
                "category": "Submissions",
                "question": "Who can submit a paper?",
                "answer": "Researchers, academicians, PhD scholars, students, and industry professionals are eligible to submit original research manuscripts within the scope of the conference tracks.",
                "display_order": 1
            },
            {
                "category": "Submissions",
                "question": "What is the paper format?",
                "answer": "Papers should be prepared according to standard double-column conference format (Word template available on the Call for Papers page). Full papers should strictly follow the prescribed page limit.",
                "display_order": 2
            },
            {
                "category": "Submissions",
                "question": "What file formats are accepted?",
                "answer": "The submission portal accepts PDF, DOC, and DOCX formats up to a maximum file size of 16 MB.",
                "display_order": 3
            },
            {
                "category": "Submissions",
                "question": "What are the important dates?",
                "answer": "All important dates, including submission deadlines, notification of acceptance, and camera-ready deadlines, are listed on the Important Dates section of the website.",
                "display_order": 4
            },
            {
                "category": "Registration",
                "question": "How do I register?",
                "answer": "Navigate to the 'Registration' page, select your participant category, fill in your details and linked Paper ID (if applicable), and submit the form to receive your unique Registration ID.",
                "display_order": 5
            },
            {
                "category": "Registration",
                "question": "Can students participate?",
                "answer": "Yes, undergraduate and postgraduate students are encouraged to participate and register under the student category.",
                "display_order": 6
            },
            {
                "category": "Registration",
                "question": "Is there a registration fee?",
                "answer": "Yes, there is a registration fee based on participant categories. Please refer to the Registration Fees section on the website for the current fee structure.",
                "display_order": 7
            },
            {
                "category": "Venue",
                "question": "Where will the conference be conducted?",
                "answer": "The conference will be conducted at Sapthagiri NPS University (SNPSU) Campus, Bengaluru, Karnataka, India. Detailed venue information is available on the Venue page.",
                "display_order": 8
            }
        ]
        for f in faq_data:
            db.session.add(FAQItem(**f))
        print("Seeded FAQ items.")

        db.session.commit()
        print("Clean database seeding completed successfully.")
    finally:
        if ctx:
            ctx.pop()

def seed_database():
    app = create_app()
    with app.app_context():
        # Clear existing data to remove unwanted invented information
        db.drop_all()
        db.create_all()
        populate_seed_data()

def init_db_and_seed(app):
    """
    Initializes database tables, synchronizes column schema for PostgreSQL/SQLite,
    and populates default conference data if tables are empty.
    Safe for production startup (does not drop any existing data).
    """
    try:
        with app.app_context():
            db.create_all()

            # Dynamic schema synchronization for PostgreSQL & SQLite:
            # Ensures columns added in models exist on existing tables without requiring external migration tooling.
            try:
                from sqlalchemy import inspect, text
                inspector = inspect(db.engine)
                table_names = inspector.get_table_names()

                # Ensure registrations columns exist
                if 'registrations' in table_names:
                    existing_cols = {col['name'] for col in inspector.get_columns('registrations')}
                    col_defs = {
                        'srn': 'VARCHAR(50)',
                        'semester': 'VARCHAR(50)',
                        'project_title': 'TEXT',
                        'project_category': 'VARCHAR(255)',
                        'project_abstract': 'TEXT',
                        'technologies': 'TEXT',
                        'mentor_name': 'VARCHAR(255)',
                        'desk_number': 'VARCHAR(100)',
                        'team_members_json': 'TEXT',
                        'payment_mode': 'VARCHAR(100)',
                        'transaction_ref': 'VARCHAR(100)',
                        'payment_status': 'VARCHAR(50)',
                        'amount_paid': 'VARCHAR(50)',
                        'dietary_pref': 'VARCHAR(50)',
                        'created_at': 'TIMESTAMP'
                    }
                    for col_name, col_type in col_defs.items():
                        if col_name not in existing_cols:
                            try:
                                db.session.execute(text(f"ALTER TABLE registrations ADD COLUMN {col_name} {col_type}"))
                                db.session.commit()
                            except Exception as ce:
                                db.session.rollback()
                                app.logger.warning(f"Could not add column {col_name} to registrations: {ce}")

                # Ensure paper_submissions file_data column exists
                if 'paper_submissions' in table_names:
                    sub_cols = {col['name'] for col in inspector.get_columns('paper_submissions')}
                    if 'file_data' not in sub_cols:
                        try:
                            is_postgres = db.engine.dialect.name == 'postgresql'
                            col_type = 'BYTEA' if is_postgres else 'BLOB'
                            db.session.execute(text(f"ALTER TABLE paper_submissions ADD COLUMN file_data {col_type}"))
                            db.session.commit()
                        except Exception as ce:
                            db.session.rollback()
                            app.logger.warning(f"Could not add column file_data to paper_submissions: {ce}")
            except Exception as se:
                app.logger.warning(f"Schema synchronization skipped: {se}")

            if ConferenceTrack.query.first() is None:
                populate_seed_data()
            elif Admin.query.filter_by(username='admin').first() is None:
                try:
                    default_admin = Admin(
                        username='admin',
                        full_name='Conference Administrator',
                        email='icbdtt@snpsu.edu.in'
                    )
                    default_admin.set_password('Admin@SNPSU2026!')
                    db.session.add(default_admin)
                    db.session.commit()
                except Exception as ae:
                    db.session.rollback()
                    app.logger.warning(f"Could not auto-create default admin: {ae}")
    except Exception as e:
        app.logger.warning(f"Database auto-initialization skipped or deferred: {e}")

if __name__ == '__main__':
    seed_database()
