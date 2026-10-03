from datetime import datetime
from models.db import db
from sqlalchemy.orm import deferred

class PaperSubmission(db.Model):
    __tablename__ = 'paper_submissions'

    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.String(32), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(255), nullable=False)
    track = db.Column(db.String(120), nullable=False)
    
    # Author details
    corresponding_author = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    author_count = db.Column(db.Integer, default=1)
    co_authors_info = db.Column(db.Text, nullable=True) # JSON or newline string of coauthors
    
    # File details: supports both disk path and persistent binary data for serverless runtimes
    file_path = db.Column(db.String(350), nullable=True)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size_bytes = db.Column(db.Integer, nullable=True)
    file_data = deferred(db.Column(db.LargeBinary, nullable=True))
    
    # Submission Status: Submitted, Under Review, Accepted, Rejected, Camera Ready
    status = db.Column(db.String(40), default='Submitted', nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewer_comments = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<PaperSubmission {self.paper_id} - {self.title[:30]}>'
