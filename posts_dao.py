import sqlite3
from datetime import datetime

# funzione che aggiorna il timer della raccolta
def aggiornatimer(timeout, raccid):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'UPDATE raccolte SET timer = ? WHERE raccid = ?'
    cursor.execute(sql, (timeout, raccid))
    conn.commit()

    cursor.close()
    conn.close()

# funzione che aggiorna specifiche della raccolta
def aggiorna(key, value, raccid):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("--- ", key, value)

    sql = f'UPDATE raccolte SET {key} = ? WHERE raccid = ?'
    cursor.execute(sql, (value, raccid))
    try:
        conn.commit()
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

# funzione che aggiorna l'immagine della raccolta
def aggiornaimmagine(image, id):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = f'UPDATE raccolte SET image = ? WHERE raccid = ?'
    cursor.execute(sql, (image, id))
    try:
        conn.commit()
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()

# funzione per aggiungere una petizione al db
def add_post(post, timeout, id, datacrz):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    print(id)
    print(timeout)
    print(post)

    success = False
    if 'immagine_post' in post:
        sql = 'INSERT INTO raccolte(timer, goal, titolo, descrizione, image, tiporac, minen, maxen, idutente, soldrac, datafine, datacrz) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'
        cursor.execute(sql, (timeout, post['goal'], post['titolo'], post['descrizione'], post['immagine_post'], post['tipo_raccolta'], post['minel'], post['maxel'], id, 0, post['datetime'], datacrz))
    else:
        sql = 'INSERT INTO raccolte(timer, goal, titolo, descrizione, tiporac, minen, maxen, idutente, soldrac, datafine, datacrz) VALUES(?,?,?,?,?,?,?,?,?,?,?)'
        cursor.execute(sql, (timeout, post['goal'], post['titolo'], post['descrizione'], post['tipo_raccolta'], post['minel'], post['maxel'], id, 0, post['datetime'], datacrz))
    
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success

# funzione da cui prendo tutte le raccolte del db
def get_posts(mod):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if mod == 1:
        sql = 'SELECT * FROM raccolte WHERE timer == "0" ORDER BY (goal-soldrac)'
    elif mod == 0:
        sql = 'SELECT * FROM raccolte WHERE timer != "0" ORDER BY datafine'
    cursor.execute(sql)
    posts = cursor.fetchall()

    cursor.close()
    conn.close()

    return posts

# fprendo tutte le raccolte create da uno specifico utente
def get_posts_user(id):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM raccolte WHERE idutente = ? ORDER BY datafine'
    cursor.execute(sql, (id,))
    posts = cursor.fetchall()
    print(posts)

    cursor.close()
    conn.close()

    return posts

# prende una specifica raccolta
def get_post(id):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM raccolte WHERE raccid = ?'
    cursor.execute(sql, (id,))
    post = cursor.fetchone()

    cursor.close()
    conn.close()

    return post

# cancello dal db una specifica raccolta
def cancella(raccid):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM raccolte WHERE raccid = ?'
    cursor.execute(sql, (raccid, ))
    
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success