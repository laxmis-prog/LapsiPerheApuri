import os
from dotenv import load_dotenv
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Permission
import unittest

# Load environment variables from .env file
load_dotenv()

# Initialize the app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Initialize migration support
migrate = Migrate(app, db)

# Only register the admin blueprint once
from app.admin import admin  # Import the admin blueprint
# Check if the blueprint is already registered
if 'admin' not in app.blueprints:
    app.register_blueprint(admin, url_prefix='/admin')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)

@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

# Optional CLI command to make a user an admin
@app.cli.command()
@click.argument('email')
def create_admin(email):
    """Make a user an admin."""
    user = User.query.filter_by(email=email).first()
    if user is None:
        print(f"User with email {email} not found.")
        return
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role is None:
        print("Admin role not found.")
        return
    user.role_id = admin_role.id  # Set the role of the user to 'admin'
    db.session.commit()
    print(f"User {email} is now an admin.")