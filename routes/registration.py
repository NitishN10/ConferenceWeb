import json
import random
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from models import db, Registration, RegistrationFee, PaperSubmission
from utils import generate_registration_id

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/registration', methods=['GET', 'POST'])
def register():
    fees = RegistrationFee.query.order_by(RegistrationFee.display_order).all()
    
    if request.method == 'POST':
        is_json = request.is_json
        data = request.get_json(silent=True) if is_json else request.form.to_dict()
        if not data:
            data = request.form.to_dict()

        # Extract fields supporting standard and conference form format
        name = (data.get('name') or data.get('leader_name') or '').strip()
        email = (data.get('email') or data.get('leader_email') or '').strip().lower()
        phone = (data.get('phone') or data.get('leader_phone') or '').strip()
        institution = (data.get('institution') or 'Sapthagiri NPS University (SNPSU)').strip()
        department = (data.get('department') or data.get('leader_department') or 'Computer Science & Engineering').strip()
        designation = (data.get('designation') or 'Faculty / Researcher').strip()
        participant_type = (data.get('participant_type') or 'Faculty / Academician').strip()
        country = (data.get('country') or 'India').strip()
        paper_id = (data.get('paper_id') or '').strip().upper()
        accompanying = bool(data.get('accompanying_person'))
        
        # Conference presentation fields
        paper_title = (data.get('paper_title') or data.get('project_title') or data.get('title') or '').strip()
        track = (data.get('track') or data.get('project_category') or data.get('category') or 'Big Data Analytics').strip()
        presentation_mode = (data.get('presentation_mode') or data.get('technologies') or 'In-Person (Oral Presentation)').strip()
        presentation_abstract = (data.get('presentation_abstract') or data.get('project_abstract') or data.get('abstract') or '').strip()
        co_authors = (data.get('co_authors') or data.get('mentor_name') or '').strip()
        srn = (data.get('srn') or data.get('leader_srn') or '').strip()
        semester = (data.get('semester') or data.get('leader_semester') or '').strip()

        # Co-authors / additional attendees list handling
        members_raw = data.get('team_members') or data.get('members') or '[]'
        if isinstance(members_raw, str):
            try:
                team_members_list = json.loads(members_raw)
            except Exception:
                team_members_list = []
        elif isinstance(team_members_list := members_raw, list):
            pass
        else:
            team_members_list = []

        team_members_json = json.dumps(team_members_list)

        # Payment details
        payment_mode = data.get('payment_mode') or 'Online Gateway (UPI / Cards / NetBanking)'
        transaction_ref = (data.get('transaction_ref') or data.get('transactionId') or '').strip()
        if not transaction_ref:
            transaction_ref = f"TXN_CONF_{random.randint(1000000000, 9999999999)}"
        payment_status = data.get('payment_status') or 'Confirmed'
        
        # Calculate amount if not provided
        amount_paid = (data.get('amount_paid') or data.get('amount') or '').strip()
        if not amount_paid:
            if 'Team' in participant_type or 'Project' in participant_type:
                amount_paid = '₹ 500'
            elif 'Student' in participant_type:
                amount_paid = '₹ 1,500'
            elif 'Scholar' in participant_type or 'Ph.D' in participant_type:
                amount_paid = '₹ 2,500'
            elif 'Industry' in participant_type:
                amount_paid = '₹ 5,000'
            elif 'International' in participant_type:
                amount_paid = '$ 120'
            elif 'Listener' in participant_type or 'Attendee' in participant_type:
                amount_paid = '₹ 1,000'
            else:
                amount_paid = '₹ 3,500'
                
        dietary_pref = data.get('dietary_pref', 'Standard')

        # Delegate badge / counter / project stall allocation
        desk_number = data.get('desk_number') or f"Stall P-{random.randint(10, 48)} (Expo Hall A)"

        # Strict email regex matching name12@gmail.com format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*@[a-zA-Z0-9]+([.-][a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$')

        # Validation
        errors = []
        if not name:
            errors.append('Delegate / Team Leader full name is required.')
        if not email or not EMAIL_REGEX.match(email):
            errors.append('A valid email address in the format name12@gmail.com is required for Team Leader.')
        if not phone:
            errors.append('Contact telephone or mobile number is required for Team Leader.')

        # Validate member emails if team members list is provided
        for idx, m in enumerate(team_members_list, start=2):
            m_email = (m.get('email') or '').strip().lower()
            if not m_email or not EMAIL_REGEX.match(m_email):
                errors.append(f"A valid email address in the format name12@gmail.com is required for Team Member {idx} ({m.get('name') or 'Member'}).")

        if errors:
            if is_json:
                return jsonify({'success': False, 'errors': errors}), 400
            for error in errors:
                flash(error, 'danger')
            return render_template('registration.html', fees=fees, form=data)

        try:
            reg_id = generate_registration_id()
            while Registration.query.filter_by(registration_id=reg_id).first():
                reg_id = generate_registration_id()

            new_reg = Registration(
                registration_id=reg_id,
                name=name,
                srn=srn,
                email=email,
                phone=phone,
                institution=institution,
                department=department,
                semester=semester,
                designation=designation,
                participant_type=participant_type,
                country=country,
                paper_id=paper_id if paper_id else None,
                accompanying_person=accompanying,
                project_title=paper_title if paper_title else ('Research Paper Presentation' if paper_id else ('Project Team Presentation' if 'Team' in participant_type or 'Project' in participant_type else 'Conference Delegate Attendee')),
                project_category=track,
                project_abstract=presentation_abstract,
                technologies=presentation_mode,
                mentor_name=co_authors,
                desk_number=desk_number,
                team_members_json=team_members_json,
                payment_mode=payment_mode,
                transaction_ref=transaction_ref,
                payment_status=payment_status,
                amount_paid=amount_paid,
                dietary_pref=dietary_pref
            )

            db.session.add(new_reg)
            db.session.commit()

            success_url = url_for('registration.registration_success', reg_id=reg_id)

            if is_json:
                return jsonify({
                    'success': True,
                    'registration_id': reg_id,
                    'redirect_url': success_url,
                    'registration': {
                        'id': reg_id,
                        'name': name,
                        'srn': srn,
                        'email': email,
                        'phone': phone,
                        'institution': institution,
                        'department': department,
                        'designation': designation,
                        'participant_type': participant_type,
                        'paper_id': paper_id,
                        'paper_title': paper_title,
                        'track': track,
                        'presentation_mode': presentation_mode,
                        'co_authors': co_authors,
                        'payment_status': payment_status,
                        'amount_paid': amount_paid,
                        'transaction_ref': transaction_ref,
                        'created_at': new_reg.created_at.strftime('%Y-%m-%d %H:%M')
                    }
                })

            flash(f'Registration confirmed! Your official Delegate Registration ID is {reg_id}', 'success')
            return redirect(success_url)

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration Error: {e}")
            if is_json:
                return jsonify({'success': False, 'errors': ['Failed to complete registration due to an unexpected error. Please try again.']}), 500
            flash('Failed to complete registration due to an unexpected error. Please try again.', 'danger')
            return render_template('registration.html', fees=fees, form=data)

    initial_paper_id = request.args.get('paper_id', '')
    return render_template('registration.html', fees=fees, initial_paper_id=initial_paper_id, form={})

@registration_bp.route('/registration/success/<reg_id>')
def registration_success(reg_id):
    reg = Registration.query.filter_by(registration_id=reg_id).first_or_404()
    return render_template('registration-success.html', registration=reg)

@registration_bp.route('/registration/api/<reg_id>')
def registration_api(reg_id):
    reg = Registration.query.filter_by(registration_id=reg_id).first_or_404()
    return jsonify({
        'id': reg.registration_id,
        'name': reg.name,
        'email': reg.email,
        'phone': reg.phone,
        'institution': reg.institution,
        'department': reg.department,
        'designation': reg.designation,
        'participant_type': reg.participant_type,
        'paper_id': reg.paper_id or '',
        'paper_title': reg.project_title or 'Conference Participation',
        'track': reg.project_category or 'General',
        'presentation_mode': reg.technologies or 'In-Person',
        'payment': {
            'status': reg.payment_status,
            'amount': reg.amount_paid or '₹ 3,500',
            'transactionId': reg.transaction_ref or 'TXN_CONF_VERIFIED',
            'method': reg.payment_mode
        },
        'createdAt': reg.created_at.strftime('%Y-%m-%d %H:%M')
    })
