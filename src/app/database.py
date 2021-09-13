from app import db
from datetime import datetime as dt

def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table
    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from tasks;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2],
            "added_at": result[3],
            "difficulty": result[4],
            "deadline": result[5],
            "importance": result[6]
        }
        todo_list.append(item)

    return todo_list


def update_task(field, task_id: int, text) -> None:
    conn = db.connect()
    content = f"'{text}'" if isinstance(text, str) else int(text)

    query = f"Update tasks set {field} = {content} where id = {task_id};"
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update tasks set status = \'{}\' where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str, difficulty, deadline, importance) ->  int:
    date = dt.today().strftime('%Y-%m-%d')
    conn = db.connect()
    query = 'Insert Into tasks (task, status, difficulty, deadline, importance, added_at) VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(
        text, "Todo", difficulty, importance, deadline, date)
    conn.execute(query)
    query_results = conn.execute("SELECT currval(pg_get_serial_sequence('tasks','id'));")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From tasks where id={};'.format(task_id)
    conn.execute(query)
    conn.close()