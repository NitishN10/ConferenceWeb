# International Conference on Big Data Tools and Techniques (ICBDTT-2026)
### Sapthagiri NPS University (SNPSU), Bengaluru

Official web portal and conference management platform for the **International Conference on Big Data Tools and Techniques (ICBDTT-2026)**, hosted by **Sapthagiri NPS University (SNPSU), Bengaluru**.

> **Conference Theme**: *"Advancing Data-Driven Research, Innovation and Intelligent Solutions"*  
> **Dates**: November 20–21, 2026  
> **Venue**: Dr. APJ Abdul Kalam Auditorium, Sapthagiri NPS University Campus, Bengaluru, Karnataka, India  
> **Official University Reference**: [https://snpsu.edu.in/](https://snpsu.edu.in/)  

---

## 🌟 Key Highlights & Design Identity

- **SNPSU University Branding**: Built on the official Sapthagiri NPS University visual identity featuring the royal navy (`#001040`), warm gold (`#C69E66`), and high-tech cyan accents (`#0284c7`), with official logos and modern academic aesthetics.
- **Dynamic Big Data & Network Visualization**: Interactive HTML5 Canvas particle & node network in the hero section representing neural network graphs and distributed data streams.
- **Fully Modular Multi-Page Architecture**: Each major section has a dedicated, semantic HTML page extending a shared academic base layout (`base.html`).
- **Complete End-to-End Functional Backend**: Real persistence with Python, Flask, and SQLAlchemy (SQLite initially, with a clean path to PostgreSQL).
- **Paper Submission System**: Server-side file validation for PDF/DOC/DOCX up to 16 MB, secure cryptographic filename hashing, persistent metadata storage in DB, unique Paper IDs (e.g. `SNPSU-BDTT-P-XXXX`), and an online status tracking portal.
- **Conference Registration System**: Real-time fee calculator (INR vs. USD for international delegates), Paper ID linkage, and unique Registration IDs (e.g. `SNPSU-BDTT-REG-XXXX`) with printable confirmation vouchers and QR badges.
- **Conference Content Management & Admin Console**:
  - Secure `/admin/login` with Werkzeug password hashing and session authorization.
  - Dashboard analytics overview (Total Registrations, Submissions, Under Review, Accepted, Unread Inquiries).
  - Submissions management: review status updates (`Submitted`, `Under Review`, `Accepted`, `Rejected`, `Camera Ready`), reviewer comments, and manuscript downloads.
  - Registrations management: table search, participant category filters, and CSV export.
  - Speaker, Important Dates, Conference Tracks, and Schedule agenda management.
  - Contact inquiries inbox.
- **Downloadable Word Paper Template**: Pre-formatted `.docx` paper template ready for authors to download.

---

## 📂 Project Architecture

```
Conference website/
├── app.py                      # Flask Application Factory & Error Handlers
├── config.py                   # Central Configuration & Conference Constants
├── requirements.txt            # Python Dependencies
├── .env.example                # Environment Variable Template
├── seed_data.py                # Database Initializer & Pre-Populated Academic Data
├── generate_template.py        # Generates the official Word manuscript template
├── test_app.py                 # Automated Unit & Integration Test Suite
│
├── models/                     # SQLAlchemy Database Models
│   ├── __init__.py             # Exports all models
│   ├── db.py                   # db = SQLAlchemy()
│   ├── admin.py                # Admin (password hashing & auth)
│   ├── registration.py         # Registration records & registration IDs
│   ├── submission.py           # Paper submissions, file paths & statuses
│   ├── speaker.py              # Keynote & invited speakers
│   ├── contact.py              # Inquiries from contact form
│   ├── track.py                # Conference research tracks & topics
│   ├── dates.py                # Important dates & milestones
│   ├── schedule.py             # Conference programme sessions & venues
│   ├── fee.py                  # Registration fee categories
│   └── faq.py                  # Categorized FAQs
│
├── routes/                     # Modular Blueprints
│   ├── __init__.py             # Blueprint aggregator
│   ├── main.py                 # Public pages (/, /about, /tracks, /cfp, /speakers, /schedule, /venue, /faq)
│   ├── submission.py           # Paper submission form, success page & status tracker
│   ├── registration.py         # Delegate registration form & voucher page
│   ├── contact.py              # Contact inquiry handling
│   └── admin.py                # Admin authentication, dashboard, CRUD & CSV export
│
├── utils/                      # Helper Functions
│   ├── __init__.py             # Utility exports
│   ├── auth.py                 # @admin_required decorator
│   ├── file_handler.py         # Secure file upload & format checks
│   └── helpers.py              # Unique ID generators (Registration & Paper IDs)
│
├── templates/                  # Semantic HTML5 Jinja2 Templates
│   ├── base.html               # Master layout with top bar, navbar & footer
│   ├── index.html              # Homepage with hero canvas, tracks & keynote preview
│   ├── about.html              # Conference vision, objectives & university history
│   ├── tracks.html             # Detailed breakdown of all 6 research tracks
│   ├── call-for-papers.html    # Guidelines, review criteria & template download
│   ├── submission.html         # Manuscript submission form with drag-and-drop
│   ├── submission-success.html # Submission confirmation voucher & receipt
│   ├── submission-status.html  # Author status lookup by Paper ID & email
│   ├── registration.html       # Delegate registration form with live calculator
│   ├── registration-success.html# Delegate voucher with QR badge & print option
│   ├── speakers.html           # Keynote & invited academic profiles
│   ├── committee.html          # Patrons, Chairs, TPC, and Student Coordinators
│   ├── schedule.html           # Day 1 & Day 2 interactive agenda timeline
│   ├── fees.html               # Registration tariff matrix & bank details
│   ├── venue.html              # SNPSU campus, transit directions & hotels
│   ├── contact.html            # Contact form & secretariat directory
│   ├── faq.html                # Categorized interactive accordion FAQ
│   ├── 404.html                # Custom 404 Not Found
│   ├── 413.html                # Custom 413 File Too Large Error
│   ├── 500.html                # Custom 500 Internal Server Error
│   └── admin/                  # Organizer Management Console Templates
│       ├── base_admin.html     # Admin dashboard sidebar layout
│       ├── login.html          # Secure organizer sign-in
│       ├── dashboard.html      # Analytics overview & quick shortcuts
│       ├── registrations.html  # Registrations table, search & CSV export
│       ├── submissions.html    # Submissions review, status editor & downloads
│       ├── speakers.html       # Speaker profile CRUD
│       ├── dates.html          # Important dates editor
│       ├── tracks.html         # Research tracks editor
│       ├── schedule.html       # Day 1 & Day 2 session editor
│       └── messages.html       # Contact message inbox
│
├── static/                     # Static Assets
│   ├── css/
│   │   ├── style.css           # Core design system & SNPSU brand typography
│   │   ├── responsive.css      # Mobile & tablet media queries
│   │   └── admin.css           # Admin dashboard stylesheet
│   ├── js/
│   │   ├── main.js             # Canvas particle graph, sticky nav, accordion
│   │   ├── registration.js     # Real-time fee calculator & paper toggle
│   │   ├── submission.js       # Drag-and-drop file upload & word counter
│   │   └── admin.js            # Admin search filters & status modals
│   ├── images/
│   │   ├── snpsu_logo.webp     # Official SNPSU university logo
│   │   ├── favicon.webp        # Official university favicon
│   │   └── speakers/           # Keynote scholar portraits
│   └── downloads/
│       └── SNPSU_BDTT_2026_Paper_Template.docx # Official IEEE/Springer formatted template
│
└── uploads/                    # Dedicated File Storage
    └── papers/                 # Secure manuscript file storage
```

---

## 🚀 Getting Started

### 1. Installation

Ensure Python 3.10+ is installed:
```bash
cd "Conference website"
pip install -r requirements.txt
```

### 2. Database Initialization & Seeding

Pre-populate the database with the default admin account, 6 research tracks, important dates, keynote speakers, registration fee tiers, conference schedule items, and FAQs:
```bash
python seed_data.py
```

### 3. Generate Official Word Template

Generate the downloadable manuscript template:
```bash
python generate_template.py
```

### 4. Running the Development Server

Start the Flask application:
```bash
python app.py
```
Open your browser and navigate to:  
👉 **Public Portal**: `http://127.0.0.1:5000/`  
👉 **Admin Portal**: `http://127.0.0.1:5000/admin/login`  

---

## 🔐 Default Admin Credentials

| Parameter | Value |
|---|---|
| **Login URL** | `/admin/login` |
| **Username** | `admin` |
| **Password** | `Admin@SNPSU2026!` |

*(Passwords are securely hashed using PBKDF2/SHA256 via Werkzeug security).*

---

## 🧪 Automated Test Verification

To run the automated test suite verifying all routes, submissions, registrations, downloads, and admin features:
```bash
python test_app.py
```
*Result: 6/6 tests passing (100% OK).*
