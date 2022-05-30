from typing import Optional, Union
import sqlite3

from fastapi import FastAPI
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    description: Optional[str] = None


# create function for run SQL
def run_sql(
        sql_statement: str,
        value: Optional[tuple] = (),
        is_select: Optional[bool] = False
) -> Union[None, list]:

    # connect sqlite
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute(sql_statement, value)

    # check select
    if is_select is True:
        list_of_books = cur.fetchall()
        conn.commit()
        conn.close()
        return list_of_books
    else:
        conn.commit()
        conn.close()


# Create database
run_sql(
    sql_statement="""
    CREATE TABLE IF NOT EXISTS books
        (id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT)
    """
)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# get books
@app.get("/books")
async def select_query():
    # Query
    result = run_sql(
        sql_statement="SELECT * FROM books",
        is_select=True
    )
    return {"result": result}


# add new book
@app.post("/books")
async def insert_book(book: Book):
    # Insert
    run_sql(
        sql_statement="INSERT INTO books (title, description) VALUES (?, ?)",
        value=(book.title, book.description)
    )
    return {
        "name": book.title,
        "desc": book.description,
    }


# edit book name form id
@app.patch("/books/{id}")
async def update_book(id: int, book: Book):
    # update
    run_sql(
        sql_statement="UPDATE books SET title = ? WHERE id = ?",
        value=(book.title, id)
    )
    return {
        "msg": f"edit book id:{id} completed"
    }


# delete book from id
@app.delete("/books/{id}")
async def delete_book(id: int):
    run_sql(
        sql_statement="DELETE FROM books WHERE id = ?",
        value=(id,)
    )
    return {
        "msg": f'delete book id:{id} completed',
    }


"""
Run FastAPI by use this command

>> python -m uvicorn main:app --reload <<

main is name of file.py
app is name of FastAPI() <- line 47
"""
