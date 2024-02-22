# FirmeOnline

### Info Base
Il progetto è stato svolto per il corso 'Introduzzione alle applicazioni Web'.\
L’indirizzo a cui l’applicazione web è visibile e usabile è [andrea01.pythonanywhere.com](https://andrea01.pythonanywhere.com).\
Gli utenti registrati sono i seguenti:

```
mail utente            | password
-------------------------------------
marco.b@example.com    | MarcoB123
chiararossi@yahoo.com  | Chiara123
matteo.russo@gmail.com | pass89
```

Nel caso in cui, all'apertura dell'applicazione, non siano presenti raccolte è perchè sono state tutte chiuse (la data di chiusura è stata superata) e si possono visualizzare nella sezione 'Finite'. Per poterne creare serve:
- fare il login (con utenti indicati sopra) o una registrazione
- creare una nuova petizione con 'Lancia la tua petizione'

Per maggiori informazioni leggere i file 'info.txt' (su come funziona l'applicazione) e 'requirements.txt' (librerie che ho usato).

### Descrizione dell'applicazione web
Si vuole creare un'applicazione web per raccolte fondi tra privati. L’applicazione web deve supportare due tipi di utenti: quelli registrati e i visitatori del sito. \
Gli utenti registrati, previa registrazione e login sul sito, possono gestire delle raccolte fondi. Il form di login/registrazione richiede un campo il cui valore univoco verrà utilizzato per riconoscere l’utente nel sito (per esempio, la mail). Gli utenti possono, in particolare, creare, modificare e cancellare le proprie raccolte fondi. Alla creazione, una raccolta fondi sarà rappresentata dalle seguenti informazioni:
- Titolo della raccolta fondi
- Breve descrizione
- Immagine che rappresenta lo scopo o il tema della raccolta fondi
- Obiettivo monetario da raggiungere
- Tipo della raccolta:
  - lampo, cioè si possono ricevere donazioni solo entro 5 minuti dalla creazione della raccolta stessa
  - normale, cioè si possono ricevere donazioni nei 14 giorni seguenti la data di creazione (con data e ora di chiusura a        scelta dell’utente che crea la raccolta fondi)
- Entità minima e massima della singola donazione (per esempio, da 5 euro a 5000 euro)
Tutte le informazioni sono obbligatorie al momento della creazione della raccolta, tranne l’immagine. 

Gli utenti registrati possono modificare e cancellare le proprie raccolte fondi in ogni momento finché la raccolta è aperta, cioè finché si possono ricevere donazioni. Per ogni raccolta fondi si dovrà anche tener traccia di quanti soldi sono stati donati e questo valore non potrà essere cambiato dall’utente. Il totale donato andrà opportunamente visualizzato nella pagina della singola raccolta fondi.

Quando una raccolta fondi è chiusa (cioè se non si possono più ricevere donazioni), non potrà essere più modificata né eliminata. All’atto della chiusura, si possono verificare due situazioni:
- La raccolta ha raggiunto (o superato) l’obiettivo monetario. In questo caso, la pagina della raccolta fondi mostra la 
  scritta “Obiettivo raggiunto!” e i soldi raccolti vengono trasferiti nel portafoglio virtuale dell’utente, visibile dalla 
  sua pagina profilo.
- La raccolta non ha raggiunto l’obiettivo monetario. In questo caso, la pagina della raccolta fondi mostrerà la scritta 
  “Obiettivo non raggiunto!”.

I visitatori non hanno bisogno di registrarsi né fare il login sul sito e potranno navigare liberamente nell’applicazione web e fare donazioni.\
Nella home page, i visitatori troveranno la lista delle raccolte aperte, ordinate per data/ora di chiusura (a partire da quelle che chiuderanno prima). Deve essere chiaro al visitatore quali siano le raccolte lampo e quali quelle normali, con l’indicazione di quanto manca alla loro chiusura per entrambe.\
Le raccolte chiuse, invece, dovranno essere elencate in una pagina dedicata che mostrerà per prima le raccolte che hanno raggiunto l’obiettivo monetario.\
Quando un visitatore vorrà fare una donazione, dovrà farlo dalla pagina della singola raccolta fondi, scegliendo la cifra da donare, indicando il proprio nome, cognome, indirizzo, le informazioni sulla carta di credito e se si vuole che la sua donazione sia pubblica o che rimanga anonima. Si supponga che i pagamenti siano istantanei e sempre possibili. \
Dopo una donazione, i dettagli del donatore (cioè, nome del donatore e l’ammontare donato) devono essere visibili in un’apposita sezione della pagina della singola raccolta fondi; se il donatore ha scelto di rimanere anonimo, comparirà “Anonimo” invece del nome del donatore. I fondi donati andranno ad aumentare il totale raccolto per la raccolta fondi in questione. E’ possibile donare fondi finché la raccolta è aperta.\
Un utente registrato può fare qualunque cosa faccia un visitatore, incluso donare alla propria raccolta fondi.
