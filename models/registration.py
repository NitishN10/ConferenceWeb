from datetime import datetime
from models.db import db

class Registration(db.Model):
    __tablename__ = 'registrations'

    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    participant_type = db.Column(db.String(80), nullable=False) # Student, Research Scholar, Faculty, Industry, International
    country = db.Column(db.String(80), nullable=False)
    paper_id = db.Column(db.String(32), nullable=True, index=True) # Linked Paper ID if presenting
    accompanying_person = db.Column(db.Boolean, default=False)
    payment_mode = db.Column(db.String(100), default='NEFT/UPI/Wire Transfer')
    transaction_ref = db.Column(db.String(100), nullable=True)
    payment_status = db.Column(db.String(50), default='Confirmed') # Confirmed, Pending
    amount_paid = db.Column(db.String(50), nullable=True)
    dietary_pref = db.Column(db.String(50), default='Standard')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, server_default=db.func.now())
    # Project & Student Team Fields
    srn = db.Column(db.String(50), nullable=True) # Leader SRN / USN
    semester = db.Column(db.String(50), nullable=True) # Leader Semester
    project_title = db.Column(db.Text, nullable=True)
    project_category = db.Column(db.String(255), nullable=True)
    project_abstract = db.Column(db.Text, nullable=True)
    technologies = db.Column(db.Text, nullable=True)
    mentor_name = db.Column(db.String(255), nullable=True)
    desk_number = db.Column(db.String(100), nullable=True, default='Allocated on Event Day')
    team_members_json = db.Column(db.Text, nullable=True) # JSON array of team members

    @property
    def team_members(self):
        import json
        if self.team_members_json:
            try:
                return json.loads(self.team_members_json)
            except Exception:
                return []
        return []

    def __repr__(self):
        return f'<Registration {self.registration_id} - {self.name}>'

