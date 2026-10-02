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
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['SPEAKER_UPLOAD_FOLDER'], exist_ok=True)
    db.init_app(app)
    return app

def seed_database():
    app = create_app()
    with app.app_context():
        # Clear existing data to remove unwanted invented information
        db.drop_all()
        db.create_all()

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

        # 3. Important Dates
        dates_data = [
            {
                "title": "Paper Submission Opens",
                "date_value": "June 1, 2026",
                "description": "Official opening of portal for research paper submissions",
                "is_extended": False,
                "status_badge": "Completed",
                "display_order": 1
            },
            {
                "title": "Paper Submission Deadline",
                "date_value": "September 15, 2026",
                "description": "Strict deadline for full manuscript submissions (6-8 pages)",
                "is_extended": False,
                "status_badge": "Open",
                "display_order": 2
            },
            {
                "title": "Notification of Acceptance",
                "date_value": "October 10, 2026",
                "description": "Double-blind review feedback and acceptance notices issued",
                "is_extended": False,
                "status_badge": "Upcoming",
                "display_order": 3
            },
            {
                "title": "Camera Ready Paper & Copyright",
                "date_value": "October 25, 2026",
                "description": "Final formatted manuscript submission and copyright form",
                "is_extended": False,
                "status_badge": "Upcoming",
                "display_order": 4
            },
            {
                "title": "Author Registration Deadline",
                "date_value": "October 30, 2026",
                "description": "Mandatory deadline for at least one author per accepted paper",
                "is_extended": False,
                "status_badge": "Upcoming",
                "display_order": 5
            },
            {
                "title": "Conference Dates",
                "date_value": "November 20–21, 2026",
                "description": "Inauguration, Keynotes, Technical Presentations & Valedictory",
                "is_extended": False,
                "status_badge": "Upcoming",
                "display_order": 6
            }
        ]
        for dd in dates_data:
            db.session.add(ImportantDate(**dd))
        print("Seeded Important Dates.")

        # 4. Speakers (Distinguished Academics & Researchers)
        speakers_data = [
            {
                "name": "Dr. Anand Rajaraman",
                "designation": "Visiting Professor & AI Fellow",
                "institution": "Indian Institute of Science (IISc)",
                "country": "India",
                "biography": "Dr. Anand Rajaraman is a distinguished researcher in large-scale data systems and AI. Alumnus of Stanford University, he has authored foundational papers in distributed databases and mining massive datasets.",
                "photo": "speaker1.svg",
                "speaker_type": "Keynote",
                "session_topic": "Scalable Lakehouse Architectures for Exabyte-Scale Real-Time Analytics",
                "display_order": 1
            },
            {
                "name": "Prof. Priya Sundaram",
                "designation": "Professor & Chair of Data Engineering",
                "institution": "National University of Singapore (NUS)",
                "country": "Singapore",
                "biography": "Prof. Priya Sundaram leads research in autonomous distributed systems, adaptive stream processing, and resilient edge intelligence with over 120 high-impact publications.",
                "photo": "speaker2.svg",
                "speaker_type": "Keynote",
                "session_topic": "Autonomous Distributed Systems & Resilient Edge Data Pipelines",
                "display_order": 2
            },
            {
                "name": "Dr. Rajeshwar Rao",
                "designation": "Chief Scientist & Fellow",
                "institution": "Big Data Intelligence Labs",
                "country": "India",
                "biography": "Dr. Rajeshwar Rao specializes in multimodal foundation models, high-performance distributed computing frameworks, and accelerated graph analytics on cloud clusters.",
                "photo": "speaker3.svg",
                "speaker_type": "Keynote",
                "session_topic": "Foundation Models & Multimodal Big Data Processing: Paradigms and Benchmarks",
                "display_order": 3
            },
            {
                "name": "Dr. Marcus Vance",
                "designation": "Principal Data Architect",
                "institution": "Distributed Cloud Systems",
                "country": "United Kingdom",
                "biography": "Dr. Marcus Vance is an industry authority on federated query optimization, differential privacy, and decentralized data mesh architectures for enterprise workloads.",
                "photo": "speaker4.svg",
                "speaker_type": "Invited",
                "session_topic": "Privacy-Preserving Federated Query Engines on Heterogeneous Clouds",
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

        # 6. Schedule Items
        schedule_data = [
            # Day 1
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "08:30 AM",
                "end_time": "09:30 AM",
                "session_type": "Registration",
                "session_title": "Delegate Check-in & Kit Collection",
                "speaker": "Organizing Secretariat",
                "topic": "Welcome reception, delegate badge & conference kit distribution",
                "venue": "Registration Desk, Auditorium Lobby",
                "display_order": 1
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "09:30 AM",
                "end_time": "10:30 AM",
                "session_type": "Inauguration",
                "session_title": "Inauguration Ceremony & Welcome Address",
                "speaker": "Honourable Chancellor & University Dignitaries",
                "topic": "Lighting of the Lamp, Presidential Address & Release of Conference Souvenir",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 2
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "10:30 AM",
                "end_time": "11:00 AM",
                "session_type": "Break",
                "session_title": "Tea & High Networking Break",
                "speaker": None,
                "topic": None,
                "venue": "Convention Foyer",
                "display_order": 3
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "11:00 AM",
                "end_time": "12:15 PM",
                "session_type": "Keynote",
                "session_title": "Keynote Address 1",
                "speaker": "Dr. Anand Rajaraman",
                "topic": "Scalable Lakehouse Architectures for Exabyte-Scale Real-Time Analytics",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 4
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "12:15 PM",
                "end_time": "01:15 PM",
                "session_type": "Break",
                "session_title": "Conference Networking Lunch",
                "speaker": None,
                "topic": None,
                "venue": "University Banquet Hall",
                "display_order": 5
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "01:15 PM",
                "end_time": "03:30 PM",
                "session_type": "Technical Session",
                "session_title": "Technical Paper Presentations: Tracks 1 & 2",
                "speaker": "Session Chairs: Dr. Ramachandra K. & Dr. Suresh Kumar",
                "topic": "Oral presentations on Big Data Analytics and AI/ML",
                "venue": "Seminar Halls A & B",
                "display_order": 6
            },
            {
                "day_number": 1,
                "date_display": "Day 1 - November 20, 2026",
                "start_time": "03:45 PM",
                "end_time": "05:00 PM",
                "session_type": "Keynote",
                "session_title": "Keynote Address 2",
                "speaker": "Prof. Priya Sundaram",
                "topic": "Autonomous Distributed Systems & Resilient Edge Data Pipelines",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 7
            },
            # Day 2
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "09:30 AM",
                "end_time": "10:45 AM",
                "session_type": "Keynote",
                "session_title": "Keynote Address 3",
                "speaker": "Dr. Rajeshwar Rao",
                "topic": "Foundation Models & Multimodal Big Data Processing: Paradigms and Benchmarks",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 8
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "11:00 AM",
                "end_time": "01:00 PM",
                "session_type": "Technical Session",
                "session_title": "Technical Paper Presentations: Tracks 3, 4, 5 & 6",
                "speaker": "Session Chairs: Dr. Kavitha Srinivas & Dr. Poornima M.",
                "topic": "Oral presentations on Big Data Technologies, Data Science, IoT & Security",
                "venue": "Seminar Halls A & C",
                "display_order": 9
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "01:00 PM",
                "end_time": "02:00 PM",
                "session_type": "Break",
                "session_title": "Conference Lunch",
                "speaker": None,
                "topic": None,
                "venue": "University Banquet Hall",
                "display_order": 10
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "02:00 PM",
                "end_time": "03:30 PM",
                "session_type": "Panel",
                "session_title": "Industry-Academia Panel Discussion",
                "speaker": "Dr. Marcus Vance & Distinguished Panelists",
                "topic": "Future of Enterprise Data Platforms, LLM Integrations and Scalability",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 11
            },
            {
                "day_number": 2,
                "date_display": "Day 2 - November 21, 2026",
                "start_time": "03:45 PM",
                "end_time": "05:00 PM",
                "session_type": "Valedictory",
                "session_title": "Valedictory & Awards Ceremony",
                "speaker": "General Chairs & Executive Committee",
                "topic": "Best Research Paper Awards, Distribution of Certificates & Vote of Thanks",
                "venue": "Dr. APJ Abdul Kalam Auditorium",
                "display_order": 12
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

if __name__ == '__main__':
    seed_database()
