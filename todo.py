import click
import logging
from pathlib import Path
from create import create_db
from all_todos import all_todos


BASE_DIR = Path.home() / ".todo"
LOG_FILE = BASE_DIR / "todo.log"
logging.basicConfig(
    
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


@click.group(invoke_without_command=True) #bunch of commands, if add invoke_without_command=True without any subcommand cli() run and call
@click.option("-a","--all", "show_all", is_flag=True , help ="show all todo lists" ) #show_all is a function parameter, -a and --all store in show_all
@click.pass_context # Allow access to context inside a function 
def cli(ctx,show_all): # ctx -> Current execution state holder
    """
    Simple ToDo CLI app.
    
    Use -a or --all for show all todo lists
    
    """
    if ctx.invoked_subcommand is None and not show_all:
        click.echo(ctx.get_help())
        return
    
    if show_all and ctx.invoked_subcommand is None:
        todos = all_todos()
        if todos:
            click.secho("Available todo lists:" , fg="cyan")
            for t in todos:
                click.echo(f"  - {t}")
        else:
            click.secho("No Todo list found",fg="yellow") 


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
    
