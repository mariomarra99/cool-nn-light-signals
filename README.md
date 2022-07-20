<h1 id="h1-traffic-light-detection-classification"><a name="Traffic-light-detection-classification" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Traffic-light-detection-classification</h1><p>Progetto sulla ricerca di metodi per una efficace <strong>detection</strong> della location dei semafori e <strong>classification</strong> dei colori delle lenti.<br>Parte fondante e fondamentale sia per il progetto che per la presentazione si può trovare qui:<br><a href="https://colab.research.google.com/drive/16xmd3PJsmGA4x6rRYSjiZmGbOVb2SRzn?authuser=3#scrollTo=lOjlW3JWwDrB">https://colab.research.google.com/drive/16xmd3PJsmGA4x6rRYSjiZmGbOVb2SRzn?authuser=3#scrollTo=lOjlW3JWwDrB</a></p>
<p>In particolare ci sono quasi tutte le sperimentazioni che ho effettuato sia in ambito <strong>AI</strong> sia in ambito <strong>Computer Vision</strong>. Ho cercato di utilizzare tutti e due gli approcci, soprattutto per lavorare sul semaforo dopo la detection.</p>
<h2 id="h2-introduzione"><a name="Introduzione" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Introduzione</h2><p>A fronte di idee propostemi da <a href="mailto:kaszuba@diag.uniroma1.it" "="">kaszuba@diag.uniroma1.it</a> , sono arrivato a questa idea qui. Inizialmente il task doveva occupare un campo molto più ampio, ma sicuramente l’esperienza acquisita per risolvere questo ‘problema’ può risultare utile anche per spaziare eventualmente in futuro.</p>
<p>L’utilizzo di segnali luminosi è molto diffuso in diversi ambiti, non solo per le strade ma anche in ambito industriale e agricolo come “controllori” del corretto funzionamento delle macchine. Ad oggi, per verificare che funzionano, si utilizzano tendenzialmente cavi collegati direttamente al terminale che li gestisce. Tuttavia, soprattutto in grosse industrie, ci sono tanti device da controllare per cui, oltre ai costi, sorge un problema: chi controlla i controllori? Di solito vengono assunti degli addetti umani, ma perché farlo se possiamo risparmiare utilizzando un pc di fascia media e una telecamera neanche troppo dispendiosa?</p>
<p>L’obiettivo di questo progetto è quindi di scandagliare tra le varie metodologie e trovare quelle più efficaci all’impronta dell’ergonomia.</p>
<p>Purtroppo uno dei limiti era la mancanza di <strong>dataset</strong> specifici, per cui di fatto abbiamo certezze solo sui semafori. In ogni caso la struttura di un segnale luminoso è sempre più o meno quella : tendenzialmente a colonna verticale od orizzontale, lente illuminata se si verifica una condizione, sennò spenta. Ergo queste soluzioni possono essere adottate anche con colori diversi, forme delle lenti diversi e semafori diversi.</p>
<h4 id="h4-breve-trattazione-algoritmi-scartati"><a name="Breve trattazione algoritmi scartati" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Breve trattazione algoritmi scartati</h4><p>Prima di procedere alle soluzione, veloce ricapitolio di algoritmi utilizzati scartati o per malfunzionamento o per inefficienza o per poco sviluppo. Parlerò anche di <strong>detection</strong> delle lenti anche se nelle soluzioni finali non è presente: una delle strade che ho seguito inizialmente era la <strong>classificazione</strong> del colore dopo aver individuato la lente. In parte questo approccio comunque verrà sfruttato in una soluzione della <strong>classification</strong>.</p>
<p>Per la <strong>detection</strong> dei semafori e la <strong>detection</strong> delle lenti, ho provato ad utilizzare <strong>harris corner detector</strong>. Per immagini dettagliate funziona molto bene, riesce ad estrarre effettivamente tanti <strong>keypoints</strong>. Il problema è proprio quello: estrae troppe features. Inoltre, fa difficoltà a lavorare su immagini di qualità bassa con relativamente pochi pixel.</p>
<p>Per la <strong>detection</strong> delle regioni di interesse dei semafori (lenti), ho utilizzato <strong>blob detection</strong>. Su immagini molto dettagliate andava in <strong>‘overfitting’</strong>: effettuava detection di punti non davvero importanti. Per immagini poco dettagliate, non c’è molta affidabilità.</p>
<p>Per la <strong>classification</strong> del color, ho provato ad utilizzare <strong>K-nearest neighbors</strong> concatentato con l’individuazione dei <strong>centri</strong> delle lenti tramite un gioco di proporzioni matematiche. Il problema era che i <strong>centri</strong> non ci consentivano di avere certezze sulla location (se il semaforo è dispari va bene, ma se è pari? se non è perfettamente inquadrato?) né <strong>K-nearest neighbors</strong> era in grado di classificare i colori in modo efficace, la sua struttura non consente di dare risposte generalizzate su tante sfumature dei colori se non con attenzione particolareggiata al training.</p>
<h2 id="h2-dataset"><a name="Dataset" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Dataset</h2><p><strong>S2TLD</strong>: 5786 immagini di circa 1,080 x 1,920 pixels e 720 x 1,280 pixels. Contiene 5 categorie (Verde, Giallo, Rosso, wait on e off) di 14130 instances. Lo utilizzeremo sia per la verifica della <strong>detection</strong> che per quella della classification. <a href="https://github.com/Thinklab-SJTU/S2TLD">Link.</a></p>
<p><strong>jeremyscatigna/Traffic_light_classifier/traffic_light_images</strong>: derivativo del <strong>MIT self-driving car course</strong> , 1484 immagini che verranno portati a 32x32 pixel in fase di <strong>precompiling</strong>. Contiene tre categorie (Verde, Giallo, Rosso). Lo utilizzeremo per validare la <strong>classificazione</strong> e per il <strong>training</strong> di un algoritmo. <a href="https://github.com/jeremyscatigna/Traffic_light_classifier">Link.</a></p>
<h2 id="h2-precompiling"><a name="Precompiling" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Precompiling</h2><p><strong>S2TLD</strong> è strutturato in <strong>Annotations</strong> in xml, cartella contente le immagini e un file che contiene le class. Per rendere più facile la lettura delle annotations, le ho convertite in file .txt utilizzando la funzione <strong>annotation_xml_read(<em>filename</em>)</strong> che utilizza il lettore xml di pandas.</p>
<p>Estratto del dataset<br><img src="https://github.com/mariomarra99/cool-nn-light-signals/blob/main/images/S2TLD.png" alt="Estratto del dataset" title="Estratto del dataset"></p>
<p>Occorrono un paio di <strong>Annotations</strong> che fanno riferimento a immagini senza semafori, quindi a volte dà errore. Ho provveduto a creare “a mano” i corrispondente file .txt.</p>
<p>Per il <strong>dataset</strong> contenuto nella repository di <strong>jeremyscatigna</strong> invece procedo con l’approccio suggerito da <a href="https://github.com/jeremyscatigna/Traffic_light_classifier">lui stesso</a> nella <strong>Sezione 2</strong> per la prima soluzione di <strong>classification</strong> che andrò a presentare. Tuttavia per il <strong>training</strong> semplicemente porto le immagini a 32x32.</p>
<p><img src="https://github.com/mariomarra99/cool-nn-light-signals/blob/main/images/processing_steps.png" alt=""></p>
<h2 id="h2-la-coppia-vincente-detection-classification"><a name="La coppia vincente: Detection + Classification" class="reference-link"></a><span class="header-link octicon octicon-link"></span>La coppia vincente: Detection + Classification</h2><p>Tutte le soluzioni che adotteremo saranno essenzialmente strutturate così:</p>
<ul>
<li><strong>Detection</strong>: individuiamo in un’immagine dov’è il semaforo</li><li><strong>Classification</strong>: classifichiamo qual è il colore della lente luminosa del semaforo</li></ul>
<p>Una strategia molto semplice ma molto on-point sul lavoro che dobbiamo effettuare.</p>
