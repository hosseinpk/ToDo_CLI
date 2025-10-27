import click
import logging
from pathlib import Path
from create import create_db


BASE_DIR = Path.home() / ".todo"
LOG_FILE = BASE_DIR / "todo.log"
logging.basicConfig(
    
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


@click.group()

def cli():
    """Simple ToDo CLI app using SQLite."""
    pass


@cli.command("create")
@click.argument("name", metavar="<db_name>")
@click.option("--force",is_flag=True,help="Overwrite the existing database if it already exists.")
def create(name:str , force:bool) -> str:
    """
    Create a new ToDo list SQLite database.

    Example:\n
        python todo.py create mylist\n
        python todo.py create mylist --force
    """
    db_path = Path.home() / ".todo" / f"{name}.db"
    
    if db_path.exists():
        if not force:
            click.secho(f" Database '{name}.db' already exists.", fg="yellow")
            logging.warning(f" Database '{name}.db' already exists.")
            click.secho("   Use --force to overwrite it.", fg="yellow")
            raise click.Abort()
        else:
            click.echo(f"remove existing file {name}")
            logging.warning(f"remove existing file {name}")
            db_path.unlink()
            
    try:
        create_db(name)
        click.secho(f" {name}.db created successfully in ~/.todo", fg="green")
        logging.info(f" {name}.db created successfully in ~/.todo")
    except Exception as e:
        click.secho(f" Error creating database: {e}", fg="red")
        logging.error(f" Error creating database: {e}")
        raise click.Abort()

if __name__ == "__main__":
    cli()
    
