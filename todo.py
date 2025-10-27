import click
import sqlite3
from pathlib import Path
from create import create_db


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
            click.secho("   Use --force to overwrite it.", fg="yellow")
            raise click.Abort()
        else:
            click.echo(f"remove existing file {name}")
            db_path.unlink()
            
    try:
        create_db(name)
        click.secho(f" {name}.db created successfully in ~/.todo", fg="green")
    except Exception as e:
        click.secho(f" Error creating database: {e}", fg="red")
        raise click.Abort()

if __name__ == "__main__":
    cli()
    
