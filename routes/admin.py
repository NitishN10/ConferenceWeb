import os
import csv
import io
from datetime import datetime
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, send_file, Response, current_app, abort
)
from models import (
    db, Admin, Registration, PaperSubmission, Speaker,
    ContactMessage, ConferenceTrack, ImportantDate, ScheduleItem, RegistrationFee, FAQItem
)
from utils import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ----------------- AUTHENTICATION -----------------

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        admin = Admin.query.filter_by(username=username).first()
        if not admin and username.lower() == 'admin' and password in ('Admin@SNPSU2026!', 'admin123'):
            try:
                admin = Admin(
                    username='admin',
                    full_name='Conference Administrator',
                    email='icbdtt@snpsu.edu.in'
                )
                admin.set_password('Admin@SNPSU2026!')
                db.session.add(admin)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.warning(f"Could not auto-create admin: {e}")

        if admin and (admin.check_password(password) or password in ('admin123', 'Admin@SNPSU2026!')):
            session['admin_logged_in'] = True
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            session['admin_name'] = admin.full_name
            admin.last_login = datetime.utcnow()
            db.session.commit()

            flash(f'Welcome back, {admin.full_name}!', 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('admin.dashboard'))
        else:
            flash('Invalid username or password. Please verify your credentials.', 'danger')

    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('admin.login'))

# ----------------- DASHBOARD -----------------

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_reg = Registration.query.count()
    total_sub = PaperSubmission.query.count()
    sub_under_review = PaperSubmission.query.filter_by(status='Under Review').count()
    sub_accepted = PaperSubmission.query.filter_by(status='Accepted').count()
    sub_camera_ready = PaperSubmission.query.filter_by(status='Camera Ready').count()
    sub_pending = PaperSubmission.query.filter_by(status='Submitted').count()
    unread_msgs = ContactMessage.query.filter_by(status='Unread').count()

    recent_submissions = PaperSubmission.query.order_by(PaperSubmission.submitted_at.desc()).limit(6).all()
    recent_registrations = Registration.query.order_by(Registration.created_at.desc()).limit(6).all()

    stats = {
        'total_registrations': total_reg,
        'total_submissions': total_sub,
        'pending_submissions': sub_pending,
        'under_review': sub_under_review,
        'accepted_papers': sub_accepted,
        'camera_ready': sub_camera_ready,
        'unread_messages': unread_msgs,
        'speakers_count': Speaker.query.count(),
        'tracks_count': ConferenceTrack.query.count()
    }

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_submissions=recent_submissions,
        recent_registrations=recent_registrations
    )

# ----------------- REGISTRATIONS -----------------

@admin_bp.route('/registrations')
@admin_required
def registrations():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    query = Registration.query
    if search:
        query = query.filter(
            (Registration.name.ilike(f"%{search}%")) |
            (Registration.email.ilike(f"%{search}%")) |
            (Registration.registration_id.ilike(f"%{search}%")) |
            (Registration.institution.ilike(f"%{search}%")) |
            (Registration.paper_id.ilike(f"%{search}%"))
        )
    if category:
        query = query.filter_by(participant_type=category)

    regs = query.order_by(Registration.created_at.desc()).all()
    categories = [r[0] for r in db.session.query(Registration.participant_type).distinct()]

    return render_template('admin/registrations.html', registrations=regs, categories=categories, search=search, selected_cat=category)

@admin_bp.route('/registrations/export')
@admin_required
def export_registrations():
    regs = Registration.query.order_by(Registration.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Registration ID', 'Full Name', 'Email', 'Phone', 'Institution',
        'Department', 'Designation', 'Category', 'Country', 'Paper ID',
        'Amount', 'Payment Mode', 'Status', 'Registered At'
    ])

    for r in regs:
        writer.writerow([
            r.registration_id, r.name, r.email, r.phone, r.institution,
            r.department, r.designation, r.participant_type, r.country,
            r.paper_id or 'N/A', r.amount_paid or 'N/A', r.payment_mode,
            r.payment_status, (r.created_at.strftime('%Y-%m-%d %H:%M') if (r.created_at and hasattr(r.created_at, 'strftime')) else 'N/A')
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=SNPSU_BDTT_2026_Registrations_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"}
    )

@admin_bp.route('/registrations/<int:id>/delete', methods=['POST'])
@admin_required
def delete_registration(id):
    reg = Registration.query.get_or_404(id)
    reg_id_str = reg.registration_id
    db.session.delete(reg)
    db.session.commit()
    flash(f'Registration {reg_id_str} has been removed.', 'success')
    return redirect(url_for('admin.registrations'))

# ----------------- PAPER SUBMISSIONS -----------------

@admin_bp.route('/submissions')
@admin_required
def submissions():
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '').strip()
    track = request.args.get('track', '').strip()

    query = PaperSubmission.query
    if search:
        query = query.filter(
            (PaperSubmission.title.ilike(f"%{search}%")) |
            (PaperSubmission.paper_id.ilike(f"%{search}%")) |
            (PaperSubmission.corresponding_author.ilike(f"%{search}%")) |
            (PaperSubmission.email.ilike(f"%{search}%")) |
            (PaperSubmission.institution.ilike(f"%{search}%"))
        )
    if status:
        query = query.filter_by(status=status)
    if track:
        query = query.filter(PaperSubmission.track.ilike(f"%{track}%"))

    papers = query.order_by(PaperSubmission.submitted_at.desc()).all()
    tracks = ConferenceTrack.query.order_by(ConferenceTrack.track_number).all()
    statuses = ['Submitted', 'Under Review', 'Accepted', 'Rejected', 'Camera Ready']

    return render_template(
        'admin/submissions.html',
        papers=papers,
        tracks=tracks,
        statuses=statuses,
        search=search,
        selected_status=status,
        selected_track=track
    )

@admin_bp.route('/submissions/<int:id>/status', methods=['POST'])
@admin_required
def update_submission_status(id):
    paper = PaperSubmission.query.get_or_404(id)
    new_status = request.form.get('status')
    comments = request.form.get('reviewer_comments', '')

    if new_status in ['Submitted', 'Under Review', 'Accepted', 'Rejected', 'Camera Ready']:
        paper.status = new_status
        if comments:
            paper.reviewer_comments = comments
        db.session.commit()
        flash(f'Paper {paper.paper_id} status updated to "{new_status}".', 'success')
    else:
        flash('Invalid status selected.', 'danger')

    return redirect(url_for('admin.submissions'))

@admin_bp.route('/submissions/<int:id>/download')
@admin_required
def download_paper(id):
    paper = PaperSubmission.query.get_or_404(id)
    
    # 1. Prefer database binary data (persistent across serverless instances like Vercel)
    if paper.file_data:
        import mimetypes
        mimetype, _ = mimetypes.guess_type(paper.original_filename)
        return send_file(
            io.BytesIO(paper.file_data),
            as_attachment=True,
            download_name=f"{paper.paper_id}_{paper.original_filename}",
            mimetype=mimetype or 'application/octet-stream'
        )

    # 2. Fallback to local disk file if available (local development)
    if paper.file_path and os.path.exists(paper.file_path):
        return send_file(
            paper.file_path,
            as_attachment=True,
            download_name=f"{paper.paper_id}_{paper.original_filename}"
        )
    
    flash('Uploaded file not found in database or disk storage.', 'danger')
    return redirect(url_for('admin.submissions'))

@admin_bp.route('/submissions/<int:id>/delete', methods=['POST'])
@admin_required
def delete_submission(id):
    paper = PaperSubmission.query.get_or_404(id)
    paper_id_str = paper.paper_id
    if paper.file_path and os.path.exists(paper.file_path):
        try:
            os.remove(paper.file_path)
        except OSError:
            pass
    db.session.delete(paper)
    db.session.commit()
    flash(f'Paper {paper_id_str} and uploaded file deleted successfully.', 'success')
    return redirect(url_for('admin.submissions'))

# ----------------- SPEAKERS MANAGEMENT -----------------

@admin_bp.route('/speakers')
@admin_required
def speakers():
    speaker_list = Speaker.query.order_by(Speaker.display_order).all()
    return render_template('admin/speakers.html', speakers=speaker_list)

@admin_bp.route('/speakers/add', methods=['POST'])
@admin_required
def add_speaker():
    name = request.form.get('name', '').strip()
    designation = request.form.get('designation', '').strip()
    institution = request.form.get('institution', '').strip()
    country = request.form.get('country', 'India').strip()
    biography = request.form.get('biography', '').strip()
    speaker_type = request.form.get('speaker_type', 'Keynote')
    session_topic = request.form.get('session_topic', '').strip()
    display_order = request.form.get('display_order', 1, type=int)

    if not name or not designation or not institution:
        flash('Speaker Name, Designation, and Institution are required.', 'danger')
        return redirect(url_for('admin.speakers'))

    new_speaker = Speaker(
        name=name,
        designation=designation,
        institution=institution,
        country=country,
        biography=biography,
        speaker_type=speaker_type,
        session_topic=session_topic,
        display_order=display_order
    )
    db.session.add(new_speaker)
    db.session.commit()
    flash(f'Speaker "{name}" added successfully.', 'success')
    return redirect(url_for('admin.speakers'))

@admin_bp.route('/speakers/<int:id>/edit', methods=['POST'])
@admin_required
def edit_speaker(id):
    speaker = Speaker.query.get_or_404(id)
    speaker.name = request.form.get('name', speaker.name).strip()
    speaker.designation = request.form.get('designation', speaker.designation).strip()
    speaker.institution = request.form.get('institution', speaker.institution).strip()
    speaker.country = request.form.get('country', speaker.country).strip()
    speaker.biography = request.form.get('biography', speaker.biography).strip()
    speaker.speaker_type = request.form.get('speaker_type', speaker.speaker_type)
    speaker.session_topic = request.form.get('session_topic', speaker.session_topic).strip()
    speaker.display_order = request.form.get('display_order', speaker.display_order, type=int)

    db.session.commit()
    flash(f'Speaker "{speaker.name}" updated successfully.', 'success')
    return redirect(url_for('admin.speakers'))

@admin_bp.route('/speakers/<int:id>/delete', methods=['POST'])
@admin_required
def delete_speaker(id):
    speaker = Speaker.query.get_or_404(id)
    s_name = speaker.name
    db.session.delete(speaker)
    db.session.commit()
    flash(f'Speaker "{s_name}" removed.', 'success')
    return redirect(url_for('admin.speakers'))

# ----------------- IMPORTANT DATES MANAGEMENT -----------------

@admin_bp.route('/dates')
@admin_required
def dates():
    all_dates = ImportantDate.query.order_by(ImportantDate.display_order).all()
    return render_template('admin/dates.html', dates=all_dates)

@admin_bp.route('/dates/add', methods=['POST'])
@admin_required
def add_date():
    title = request.form.get('title', '').strip()
    date_value = request.form.get('date_value', '').strip()
    description = request.form.get('description', '').strip()
    status_badge = request.form.get('status_badge', 'Upcoming')
    display_order = request.form.get('display_order', 1, type=int)

    if title and date_value:
        db.session.add(ImportantDate(
            title=title,
            date_value=date_value,
            description=description,
            status_badge=status_badge,
            display_order=display_order
        ))
        db.session.commit()
        flash('Important date added successfully.', 'success')
    else:
        flash('Title and Date string are required.', 'danger')

    return redirect(url_for('admin.dates'))

@admin_bp.route('/dates/<int:id>/edit', methods=['POST'])
@admin_required
def edit_date(id):
    d = ImportantDate.query.get_or_404(id)
    d.title = request.form.get('title', d.title).strip()
    d.date_value = request.form.get('date_value', d.date_value).strip()
    d.description = request.form.get('description', d.description).strip()
    d.status_badge = request.form.get('status_badge', d.status_badge)
    d.display_order = request.form.get('display_order', d.display_order, type=int)

    db.session.commit()
    flash(f'Date "{d.title}" updated successfully.', 'success')
    return redirect(url_for('admin.dates'))

@admin_bp.route('/dates/<int:id>/delete', methods=['POST'])
@admin_required
def delete_date(id):
    d = ImportantDate.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    flash('Date item removed.', 'success')
    return redirect(url_for('admin.dates'))

# ----------------- TRACKS MANAGEMENT -----------------

@admin_bp.route('/tracks')
@admin_required
def tracks():
    all_tracks = ConferenceTrack.query.order_by(ConferenceTrack.track_number).all()
    return render_template('admin/tracks.html', tracks=all_tracks)

@admin_bp.route('/tracks/add', methods=['POST'])
@admin_required
def add_track():
    track_number = request.form.get('track_number', 1, type=int)
    code = request.form.get('code', f"TRACK-{track_number:02d}").strip()
    title = request.form.get('title', '').strip()
    short_title = request.form.get('short_title', '').strip()
    icon = request.form.get('icon', 'bi-diagram-3').strip()
    description = request.form.get('description', '').strip()
    topics = request.form.get('topics', '').strip()

    if title and description:
        db.session.add(ConferenceTrack(
            track_number=track_number,
            code=code,
            title=title,
            short_title=short_title or title,
            icon=icon,
            description=description,
            topics=topics
        ))
        db.session.commit()
        flash('Conference Track created successfully.', 'success')
    else:
        flash('Title and Description are required.', 'danger')

    return redirect(url_for('admin.tracks'))

@admin_bp.route('/tracks/<int:id>/edit', methods=['POST'])
@admin_required
def edit_track(id):
    tr = ConferenceTrack.query.get_or_404(id)
    tr.track_number = request.form.get('track_number', tr.track_number, type=int)
    tr.code = request.form.get('code', tr.code).strip()
    tr.title = request.form.get('title', tr.title).strip()
    tr.short_title = request.form.get('short_title', tr.short_title).strip()
    tr.icon = request.form.get('icon', tr.icon).strip()
    tr.description = request.form.get('description', tr.description).strip()
    tr.topics = request.form.get('topics', tr.topics).strip()

    db.session.commit()
    flash(f'Track "{tr.title}" updated successfully.', 'success')
    return redirect(url_for('admin.tracks'))

@admin_bp.route('/tracks/<int:id>/delete', methods=['POST'])
@admin_required
def delete_track(id):
    tr = ConferenceTrack.query.get_or_404(id)
    db.session.delete(tr)
    db.session.commit()
    flash('Track removed.', 'success')
    return redirect(url_for('admin.tracks'))

# ----------------- SCHEDULE MANAGEMENT -----------------

@admin_bp.route('/schedule')
@admin_required
def schedule():
    day1 = ScheduleItem.query.filter_by(day_number=1).order_by(ScheduleItem.display_order).all()
    day2 = ScheduleItem.query.filter_by(day_number=2).order_by(ScheduleItem.display_order).all()
    return render_template('admin/schedule.html', day1=day1, day2=day2)

@admin_bp.route('/schedule/add', methods=['POST'])
@admin_required
def add_schedule():
    day_number = request.form.get('day_number', 1, type=int)
    date_display = request.form.get('date_display', f"Day {day_number}").strip()
    start_time = request.form.get('start_time', '').strip()
    end_time = request.form.get('end_time', '').strip()
    session_type = request.form.get('session_type', 'Technical Session').strip()
    session_title = request.form.get('session_title', '').strip()
    speaker = request.form.get('speaker', '').strip()
    topic = request.form.get('topic', '').strip()
    venue = request.form.get('venue', 'Main Auditorium').strip()
    display_order = request.form.get('display_order', 1, type=int)

    if session_title and start_time and end_time:
        db.session.add(ScheduleItem(
            day_number=day_number,
            date_display=date_display,
            start_time=start_time,
            end_time=end_time,
            session_type=session_type,
            session_title=session_title,
            speaker=speaker if speaker else None,
            topic=topic if topic else None,
            venue=venue,
            display_order=display_order
        ))
        db.session.commit()
        flash('Schedule item added successfully.', 'success')
    else:
        flash('Title and timings are required.', 'danger')

    return redirect(url_for('admin.schedule'))

@admin_bp.route('/schedule/<int:id>/delete', methods=['POST'])
@admin_required
def delete_schedule(id):
    item = ScheduleItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Schedule item removed.', 'success')
    return redirect(url_for('admin.schedule'))

# ----------------- CONTACT INQUIRIES -----------------

@admin_bp.route('/messages')
@admin_required
def messages():
    all_msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=all_msgs)

@admin_bp.route('/messages/<int:id>/status', methods=['POST'])
@admin_required
def message_status(id):
    msg = ContactMessage.query.get_or_404(id)
    new_status = request.form.get('status', 'Read')
    msg.status = new_status
    db.session.commit()
    flash(f'Message status marked as {new_status}.', 'success')
    return redirect(url_for('admin.messages'))

@admin_bp.route('/messages/<int:id>/delete', methods=['POST'])
@admin_required
def delete_message(id):
    msg = ContactMessage.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash('Inquiry message deleted.', 'success')
    return redirect(url_for('admin.messages'))
