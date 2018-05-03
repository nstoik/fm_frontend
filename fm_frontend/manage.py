import click
from flask.cli import FlaskGroup

from fm_frontend.app import create_app


def create_fm_frontend(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_fm_frontend)
def cli():
    """Main entry point."""
