from tinydb import TinyDB, Query
db = TinyDB('../../data/db.json')


def format_row(row):
    return {
        'id': row['id'],
        'content': row['content'],
        'vector': row['vector']
    }
