### IMPORT MODULI ESTERNI

#import dei moduli esterni

#import della funzione brute_force e is_valid_ip definita nel modulo chipherlib
from cipherlib import is_valid_ip, get_status_http_method


### DICHIARAZIONE VARIABILI E CHECK INPUT UTENTE    

#dichiarazione variabili per input utente
ip_target = ""
port_target = 0
path_target = ""

#Input IP target con validazione
while True:
    #input dall'utente per la stringa ip_target
    ip_target = str(input("Inserisci l'indirizzo IP del target:\n"))
    #esce dall'iterazione solo se l'ip è valido (call function is_valid_ip definita in precedenza)
    if (is_valid_ip(ip_target)):
        break

#Input Porta target con validazione
while True:
    #medesimo principio dell'input relativo all'ip target
    try:
        port_target = int(input("Inserisci la porta web target (80/443):\n"))
    except ValueError:
        print("Inserisci una porta web valida (80/443)! \n")
    #esce dall'iterazione solo se viene inserito un intero che rientri nel range UDP
    if(port_target == 80 or port_target == 443):
        break

#Input Path target con validazione
while True:
    #medesimo principio dell'input relativo alla port target
    try:
        path_target = str(input("Inserisci il path per comporre la Request-URI:\n"))
    except ValueError:
        print("Inserisci un path ! \n")
    #esce dall'iterazione solo se viene inserito un path vuoto
    if(path_target != ""):
        break


### CORPO PRINCIPALE DEL CODICE

#per get, post ed head valgono gli stessi status code
#chiamo la funzione get_status_http_method (o con GET o con POST o con HEAD) e salvo lo status code
status_code_get_post = get_status_http_method(ip_target, port_target, path_target, "GET")
#inizializzo la variabile booleana per il check della validità della risorsa a True
res_is_valid = True

#itero per gli status code della classe 400
for status_err in range(400,418):
    #se lo status della chiamata a funzione fa match con almeno uno setto a False
    #quindi risorsa non valida
    if(status_code_get_post == status_err):
        res_is_valid = False

#itero per gli status code della classe 500
for status_err in range(500,506):
    #se lo status della chiamata a funzione fa match con almeno uno setto a False
    #quindi risorsa non valida
    if(status_code_get_post == status_err):
        res_is_valid = False

#se la risorsa risulta valida continuo con le verifiche dei metodi abilitati
if(res_is_valid == True):
    #salvo il valore del tag 'Allow' chiamando get_status_http_method con method OPTIONS
    method_allowed = get_status_http_method(ip_target, port_target, path_target, "OPTIONS")
    if(method_allowed != None):
        #se non restituisce None stampo direttamente i metodi abilitati
        print("I metodi abilitati sono: ", method_allowed)
    else:
        #se è None, OPTIONS non è abilitato e verifico i metodi uno a uno
        #PUT, TRACE, DELETE
        #print("Verificare gli altri metodi!")
        #poichè nel check precedente tra le righe 94-106 ho già verificato di non aver ricevuto codici di errore dei metodi
        #GET, POST, HEAD (se disabilitati il server web non servirebbe per esporre le risorse)
        #li considero abilitati e inizio a popolare la stringa method_allowed per la stampa
        method_allowed = "GET, POST, HEAD"
        #salvo gli status code dei metodi restanti con la chiamata a funzione get_status_http_method
        put = get_status_http_method(ip_target, port_target, path_target, "PUT")
        delete = get_status_http_method(ip_target, port_target, path_target, "DELETE")
        trace = get_status_http_method(ip_target, port_target, path_target, "TRACE")
        #se per ogni method lo status code risultante è quello atteso, sono abilitati e li aggiungo in coda alla stringa
        if(put == 200 or put == 201 or put == 204):
            method_allowed = method_allowed + ", PUT"
        if(delete == 200 or delete == 202 or delete == 204):
            method_allowed = method_allowed + ", DELETE"
        if(trace == 200 ):
            method_allowed = method_allowed + ", TRACE"
        #stampo la stringa con i metodi abilitati costruita tramite controlli
        print("Metodi abilitati: ", method_allowed, "\n")
#se è stata inserita una risorsa non valida (non esiste o non è raggiungibile) stampo un messaggio di errore
else:
    print("La risorsa richiesta non esiste o non è raggiungibile!\n")
