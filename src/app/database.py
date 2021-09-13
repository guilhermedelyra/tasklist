from app import db
from datetime import datetime as dt
import sqlalchemy

def create_tables():
    conn = db.connect()
    init_sql = open('init.sql')
    escaped_sql = sqlalchemy.text(init_sql.read())
    conn.execute(escaped_sql)
    conn.close()


def fetch_todo(user_id) -> dict:
    conn = db.connect()
    query_results = conn.execute(f"Select * from tasks WHERE user_id = '{user_id}' ORDER BY priority DESC;").fetchall()
    conn.close()

    todo_list = []
    
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2],
            "priority": result[3],
            "added_at": result[4],
            "difficulty": result[5],
            "deadline": result[6],
            "importance": result[7]
        }
        todo_list.append(item)

    return todo_list


def update_task(field, task_id: int, text) -> None:
    conn = db.connect()
    content = f"'{text}'" if isinstance(text, str) else int(text)

    query = f"Update tasks set {field} = {content} where id = {task_id};"
    conn.execute(query)
    conn.close()


def insert_new_task(user_id, text: str, difficulty, deadline, importance) ->  int:
    date = dt.today().strftime('%Y-%m-%d')
    priority = round((int(difficulty) + (10-int(importance)) + int(deadline)) / 3, 2) * 10

    conn = db.connect()
    query = "Insert Into tasks (task, priority, status, difficulty, deadline, importance, added_at, user_id)" + \
                    f"VALUES ('{text}', '{priority}', 'Todo', '{difficulty}', '{deadline}', '{importance}', '{date}', '{user_id}');"
    conn.execute(query)
    query_results = conn.execute("SELECT currval(pg_get_serial_sequence('tasks','id'));")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    conn = db.connect()
    query = 'Delete From tasks where id={};'.format(task_id)
    conn.execute(query)
    conn.close()