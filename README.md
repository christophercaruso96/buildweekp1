1) I file di minuta (e.g. minutes_day1_20240318.pdf) contengono un report dello stato avanzamento lavori (SAL)
2) Il file networkDiagram.drawio contiene lo schema di rete che verrà spiegato nella documentazione da fornire al cliente
3) Il file networkDiagram.png è l'immagine relativa allo schema di rete 
4) Il fle chipherlib.py è il modulo esterno creato ad hoc per contenere tutte le funzioni degli altri script (da mettere nello stesso path)
5) Lo script checkHttpMethod.py esegue l'enumerazione dei Metodi Http abilitati su un path specifico che costituisce la RequestUri (se OPTIONS è disabilitato fa comunque ulteriori verifiche sugli altri: GET, PUT, POST ...)
6) Lo script portScanning.py esegue un check delle porte UDP/TCP a seconda del range e dell'output richiesto
7) Lo script bruteForce.py esegue un bruteForce con funzione ricorsiva per colpire su più livelli (settati PHPSESSID e security)
8) Nell'area deriverables_cliente sono presenti i documenti da inviare al cliente (Documento Management con calcolo Effort in FTE, Relazione Tecnica, Proposta Commerciale)

