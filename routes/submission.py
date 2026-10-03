import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort
from models import db, PaperSubmission, ConferenceTrack
from utils import allowed_file, save_paper_file, generate_paper_id

submission_bp = Blueprint('submission', __name__)

@submission_bp.route('/submission', methods=['GET', 'POST'])
def submit_paper():
    tracks = ConferenceTrack.query.order_by(ConferenceTrack.track_number).all()

    if request.method == 'POST':
        # 1. Author Details
        corresponding_author = request.form.get('corresponding_author', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        institution = request.form.get('institution', '').strip()
        department = request.form.get('department', '').strip()
        country = request.form.get('country', '').strip()
        author_count = request.form.get('author_count', '1').strip()
        co_authors_info = request.form.get('co_authors_info', '').strip()

        # 2. Paper Details
        title = request.form.get('title', '').strip()
        abstract = request.form.get('abstract', '').strip()
        keywords = request.form.get('keywords', '').strip()
        track = request.form.get('track', '').strip()

        # Validation
        errors = []
        if not corresponding_author:
            errors.append('Corresponding author name is required.')
        if not email or '@' not in email:
            errors.append('A valid author email address is required.')
        if not phone:
            errors.append('Contact phone number is required.')
        if not institution:
            errors.append('Affiliated institution / organization is required.')
        if not country:
            errors.append('Country is required.')
        if not title:
            errors.append('Paper title is required.')
        if not abstract:
            errors.append('Abstract is required.')
        elif len(abstract.split()) < 30:
            errors.append('Abstract must be at least 30 words in length.')
        if not keywords:
            errors.append('At least 3 comma-separated keywords are required.')
        if not track:
            errors.append('Please select an appropriate conference track.')

        # 3. File Upload Validation
        if 'paper_file' not in request.files:
            errors.append('Please select a paper manuscript file to upload.')
        else:
            file = request.files['paper_file']
            if file.filename == '':
                errors.append('No file was selected.')
            elif not allowed_file(file.filename):
                errors.append('Invalid file format. Only PDF, DOC, and DOCX manuscripts are accepted.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('submission.html', tracks=tracks, form=request.form)

        try:
            # Generate unique Paper ID
            paper_id = generate_paper_id()
            while PaperSubmission.query.filter_by(paper_id=paper_id).first():
                paper_id = generate_paper_id()

            # Save file to uploads folder / persist bytes in database
            file = request.files['paper_file']
            upload_dir = current_app.config['UPLOAD_FOLDER']
            full_path, original_filename, file_size, file_bytes = save_paper_file(file, upload_dir, paper_id)

            # Convert author count
            try:
                author_count_int = int(author_count)
            except ValueError:
                author_count_int = 1

            # Create PaperSubmission entity
            new_submission = PaperSubmission(
                paper_id=paper_id,
                title=title,
                abstract=abstract,
                keywords=keywords,
                track=track,
                corresponding_author=corresponding_author,
                email=email,
                phone=phone,
                institution=institution,
                department=department,
                country=country,
                author_count=author_count_int,
                co_authors_info=co_authors_info,
                file_path=full_path,
                original_filename=original_filename,
                file_size_bytes=file_size,
                file_data=file_bytes,
                status='Submitted'
            )

            db.session.add(new_submission)
            db.session.commit()

            flash(f'Your paper has been successfully submitted! Paper ID: {paper_id}', 'success')
            return redirect(url_for('submission.submission_success', paper_id=paper_id))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Submission Error: {e}")
            flash('An unexpected error occurred while processing your submission. Please try again.', 'danger')
            return render_template('submission.html', tracks=tracks, form=request.form)

    return render_template('submission.html', tracks=tracks, form={})

@submission_bp.route('/submission/success/<paper_id>')
def submission_success(paper_id):
    submission = PaperSubmission.query.filter_by(paper_id=paper_id).first_or_404()
    return render_template('submission-success.html', submission=submission)

@submission_bp.route('/submission/status', methods=['GET', 'POST'])
def track_status():
    status_result = None
    searched = False
    
    if request.method == 'POST':
        searched = True
        paper_id = request.form.get('paper_id', '').strip()
        email = request.form.get('email', '').strip().lower()
        
        if paper_id and email:
            status_result = PaperSubmission.query.filter(
                PaperSubmission.paper_id.ilike(paper_id),
                PaperSubmission.email.ilike(email)
            ).first()
            if not status_result:
                flash('No paper matching the provided Paper ID and Author Email was found.', 'warning')
        else:
            flash('Please enter both your Paper ID and Registered Author Email.', 'danger')
            
    return render_template('submission-status.html', result=status_result, searched=searched)
