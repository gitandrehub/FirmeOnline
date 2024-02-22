import sqlite3

# prendo l'utente data la mail
def get_user_by_email(email):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE email = ?'
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

# prendo l'utente dato l'id
def get_user_by_id(id):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE id = ?'
    cursor.execute(sql, (id ,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

# aggiungo un utente al db
def add_user(user):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO utenti(email, password, immagine_profilo, nome, cognome) VALUES(?,?,?,?,?)'
    print(user)
    
    try:
        cursor.execute(sql, (user['email'], user['password'], user['immagine_profilo'], user['nome'], user['cognome']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    
    cursor.close()
    conn.close()

    return success

