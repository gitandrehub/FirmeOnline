# moduli che mi servono
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

#altri file.py
from models import User
import utenti_dao, posts_dao, don_dao

#per le immagini
from PIL import Image

PROFILE_IMG_HEIGHT = 130
POST_IMG_WIDTH = 300

app = Flask(__name__)
app.config['SECRET_KEY'] = '2651'

login_manager = LoginManager()
login_manager.init_app(app)

# homepage
@app.route('/')
def home():
    posts_db = posts_dao.get_posts(0)
    
    faggiornatimer(posts_db)

    return render_template('home.html', posts=posts_db)

# funzione che aggiorna il timer di ogni raccolta
def faggiornatimer(posts_db):
    for post in posts_db:
        timeout = tempo_restante(post['datafine'])
        posts_dao.aggiornatimer(timeout, post['raccid'])

# funzione che calcola il tempo restante prima che una raccolta chiuda
def tempo_restante(datainput):
    print(datainput)
    datainput = datetime.strptime(datainput, '%Y-%m-%dT%H:%M')
    data_attuale = datetime.now()
    diff = datainput-data_attuale

    giorni = diff.days
    ore, resto = divmod(diff.seconds, 3600)
    minuti, _ = divmod(resto, 60)

    if(giorni > 14):
        return "-1"
    elif (giorni < 0):
        return "0"
    else:
        str = f"{giorni}:{ore}:{minuti}"
    return str

# funzione per pagina che mi fa vedere le raccolte finite
@app.route('/finite')
def finite():
    posts_db = posts_dao.get_posts(1)

    return render_template('finite.html', posts=posts_db)

# funzione di login
@app.route('/login', methods=['POST'])
def login():
    utente_form = request.form.to_dict()
    utente_db = utenti_dao.get_user_by_email(utente_form['email'])

    if not utente_db or not check_password_hash(utente_db['password'], utente_form['password']):
        flash('Credenziali non valide, riprova', 'danger')
        return redirect(url_for('home'))
    else:
        new = User(id=utente_db['id'], email=utente_db['email'], password=utente_db['password'], immagine_profilo=utente_db['immagine_profilo'],nome=utente_db['nome'], cognome=utente_db['cognome'])
        login_user(new, True)
        flash('Bentornato ' + utente_db['email'] + '!', 'success')

    return redirect(url_for('home'))

# funzione di registrazione nuovo utente; nel caso in cui l'utente 
# non inserisca un'immagine allora gliene verrà assegnata una di default (default.png)
@app.route('/registrazione')
def registrazione():
    return render_template('registrazione.html')

@app.route('/registrazione', methods=['POST'])
def registrazione_post():
    new_user = request.form.to_dict()
    user_db = utenti_dao.get_user_by_email(new_user['email'])

    if user_db:
        flash('E\' già presente un utente con questa mail', 'danger')
        return redirect(url_for('registrazione'))
    else:
        img_profilo = ''
        user_image = request.files['immagine_profilo']
        if user_image:
            img = Image.open(user_image)
            width, height = img.size
            
            # ridimensiono l'immagine
            new_width = PROFILE_IMG_HEIGHT * width/height
            size = new_width, PROFILE_IMG_HEIGHT
            img.thumbnail(size, Image.Resampling.LANCZOS)

            left = (new_width/2 - PROFILE_IMG_HEIGHT/2)
            top = 0
            right = (new_width/2 + PROFILE_IMG_HEIGHT/2)
            bottom = PROFILE_IMG_HEIGHT

            img = img.crop((left, top, right, bottom))
            ext = user_image.filename.split('.')[-1]
        else:
            img = Image.open('static/default.png')
            width, height = img.size
        
            # ridimensiono l'immagine
            new_width = PROFILE_IMG_HEIGHT * width/height
            size = new_width, PROFILE_IMG_HEIGHT
            img.thumbnail(size, Image.Resampling.LANCZOS)

            left = (new_width/2 - PROFILE_IMG_HEIGHT/2)
            top = 0
            right = (new_width/2 + PROFILE_IMG_HEIGHT/2)
            bottom = PROFILE_IMG_HEIGHT

            img = img.crop((left, top, right, bottom))
            ext = 'png'

        img.save('static/' + new_user.get('email').lower() + '.' + ext)

        img_profilo = new_user.get('email').lower() + '.' + ext

        new_user['password'] = generate_password_hash(new_user.get('password'))
        new_user['immagine_profilo'] = img_profilo

        success = utenti_dao.add_user(new_user)

        if success:
            flash('Utente creato correttamente; effettua il login !', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione dell\'utente: riprova!', 'danger')
            return redirect(url_for('registrazione'))

# load user
@login_manager.user_loader
def load_user(user_id):
    db_user = utenti_dao.get_user_by_id(user_id)
    if db_user is not None:
        user = User(id=db_user['id'], email=db_user['email'],password=db_user['password'], immagine_profilo=db_user['immagine_profilo'], nome=db_user['nome'], cognome=db_user['cognome'])
    else:
        user = None

    return user

# logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# funzione per pagina profilo utente
@app.route("/profile")
@login_required
def profile():
    post_id = posts_dao.get_posts_user(current_user.id)
    balance=0
    totpost=0

    for post in post_id:
        totpost+=1
        for key in dict(post).keys():
            if key == "timer" and (not post[key] != "0"):
                balance+=post['soldrac']
    faggiornatimer(post_id)
    
    return render_template('profile.html', posts=post_id, balance=balance, totpost=totpost)

# funzione per creare una nuova petizione
@app.route("/newpetizione")
@login_required
def newpetizione():
    return render_template('newpetizione.html')

@app.route("/newpetizione", methods=['POST'])
@login_required
def newpetizione_post():
    post = request.form.to_dict()
    post_image = request.files['immagine_post']

    if post['minel'] > post['goal'] or post['maxel'] < post['minel']:
        flash('Deve essere rispettato il pattern: minima donazione < goal e massima donazione > minima donazione', 'danger')
        return redirect(url_for('home')) 
    
    if post['tipo_raccolta'] == "normale" and post['datetime'] != '':
        timeout = tempo_restante(post['datetime'])
        if (timeout == "-1"):
            flash('La raccolta non può durare più di 14 giorni dalla creazione', 'danger')
            return redirect(url_for('home'))
    elif post['tipo_raccolta'] == "lampo":
        if(datetime.now().minute+5 > 60):
            minutes = datetime.now().minute+6-60
            hour = datetime.now().hour+1
        else:
            minutes = datetime.now().minute+6
            hour = datetime.now().hour
        if(datetime.now().month < 10): month = f"0{datetime.now().month}" 
        else: month = f"{datetime.now().month}" 
        if(datetime.now().day < 10): day = f"0{datetime.now().day}" 
        else: day = f"{datetime.now().day}"
        post['datetime'] = f"{datetime.now().year}-{month}-{day}T{hour}:{minutes}"
        timeout = tempo_restante(post['datetime'])
    else:
        flash('Inserire data e ora di fine', 'danger')
        return redirect(url_for('newpetizione'))

    if post_image:
        img = Image.open(post_image)
        width, height = img.size
        
        new_height = height/width * POST_IMG_WIDTH
        size = POST_IMG_WIDTH, new_height
        img.thumbnail(size, Image.Resampling.LANCZOS)

        ext = post_image.filename.split('.')[-1]
        secondi = int(datetime.now().timestamp())

        img.save('static/@' + current_user.email.lower() + '-' + str(secondi) + '.' + ext)

        post['immagine_post'] = '@' + current_user.email.lower() + '-' + str(secondi) + '.' + ext
    
    post['id_utente'] = int(current_user.id)
    success = posts_dao.add_post(post, timeout, current_user.id, datetime.now())

    if success: flash('Post creato correttamente', 'success')
    else: flash('Non siamo riusciti a creare il post ! riprova', 'danger')
    
    return redirect(url_for('home'))

# funzione per aggiungere una donazione
@app.route("/donazione/<int:id>", methods=['POST'])
def donazione(id):
    don = request.form.to_dict()
    racc = posts_dao.get_post(id)
    timerest = tempo_restante(racc['datafine'])

    print(don)

    if (timerest == "0" or don['numcarta'] == '' or don['cvv'] == ''):
        flash('La raccolta è stata chiusa durante la donazione', 'danger')
        return redirect(url_for('home'))
    else:
        try:
            if don['anonimo'] == '' :
                success = don_dao.newdonazione(don, racc)
        except:
            if don['nome'] != '' and don['cognome'] != '':
                success = don_dao.newdonazione(don, racc)
            else: success = False
        if success: flash('Donazione inserita correttamente', 'success')
        else: flash('Non siamo riusciti ad accettare la donazione! riprova', 'danger')

    return redirect(url_for('single_post', id=id))

# funzione per la pagina dedicata alla singola raccolta
@app.route('/posts/<int:id>')
def single_post(id):
    post_db = posts_dao.get_post(id)
    don_db = don_dao.get_don(id)

    return render_template('single_post.html', post=post_db, dons=don_db)

# funzioni che mi fanno modificare specifiche della raccolta 
@app.route('/modifica/<int:id>')
@login_required
def modifica(id):
    post_db = posts_dao.get_post(id)
    return render_template('modifica.html', post=post_db)

@app.route('/modifica/<int:id>', methods=['POST'])
@login_required
def modifica_post(id):
    post = request.form.to_dict()
    post_image = request.files['immagine_post']
    racc = posts_dao.get_post(id)
    print(post)

    if (racc['datafine'] != post['datafine']):
        timerest = tempo_restante(post['datafine'])
    else:
        timerest = tempo_restante(racc['datafine'])

    if (timerest == "-1"):
        flash('La raccolta non può durare più di 14 giorni dalla creazione', 'danger')
    else:
        post_db = posts_dao.get_post(id)
        if post_image:
            img = Image.open(post_image)
            width, height = img.size
            
            new_height = height/width * POST_IMG_WIDTH
            size = POST_IMG_WIDTH, new_height
            img.thumbnail(size, Image.Resampling.LANCZOS)

            ext = post_image.filename.split('.')[-1]
            secondi = int(datetime.now().timestamp())

            img.save('static/@' + current_user.email.lower() + '-' + str(secondi) + '.' + ext)

            post['immagine_post'] = '@' + current_user.email.lower() + '-' + str(secondi) + '.' + ext
            posts_dao.aggiornaimmagine(post['immagine_post'], id)
        else:
            try:
                if(post['cancim'] == ''):
                    posts_dao.aggiornaimmagine('', id)
            except:
                print('no')
    
        for keyp in post.keys():
            for keydb in post_db.keys():
                if post[keyp] != dict(post_db)[keydb] and keyp == keydb:    
                    if keydb == "tiporac" and post_db[keydb] == "normale" and post[keyp] == "lampo":
                        print('normale to lampo')
                        flash('non è possibile cambiare il tipo di raccolta da normale a lampo ! <br>per terminare la raccolta tra 5 minuti cambiare la data di fine con quella di oggi e come orario l\'attuale + 5 minuti', 'danger')
                    posts_dao.aggiorna(keydb, post[keyp], id)
        
    return redirect(url_for('profile'))

# funzione per cancellare una raccolta
@app.route('/cancella/<int:id>')
@login_required
def cancella(id):
    success = posts_dao.cancella(id)
    if success: flash('Raccolta cancellata correttamente', 'success')
    else: flash('Errore durante la chiusura della raccolta! riprova', 'danger')

    return redirect(url_for('profile'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)