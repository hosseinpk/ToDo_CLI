import click
import logging
from pathlib import Path
from create import create_db


LOG_DIR = Path.home() / ".todo"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "todo.log"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(console_handler)


@click.group()
def cli():
    """Simple ToDo CLI app using SQLite."""
    pass


@cli.command("create")
@click.argument("name", metavar="<db_name>")
@click.option("--force", is_flag=True, help="Overwrite if it exists.")
def create(name: str, force: bool):
    db_path = Path.home() / ".todo" / f"{name}.db"

    if db_path.exists():
        if not force:
            click.secho(f" Database '{name}.db' already exists.", fg="yellow")
            logging.warning(f"Database already exists: {db_path}")
            raise click.Abort()
        else:
            click.echo(f"Removing existing file {name}.db")
            logging.info(f"Removed existing file: {db_path}")
            db_path.unlink()

    try:
        create_db(name)
        click.secho(f" {name}.db created successfully in ~/.todo", fg="green")
        logging.info(f"Created new database: {db_path}")
    except Exception as e:
        click.secho(f" Error creating database: {e}", fg="red")
        logging.error(f"Error creating database {db_path}: {e}")
        raise click.Abort()


if __name__ == "__main__":
    cli()
