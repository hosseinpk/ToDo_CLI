from pathlib import Path as p
from .all_todos import is_sqlite_file
from .add_todo import db_connection
import click


def get_todo(path: str, id: str | None = None) -> bool:

    TODO_DB = p.home() / ".todo" / f"{path}.db"

    try:

        if not TODO_DB.exists():
            click.secho(f"{path} not exists", fg="yellow")
            return False

        if not is_sqlite_file(TODO_DB):
            click.secho(f"{path} is not a todo list", fg="yellow")
            return False

        conn = db_connection(f"{TODO_DB}")

        if not conn:
            return False

        cursor = conn.cursor()
        if id is None:
            get_query = f"""
            SELECT * FROM tasks ORDER BY status;
            """
            cursor.execute(get_query)
        else:
            get_query = f"""
            SELECT * FROM tasks WHERE id=(?);
            """
            cursor.execute(get_query, (id))

        all_todo = cursor.fetchall()

        for todo in all_todo:
            print(todo)
    except Exception as e:
        print(e)
    finally:
        conn.close()

    return True

if __name__ =="__main__":
    get_todo("hossein")
