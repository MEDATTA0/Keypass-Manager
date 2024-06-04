from cryptography.fernet import Fernet
import random
import curses.ascii

def table_searcher(ident_or_site):
    #Elle recherche la table et le field correspondants
    #Un identifiant finit pas @..... donc on va chercher dans ident_or_site s'il y a un indice que c'est un compte
    accounts = ['@gmail.com', '@icloud.com', '@outlook.com']
    for account in accounts:
        if account in ident_or_site:
            return ['keypassManager', 'identifiant']
        
    return ['associated_site', 'site']


def initialisation():
    #Tentative de connexion à la base de données
    connexion = mysql.connector.connect(
        host = 'localhost',
        user = 'user1',
        password = '123456789',
        database = 'project'
    )

    #Création d'un curseur pour envoyer des requêtes
    cursor = connexion.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS keypassManager(
        compte VARCHAR(50) NOT null,
        identifiant VARCHAR(50) NOT null,
        password VARCHAR(300) NOT null,
        cipher VARCHAR(200))'''
    )
    #identifiant_id INT AUTO_INCREMENT,
    #PRIMARY KEY(identifiant_id)
    #Confirmation de la modification de la table avec commit()
    connexion.commit()
    
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS associated_site(
        identifiant VARCHAR(50),
        site VARCHAR(50)
        )'''
        #FOREIGN KEY(identifiant_id) REFERENCES keypassManager(identifiant_id)
    )
    #On retourne la connexion si c'est successful
    return connexion

def ajouter(compte, identifiant, data, connexion):
    '''Elle reçoit en paramètre une connexion à la base de donnée,
    un identifiant et un password qu'elle crypte et l'insère dans la base de donnée.
    Elle insère aussi la clé de chiffrement sous forme de valeur hexadécimale
    '''
    #On génère une clé
    key = Fernet.generate_key()
    #On crée un chiffeur
    cipher = Fernet(key)
    #On encode le mot de passe pour le switch de string->bytes
    data = data.encode()
    #On chiffre le mot de passe
    encrypted_data = cipher.encrypt(data)
    #On crée un curseur à la base de données
    cursor = connexion.cursor()
    #On envoie une requête à la base de données
    cursor.execute(
        '''INSERT INTO keypassManager (type, identifiant, password, cipher)
        VALUES ('{}', '{}', '{}', '{}')'''.format(compte, identifiant, encrypted_data.decode(), key.decode())
    )
    #On confirme la modification de la table keypassManager
    connexion.commit()
    print("\t\t\tENREGISTREMENT REUSSI\n")


def afficher(connexion):
    
    cursor = connexion.cursor()
    cursor.execute(
        '''SELECT * FROM keypassManager'''
    )
    #On récupère les réponses de la requête dans rows
    rows = cursor.fetchall()

    '''Chaque identifiant a son champ où est stocké la clé de chiffrement,
    elle sera récupérée à chaque fois que l'on voudrait déchiffrer et afficher un mot de passe'''    
    
    print("Site     Identifiant          Mot de passe\n")
    i = 0
    for row in rows:
        #On récupère la clé dans row[3] et on crée un chiffreur
        cipher = Fernet(row[3])
        #On dechiffre le mot de passe avec le cipher créé
        decrypted_data = cipher.decrypt(row[2])
        #le mot de passe déchiffré est en bytes, on utilise decode() pour le switch de bytes->string
        print("{}       {}        {}".format(row[0], row[1], decrypted_data.decode()))
        i += 1
    print("\t\t{} IDENTIFIANT(S) TROUVES !\n".format(i))


def supprimer(connexion, ident_or_site):
    '''Elle supprime en fonction de la table soit un site soit un identifiant'''
    cursor = connexion.cursor()
    table, field = table_searcher(ident_or_site)
    cursor.execute(
    '''DELETE FROM '{}' WHERE '{}' LIKE '%{}%' '''.format(table, field, ident_or_site)
    )
    
    connexion.commit()
    print("\t\t\tSUPPRESSION REUSSIE !\n")
        

def rechercher(connexion, ident_or_site):
    '''cette fonciton recherche un site ou un identifiant en fonction de la table choisie'''
    cursor = connexion.cursor()
    table, field = table_searcher(ident_or_site)
    cursor.execute(
       '''SELECT * FROM {} WHERE {} LIKE '%{}%' '''.format(table, field, ident_or_site)
    )
    row = cursor.fetchone()
    
    return row


def modifier(connexion, identifiant, new_password):
    #On génère une clé
    key = Fernet.generate_key()
    #On crée un cipher avec la clé
    cipher = Fernet(key)
    #On chiffre le mot de passe, encode permet de switch de string->bytes
    encrypted_password = cipher.encrypt(new_password.encode())
    #On crée un curseur pour envoyer des requêtes à la base de données
    cursor = connexion.cursor()
    #decode permet de switch de bytes->string, afin d'insérer les données sous forme de string et non sous forme de bytes
    cursor.execute(
        ''' UPDATE keypassManager SET password = '{}', cipher = '{}' WHERE identifiant = '{}' '''.format(encrypted_password.decode(), key.decode(), identifiant)
    )
    connexion.commit()
    print("\n\t\t\t MOT DE PASSE MODIFIE AVEC SUCCES !\n")


def ajouter_site_associe(connexion, identifiant):
    
    #On crée un curseur pour envoyer des requêtes à la base de données
    cursor = connexion.cursor()
    row = rechercher(connexion, identifiant)
    if row:
        site = input("Entrer le site associe : ")
        cursor.execute(
            '''INSERT INTO associated_site(identifiant, site)
            VALUES ('{}', '{}')'''
            .format(identifiant, site)
            #identifiant_id (a remettre plus tard, cle etrangere)
        )
        #On confirme la modification avec commit()
        connexion.commit()
        print("\t\t\tSITE ASSOCIE A {} !\n", identifiant)
    else:
        print("\t\t\tAUNCUN IDENTIFIANT TROUVE !\n")


def supprimer_site_associe(connexion, site=''):
    #connexion = mysql.connector.connect()
    cursor = connexion.cursor()
    cursor.execute(
        '''DELETE FROM associated_site WHERE site = '{}' '''.format(site)
    )
    #On confirme la modification adressée à la base de données grâce à commit
    connexion.commit()
    print("\t\t\tSITE SUPPRIME !")


def afficher_site_associe(connexion):
    #connexion = mysql.connector.connect()
    cursor = connexion.cursor()
    cursor.execute(
        '''SELECT * FROM associated_site'''
    )
    #On récupère toutes la reponse de requête dans la variable rows 
    rows = cursor.fetchall()
    i = 0
    #On affiche le resultat et on sauvegarde le nombre d'itération dans i
    print("IDENTIFIANT                    SITE")
    for row in rows:
        print("{}      {}".format(row[0], row[1]))
        i += 1

    print("\t\t\t{} SITE(S) TROUVE(S) !\n".format(i))

def password_gen():
    nb_caracteres = int(input("Entrer le nombre de caracteres : "))
    satisfait = False
    checker = True
    #Generer des mots de passe en boucle
    while checker :
        password =""
        i = 0
        #Generer un mot de passe avec des alphanumeriques jusqu'au nombre de caracteres desire
        while i <= nb_caracteres:
            letter = chr(random.randint(0, 255))
            if curses.ascii.isalnum(letter):
                i += 1
                password = password+letter
        #password = ord(random.randbytes(nb_caracteres))
        print(password)
        checker = bool(int(input("\n\t\tReessayer un autre ? (0/1) : ")))
    
    #On l'enregistre si l'utilisateur est satisfait
    satisfait = bool(int(input("\t\t\tVoulez-vous l'enregistrer ? (0/1) : ")))
    if satisfait and not checker:
        return password
    else:
        return ""