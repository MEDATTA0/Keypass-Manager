import mysql.connector
from cryptography.fernet import Fernet
import functions
import curses.ascii
import string
#Menu

conn = functions.initialisation()
print("\t\t\t Bienvenue Keypass Manager\n")
checker = True

while checker :
        
    print("\t\t\t\tMenu\n")
    print(''' 1. Ajouter un identifiant\n 2. Supprimer un identifiant\n 3. Modifier le mot de passe d'un identifiant 
 4.Afficher tous les identifiants\n 5. Rechercher un identifiant\n\n 6. Ajouter un site
 7.Supprimer un site\n 8. Afficher les sites\n 9. Rechercher un site\n\n 10. Quitter\n''')
    choice = input("Entrer votre choix : ")
    try:
        choice = int(choice)
    except ValueError as err:
        print("Veuillez entrer un nombre !")
        choice = '_'
    
    if choice not in range(1, 11):
        choice = '_'
    
    match choice:
        case 1:
            password = ""
            compte = input("Type de compte : ")
            identifiant = input("Identifiant : ")
            suggestion = int(input("Voulez-vous une suggestion de mot de passe ? (0/1)"))
            if suggestion:
                password = functions.password_gen()
            elif password == "":
                password = input("Entrer votre mot de passe : ")
            functions.ajouter(compte, identifiant, password, conn)
            break

        case 2:
            
            identifiant = input("Entrer l'identifiant : ")
            functions.supprimer(conn, identifiant)
            break

        case 3:
            identifiant = input("Entrer l'identifiant : ")
            new_password = input("Nouveau Mot de passe : ")
            functions.modifier(conn, identifiant, new_password)
            break

        case 4:
            functions.afficher(conn)
            break

        case 5:
            site_or_account = input("Enter le site/identifiant : ")
            row = functions.rechercher(conn, site_or_account)
            cipher = Fernet(row[3])
            decrypted_data = cipher.decrypt(row[2])
            print("Type        Identifiant          Mot de passe\n")
            print("{}       {}      {}".format(row[0], row[1], decrypted_data.decode()))
            break

        case 6:
            identifiant = input("Entrer un identifiant : ")
            functions.ajouter_site_associe(conn, identifiant)
            break

        case 7:
            site = input("Entrer le nom du site : ")
            functions.supprimer_site_associe(conn, site)
            break

        case 8:
            functions.afficher_site_associe(conn)
            break

        case 9:
            site = input("Entrer le nom du site : ")
            row = functions.rechercher(conn, site)
            print("Identifiant              Site\n")
            print("{}        {}".format(row[0], row[1]))
            break

        case 10:
            checker = False
            print("\t\t\tBye !!!")
            break

        case 11:
            nb = int(input("Entrer le nombre de caracteres : "))
            functions.password_gen(nb)
            break
        
        case '_':
            break
    
    print("\n")
'''Ajouter, supprimer, afficher les sites associe a un compte'''
        
conn.close()