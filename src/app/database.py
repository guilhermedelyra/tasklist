from app import db
import sqlalchemy

def create_tables():
    create_user = 'CREATE TABLE IF NOT EXISTS "users" ("id" INT PRIMARY KEY, "name" varchar NOT NULL, "email" varchar UNIQUE NOT NULL, "profile_pic" varchar NOT NULL)'
    create_tasks = 'CREATE TABLE IF NOT EXISTS "tasks" ("id" SERIAL PRIMARY KEY, "task" varchar NOT NULL, "status" varchar, "user_id" INT NOT NULL, CONSTRAINT "fk_user" FOREIGN KEY("user_id") REFERENCES "users"("id"))'

    conn = db.connect()
    conn.execute(create_user)
    conn.execute(create_tasks)
    conn.close()

def fetch_todo(user_id) -> dict:
    conn = db.connect()
    query_results = conn.execute(f"Select * from tasks WHERE user_id = {user_id};").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2]
        }
        todo_list.append(item)

    return todo_list


def update_task_entry(task_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update tasks set task = \'{}\' where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update tasks set status = \'{}\' where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str) ->  int:
    conn = db.connect()
    query = 'Insert Into tasks (task, status) VALUES (\'{}\', \'{}\');'.format(
        text, "Todo")
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