from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from models import db, ContactMessage

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        errors = []
        if not name:
            errors.append('Your name is required.')
        if not email or '@' not in email:
            errors.append('A valid email address is required.')
        if not subject:
            errors.append('Inquiry subject is required.')
        if not message or len(message) < 10:
            errors.append('Please provide a message with at least 10 characters.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('contact.html', form=request.form)

        try:
            msg = ContactMessage(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                status='Unread'
            )
            db.session.add(msg)
            db.session.commit()

            conf_brand = current_app.config.get('CONFERENCE_BRAND_NAME', 'Saptha DataZen 2.6')
            conf_email = current_app.config.get('CONFERENCE_EMAIL', 'datazen@snpsu.edu.in')
            flash(f'Thank you for contacting the {conf_brand} Organizing Secretariat! We will respond shortly.', 'success')
            return redirect(url_for('contact.contact'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Contact Form Error: {e}")
            conf_email = current_app.config.get('CONFERENCE_EMAIL', 'datazen@snpsu.edu.in')
            flash(f'Failed to submit your message. Please reach us directly via email at {conf_email}.', 'danger')
            return render_template('contact.html', form=request.form)

    return render_template('contact.html', form={})
