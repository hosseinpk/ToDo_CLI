from todo_cli.todo_add import db_connection
from todo_cli.all_todos import is_sqlite_file
import logging
import click
from datetime import datetime
from todo_cli.main import Main
from todo_cli.create import Status

main_cfg = Main()

def todo_update(todo_name: str , todo_id : str , todo_status : str | None = None,todo_desc: str | None = None) -> bool:

    TODO_DB = main_cfg.TODO / f"{todo_name}.db"

    conn = None
    try:
        if not TODO_DB.exists():
            click.secho(f"{todo_name} not exists", fg="yellow")
            return False

        if not is_sqlite_file(TODO_DB):
            click.secho(f"{todo_name} is not a todo list", fg="yellow")
            return False
        
        conn =  db_connection(f"{TODO_DB}")

        if not conn:
            return False
        
        cursor = conn.cursor()

        if not todo_id:
            click.secho(f"enter valid id from {todo_name}",fg="yellow")
            return False
        
        try:
            todo_id = int(todo_id)
        except (TypeError,ValueError):
            click.secho("Task id must be an integer.", fg="red")
            return False
        
        update_time = datetime.now()
        update_time = update_time.strftime("%Y-%m-%d %H:%M:%S")
        update_query = '''
            UPDATE tasks SET status=(?),description=(?),update_at=(?) WHERE id=(?)
        '''
        cursor.execute(update_query,(todo_status,todo_desc,update_time,todo_id,))
        conn.commit()
        click.secho(f"task {todo_id} updated successfully at {update_time}" , fg = "green")
        logging.info(f"task {todo_id} updated successfully")


    

if __name__ == "__main__":

    todo_update()