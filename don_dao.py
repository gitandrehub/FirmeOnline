import sqlite3

# inserisce una nuova donazione nel database 'donazioni'
def newdonazione(don, racc):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if (int(don['soldi']) < racc['minen'] or int(don['soldi']) > racc['maxen']):
        return False

    success = False
    sql = 'INSERT INTO donazioni(nome, cognome, donazione, raccid, indirizzo) VALUES(?,?,?,?,?)'

    try:
        try:
            if don['anonimo'] == '':
                cursor.execute(sql, ('anonimo', 'anonimo', don['soldi'], racc['raccid'], don['indirizzo']))
        except:
            if (don['nome'] != '' and don['cognome'] != ''):
                cursor.execute(sql, (don['nome'], don['cognome'], don['soldi'], racc['raccid'], don['indirizzo']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        conn.rollback()
    
    if success:
        sql = 'SELECT soldrac FROM raccolte WHERE raccid = ?'
        try:
            cursor.execute(sql, (racc['raccid'], ))
            val = cursor.fetchone()[0]
            success = True
        except Exception as e:
            success = False
            print('ERROR', str(e))
            conn.rollback()
    
    if success:
        newval = val + int(don['soldi'])
        sql = 'UPDATE raccolte SET soldrac = ? WHERE raccid = ?'
        try:
            cursor.execute(sql, (newval, racc['raccid']))
            conn.commit()
            success = True
        except Exception as e:
            success = False
            print('ERROR', str(e))
            conn.rollback()

    cursor.close()
    conn.close()

    return success

# prende le donazioni relative ad una specifica raccolta
def get_don(id):
    conn = sqlite3.connect('db/racfirme.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM donazioni WHERE raccid = ?'
    cursor.execute(sql, (id,))
    dons = cursor.fetchall()

    cursor.close()
    conn.close()

    return dons