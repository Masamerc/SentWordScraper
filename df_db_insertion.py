import pandas as pd
import sqlite3
import numpy as np
import uuid
import random

# creating a toy data 
# uuid = universally unique identifier
uuid_list = [str(uuid.uuid4()) for _ in range(80)]
city_list = [random.choice(["NY", "LA", "SD", "CHI"]) for _ in range(80)]

df = pd.DataFrame(
    data={
        "id": uuid_list,
        "salary": np.random.randint(25, 130, 80),
        "age": np.random.randint(18, 56, 80),
        "location": city_list
    }
)

# init database
conn = sqlite3.connect("toy.db")
cur = conn.cursor()

# create table
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY NOT NULL,
        salary INTEGER,
        age INTEGER,
        user_location TEXT
    )
''')

# insert data from df to database

def insert_user(row):
    _id = row["id"]
    salary = row["salary"]
    age = row["age"]
    location = row["location"]

    cur.execute('INSERT INTO users VALUES(?, ?, ?, ?)', (_id, salary, age, location))

    print(f"Inserted following user with id: {_id}")

# df.apply(lambda x: insert_user(x), axis=1)

# conn.commit()

# readiung sql query
df2 = pd.read_sql("SELECT * FROM users WHERE salary > 100", conn)

conn.close()

# alternative: use itertuples() but not the slow alternative iterrows()
# for row in df.itertuples(index=False):
#     _id = row[0]
#     salary = row[1]
#     age = row[2]
#     location = row[3]

#     print(f"id: {_id} salar: {salary}")


