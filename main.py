import mysql.connector
from cryptography.fernet import Fernet
import functions
#Menu
print("\t\t\t Bienvenue Keypass Manager\n")
checker = True
while checker :
        
    print("\t\t\t\tMenu\n")
    print(" 1. Ajouter un identifiant\n 2. Supprimer un identifiant\n 3. Modifier le mot de passe d'un identifiant\n 4.Afficher tous les identifiants\n 5. Rechercher un identifiant\n 6. Quiter")
    try:
        choice = int(input("Entrer votre choix : "))
        conn = functions.initialisation()

    except ValueError as error:
        print("\t\t\t\tVous devrer entrer un entier !\n ", error)
    #except ConnectionError as err:
    #    print("\t\t\t\tErreur de connexion à la base de données", err)

    match choice:
        case 1:
            site = input("Site : ")
            id = input("Identifiant : ")
            password = input("Mot de passe : ")
            functions.ajouter(site, id, password, conn)
        case 2:
            site = input("Entrer le site de l'identifiant : ")
            functions.supprimer(site, conn)
        case 3:
            site = input("Entrer le site : ")
            new = input("Nouveau Mot de passe : ")
            functions.modifier(site, new, conn)
        case 4:
            functions.afficher(conn)
        case 5:
            site = input("Enter le site : ")
            row = functions.rechercher(site, conn)
            cipher = Fernet(row[3])
            decrypted_data = cipher.decrypt(row[2])
            print("Site        Identifiant          Mot de passe\n")
            print("{}       {}      {}".format(row[0], row[1], decrypted_data.decode()))
        case 6:
            checker = False
        
conn.close()