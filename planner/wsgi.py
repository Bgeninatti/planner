from flask.cli import FlaskGroup

from planner.app import application

cli = FlaskGroup(application)

if __name__ == "__main__":
    cli()
