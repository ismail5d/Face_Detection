import sqlite3, os

def fetch_images(db):
    con=sqlite3.connect(db)
    query="select * from elements;"
    cur = con.cursor()
    cur.execute(query)
    data = cur.fetchall()
    con.close()
    return data

def get_image_by_name(name,db):
    con=sqlite3.connect(db)
    query="select IMAGE,TYPE from elements where NOM=?;"
    cur = con.cursor()
    
    cur.execute(query,[name])
    data = cur.fetchall()

    if len(data) == 0:
        return 0
    con.close()
    return (data[0][0],data[0][1])
