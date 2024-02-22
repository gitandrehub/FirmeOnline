from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password,
                 immagine_profilo, nome, cognome):
        self.id = id
        self.email = email
        self.password = password
        self.immagine_profilo = immagine_profilo
        self.nome = nome
        self.cognome = cognome