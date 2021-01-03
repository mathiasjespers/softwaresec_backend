from flask import Flask, request, jsonify, json
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, supports_credentials=True, origins="*")


def insertIntoTable(uid, name, highscore, isPublic):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO ClickingGame_users
                          (id, name, highscore, isPublic) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (uid, name, highscore, isPublic)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into ClickingGame_users table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def getScore(uid):
    highscore = -1
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query = """select * from ClickingGame_users where uid = ?"""
        cursor.execute(sql_select_query, (uid,))
        records = cursor.fetchall()
        for row in records:
            print("Name = ", row[1])
            print("highscore  = ", row[2])
            highscore = row[2]
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return highscore


def updateScore(uid, score):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_update_query = """Update ClickingGame_users set highscore = ? where id = ?"""
        data = (score, uid)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The sqlite connection is closed")


# flask get highscore route
@app.route('/highscore', methods=['GET'])
def get():
    uid = request.json['uid']
    score = getScore(uid)
    return jsonify({'highscore': int(score)})


# flask post new score route
@app.route('/score', methods=['POST'])
def post():
    score = request.json['score']
    user = request.json['user']
    uid = request.json['uid']

    isInDatabase = int(getScore(uid))

    if isInDatabase == -1:
        insertIntoTable(uid, user, score, 0)
    if isInDatabase < score:
        updateScore(uid, score)


if __name__ == '__main__':
    context = ('local.crt', 'local.key')  # certificate and key files
    app.run(debug=True, ssl_context=context)
