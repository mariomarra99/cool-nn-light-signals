#Traffic-light-detection-classification

Progetto sulla ricerca di metodi per una efficace **detection** e **classification** di semafori. 
Parte fondante e fondamentale sia per il progetto che per la presentazione si può trovare qui: 
https://colab.research.google.com/drive/16xmd3PJsmGA4x6rRYSjiZmGbOVb2SRzn?authuser=3#scrollTo=lOjlW3JWwDrB

In particolare ci sono quasi tutte le sperimentazioni che ho effettuato sia in ambito **AI** sia in ambito **Computer Vision**. Ho cercato di utilizzare tutti e due gli approcci, soprattutto per lavorare sul semaforo dopo la detection. 

##Introduzione
A fronte di idee propostemi da kaszuba@diag.uniroma1.it , sono arrivato a questa idea qui. Inizialmente il task doveva occupare un campo molto più ampio, ma sicuramente l'esperienza acquisita per risolvere questo 'problema' può risultare utile anche per spaziare eventualmente in futuro. 

L'utilizzo di segnali luminosi è molto diffuso in diversi ambiti, non solo per le strade ma anche in ambito industriale e agricolo come "controllori" del corretto funzionamento delle macchine.  Ad oggi, per verificare che funzionano, si utilizzano tendenzialmente cavi collegati direttamente al terminale che li gestisce. Tuttavia, soprattutto in grosse industrie, ci sono tanti device da controllare per cui, oltre ai costi, sorge un problema: chi controlla i controllori? Di solito vengono assunti degli addetti umani, ma perché farlo se possiamo risparmiare utilizzando un pc di fascia media e una telecamera neanche troppo dispendiosa? 

L'obiettivo di questo progetto è quindi di scandagliare tra le varie metodologie e trovare quelle più efficaci all'impronta dell'ergonomia. 

Purtroppo uno dei limiti era la mancanza di **dataset** specifici, per cui di fatto abbiamo certezze solo sui semafori.  In ogni caso la struttura di un segnale luminoso è sempre più o meno quella : tendenzialmente a colonna verticale od orizzontale, lente illuminata se si verifica una condizione, sennò spenta. 

##Dataset 
