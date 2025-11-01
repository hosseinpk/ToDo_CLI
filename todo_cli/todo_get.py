from pathlib import Path as p
from todo_cli.all_todos import is_sqlite_file
from todo_cli.add_todo import db_connection
import click


def color_status(status):
    colors = {"pending": "yellow", "done": "green", "ongoing": "cyan"}
    return click.style(status, fg=colors.get(status, "white"))


def get_todo(path: str, id: str | None = None) -> bool:

    TODO_DB = p.home() / ".todo" / f"{path}.db"

    try:

        if not TODO_DB.exists():
            click.secho(f"{path} not exists", fg="yellow")
            return False

        if not is_sqlite_file(TODO_DB):
            click.secho(f"{path} is not a todo list", fg="yellow")
            return False

        conn = db_connection(str(TODO_DB))
        if not conn:
            return False

        cursor = conn.cursor()

        if id is None:
            cursor.execute("SELECT * FROM tasks ORDER BY status;")
            todos = cursor.fetchall()

            if not todos:
                click.secho("No todos found.", fg="yellow")
                return True

            # Table header
            click.secho(f"{'ID':<4} {'Title':<20} {'Status':<12} {'Updated'}")
            click.secho("-" * 60)

            for t in todos:
                id, title, desc, status, created, updated = t
                click.echo(
                    f"{str(id):<4} {title:<20} {color_status(status):<12} {updated}"
                )

        else:
            cursor.execute("SELECT * FROM tasks WHERE id=(?);", (id,))
            todo = cursor.fetchone()

            if not todo:
                click.secho("Todo not found.", fg="red")
                return False

            id, title, desc, status, created, updated = todo

            click.secho(
                f"{'ID':<4} {'Title':<20} {'Description':<25} {'Status':<12} {'Updated'}"
            )
            click.secho("-" * 90)
            click.echo(
                f"{str(id):<4} {title:<20} {desc:<25} {color_status(status):<12} {updated}"
            )
            return True

    except Exception as e:
        click.secho(str(e), fg="red")
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    get_todo()
