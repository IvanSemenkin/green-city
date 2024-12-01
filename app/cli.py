import click
from flask.cli import with_appcontext
from app import db
from app.models import User

@click.command('make-admin')
@click.argument('username')
@with_appcontext
def make_admin(username):
    """Make a user an admin by their username."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        click.echo(f'Error: User {username} not found')
        return
    
    user.is_admin = True
    db.session.commit()
    click.echo(f'Successfully made {username} an admin')
