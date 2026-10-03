import os
from flask import Flask, render_template
from config import Config
from models import db
from routes import main_bp, submission_bp, registration_bp, contact_bp, admin_bp
from seed_data import init_db_and_seed

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # In local development, ensure required directories exist if filesystem is writable.
    # Never attempt to write to /var/task/instance or assume filesystem is writable on Vercel.
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
            os.makedirs(os.path.join(app.root_path, 'static', 'downloads'), exist_ok=True)
        except OSError:
            # Read-only filesystem or permissions restricted; skip directory creation
            pass

    # Initialize extensions
    db.init_app(app)

    # Initialize database tables and populate initial reference data if database is empty
    init_db_and_seed(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(submission_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    # Context processor to make conference branding constants available in all templates
    @app.context_processor
    def inject_conference_info():
        return {
            'CONF_NAME': app.config['CONFERENCE_NAME'],
            'CONF_ACRONYM': app.config['CONFERENCE_ACRONYM'],
            'CONF_BRAND': app.config.get('CONFERENCE_BRAND_NAME', 'ICBDTT-2026'),
            'CONF_THEME': app.config['CONFERENCE_THEME'],
            'CONF_HOST': app.config['HOST_INSTITUTION'],
            'CONF_LOCATION': app.config['HOST_LOCATION'],
            'CONF_CAMPUS': app.config['HOST_CAMPUS'],
            'CONF_EMAIL': app.config['CONFERENCE_EMAIL'],
            'CONF_PHONE': app.config['CONFERENCE_PHONE'],
            'CONF_DATE': app.config['CONFERENCE_DATE'],
            'CONF_TIMING': app.config.get('CONFERENCE_TIMING', '10:00 AM – 4:00 PM'),
            'CONF_VENUE': app.config['VENUE_NAME'],
            'CONF_FEE': app.config['REGISTRATION_FEE_PLACEHOLDER'],
            'CURRENT_YEAR': 2026
        }

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    conf_brand = app.config.get('CONFERENCE_BRAND_NAME', 'ICBDTT-2026')
    print(f"Starting {conf_brand} Conference Portal on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=True)
