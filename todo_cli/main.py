import click
import logging
from pathlib import Path as p
from .create import create_db
from .all_todos import all_todos
from .delete_todo_list import delete_todo
from .rename import rename_todo_list
from .add_todo import add_todo

BASE_DIR = p.home() / ".todo"
LOG_FILE = BASE_DIR / "todo.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
click.secho

@click.group(
    invoke_without_command=True
)  # bunch of commands, if add invoke_without_command=True without any subcommand cli() run and call
@click.option(
    "-a", "--all", "show_all", is_flag=True, help="show all todo lists"
)  # show_all is a function parameter, -a and --all store in show_all
@click.pass_context  # Allow access to context inside a function
def cli(ctx, show_all):  # ctx -> Current execution state holder
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
            click.secho("Available todo lists:", fg="cyan")
            for t in todos:
                click.echo(f"  - {t}")
        else:
            click.secho("No Todo list found", fg="yellow")


@cli.command("create")
@click.argument("name", metavar="<todo_list_name>")
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite the existing database if it already exists.",
)
def create_cli(name: str, force: bool):
    """
    Create a new ToDo list SQLite database.

    Example:\n
        todo create mylist\n
        todo create mylist --force
    """
    db_path = p.home() / ".todo" / f"{name}.db"

    if db_path.exists():
        if not force:
            click.secho(f" Database '{name}' already exists.", fg="yellow")
            logging.warning(f" Database '{name}' already exists.")
            click.secho("   Use --force to overwrite it.", fg="yellow")
            raise click.Abort()
        else:
            click.echo(f"remove existing file {name}")
            logging.warning(f"remove existing file {name}")
            db_path.unlink()

    try:
        create_db(name)
        click.secho(f" {name} created successfully in ~/.todo", fg="green")
        logging.info(f" {name}.db created successfully in ~/.todo")
    except Exception as e:
        click.secho(f" Error creating database: {e}", fg="red")
        logging.error(f" Error creating database: {e}")
        raise click.Abort()


@cli.command("delete")
@click.argument("name", metavar="<todo_list_name>")
@click.option("--force", is_flag=True, help="force delete a todo list")
def delete_cli(name: str, force: bool):
    """
    Delete an existing ToDo list database.

    Example:\n
        todo delete mylist\n
        todo delete mylist --force
    """
    TODO_FILE = p.home() / ".todo" / f"{name}.db"
    if not TODO_FILE.exists():
        click.secho(f"{name} todo list doesn't exist", fg="yellow")
        return
    if force:
        delete_todo(name)
        click.secho(f"{name} todo list deleted successfully", fg="green")
        logging.warning(f"{name} todo list deleted successfully")
    else:
        confirm = click.confirm(
            f"Are you sure you want to delete {name} todo list?",
            default=False,
            show_default=True,
        )
        if not confirm:
            click.secho(f"Deletion canceled for '{name}", fg="yellow")
            logging.info(f"Deletion canceled for '{name}")
            return

        delete_todo(name)
        click.secho(f"{name} todo list deleted successfully", fg="green")
        logging.info(f"{name} todo list deleted successfully")


@cli.command("rename")
@click.argument("old_name", metavar="<old_name>")
@click.argument("new_name", metavar="<old_name>")
def rename_cli(old_name: str, new_name: str) -> bool:
    """
    Rename an existing ToDo list.

    Example:\n
        todo rename old_name new_name\n

    """
    if rename_todo_list(old_name, new_name):

        return True
    
@cli.command("add")
@click.argument("task_name", metavar="<task_name>")
@click.option("-l","--list","list_name",required=True,metavar="<list_name>",help="Todo list to add the task to")
@click.option("-d","--desc","desc",default=None, metavar="<description>",help="add description to the task")
def add_cli(task_name:str,list_name:str,desc:str | None) -> bool:
    """
    Add a task to a  list.

    Example:\n
        todo add task_name -l list_name -d descripton\n
        todo add task_name --list list_name --description descripton\n


    """
    TODO_LIST = p.home() / ".todo" / f"{list_name}.db"
    
    if not list_name:
        click.secho("you should select a list",fg="yellow")
        return False
    if not task_name:
        click.secho("you should specify a name for task",fg="yellow")
        return False

    if not TODO_LIST.exists():
        click.secho("no list found",fg="yellow")
        return False
    
    if add_todo(list_name,task_name,desc):

        return True
    
    
if __name__ == "__main__":
    cli()
