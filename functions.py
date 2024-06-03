import mysql.connector
from cryptography.fernet import Fernet


def initialisation():
    connexion = mysql.connector.connect(
        host = 'localhost',
        user = 'user1',
        password = '123456789',
        database = 'project'
    )

    cursor = connexion.cursor()

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS keypassManager(
        site VARCHAR(50) NOT null,
        identifiant VARCHAR(50) NOT null,
        password VARCHAR(300) NOT null,
        cipher VARCHAR(200))'''
    )
    connexion.commit()
    return connexion

def ajouter(site, identifiant, data, connexion):
    '''Elle reçoit en paramètre une connexion à la base de donnée,
    un identifiant et un password qu'elle crypte et l'insère dans la base de donnée.
    Elle insère aussi la clé de chiffrement sous forme de valeur hexadécimale
    '''
    cursor = connexion.cursor()

    key = Fernet.generate_key()
    cipher = Fernet(key)
    data = data.encode()
    encrypted_data = cipher.encrypt(data)
    cursor.execute(
        '''INSERT INTO keypassManager (site, identifiant, password, cipher)
        VALUES ('{}', '{}', '{}', '{}')'''.format(site, identifiant, encrypted_data.decode(), key.decode())
    )
    connexion.commit()
    print("\t\t\tENREGISTREMENT REUSSI\n")


def afficher(connexion):
    
    cursor = connexion.cursor()
    cursor.execute(
        '''SELECT * FROM keypassManager'''
    )
    rows = cursor.fetchall()

    '''Chaque identifiant a son champ où est stocké la clé de chiffrement,
    elle sera récupérée à chaque fois que l'on voudrait déchiffrer et afficher un mot de passe'''    
    
    print("Site     Identifiant          Mot de passe\n")
    i = 0
    for row in rows:
        cipher = Fernet(row[3])
        decrypted_data = cipher.decrypt(row[2])
        print("{}       {}        {}".format(row[0], row[1], decrypted_data.decode()))
        i += 1
    print("\t\t{} IDENTIFIANT(S) TROUVES !\n".format(i))

def supprimer(site, connexion):
    cursor = connexion.cursor()
    cursor.execute(
        '''DELETE FROM keypassManager WHERE site = '{}' '''.format(site)
    )
    connexion.commit()
    print("\t\t\tSUPPRESSION REUSSIE !\n")


def rechercher(site, connexion):
    cursor = connexion.cursor()
    cursor.execute(
        "SELECT * FROM keypassManager WHERE site = '{}'".format(site)
    )
    row = cursor.fetchone()
    return row


def modifier(site, new_password, connexion):
    cursor = connexion.cursor()
    
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(new_password.encode())
    cursor.execute(
        ''' UPDATE keypassManager SET password = '{}', cipher = '{}' WHERE site = '{}' '''.format(encrypted_password.decode(), key.decode(), site)
    )
    connexion.commit()
    print("\n\t\t\t MOT DE PASSE MODIFIE AVEC SUCCES !\n")
