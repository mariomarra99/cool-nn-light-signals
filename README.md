<h1 id="h1-traffic-light-detection-classification"><a name="Traffic-light-detection-classification" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Traffic-light-detection-classification</h1><p>Progetto sulla ricerca di metodi per una efficace <strong>detection</strong> della location dei semafori e <strong>classification</strong> dei colori delle lenti.<br>Parte fondante e fondamentale sia per il progetto che per la presentazione si può trovare qui:<br><a href="https://colab.research.google.com/drive/16xmd3PJsmGA4x6rRYSjiZmGbOVb2SRzn?authuser=3#scrollTo=lOjlW3JWwDrB">https://colab.research.google.com/drive/16xmd3PJsmGA4x6rRYSjiZmGbOVb2SRzn?authuser=3#scrollTo=lOjlW3JWwDrB</a></p>
<p>In particolare ci sono quasi tutte le sperimentazioni che ho effettuato sia in ambito <strong>AI</strong> sia in ambito <strong>Computer Vision</strong>. Ho cercato di utilizzare tutti e due gli approcci, soprattutto per lavorare sul semaforo dopo la detection. I lanci dei programmi che ho utilizzato per rendicontare in questo <em>README</em> sono le <strong>ultime due sezioni</strong>.</p>
<h2 id="h2-introduzione"><a name="Introduzione" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Introduzione</h2><p>A fronte di idee propostemi da <a href="mailto:kaszuba@diag.uniroma1.it" "="">kaszuba@diag.uniroma1.it</a> , sono arrivato a questa idea qui. Inizialmente il task doveva occupare un campo molto più ampio, ma sicuramente l’esperienza acquisita per risolvere questo ‘problema’ può risultare utile anche per spaziare eventualmente in futuro.</p>
<p>L’utilizzo di segnali luminosi è molto diffuso in diversi ambiti, non solo per le strade ma anche in ambito industriale e agricolo come “controllori” del corretto funzionamento delle macchine. Ad oggi, per verificare che funzionano, si utilizzano tendenzialmente cavi collegati direttamente al terminale che li gestisce. Tuttavia, soprattutto in grosse industrie, ci sono tanti device da controllare per cui, oltre ai costi, sorge un problema: chi controlla i controllori? Di solito vengono assunti degli addetti umani, ma perché farlo se possiamo risparmiare utilizzando un pc di fascia media e una telecamera neanche troppo dispendiosa?</p>
<p>L’obiettivo di questo progetto è quindi di scandagliare tra le varie metodologie e trovare quelle più efficaci all’impronta dell’ergonomia.</p>
<p>Purtroppo uno dei limiti era la mancanza di <strong>dataset</strong> specifici, per cui di fatto abbiamo certezze solo sui semafori. In ogni caso la struttura di un segnale luminoso è sempre più o meno quella : tendenzialmente a colonna verticale od orizzontale, lente illuminata se si verifica una condizione, sennò spenta. Ergo queste soluzioni possono essere adottate anche con colori diversi, forme delle lenti diversi e semafori diversi.</p>
<h4 id="h4-breve-trattazione-algoritmi-scartati"><a name="Breve trattazione algoritmi scartati" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Breve trattazione algoritmi scartati</h4><p>Prima di procedere alle soluzione, veloce ricapitolio di algoritmi utilizzati scartati o per malfunzionamento o per inefficienza o per poco sviluppo. Parlerò anche di <strong>detection</strong> delle lenti anche se nelle soluzioni finali non è presente: una delle strade che ho seguito inizialmente era la <strong>classificazione</strong> del colore dopo aver individuato la lente. In parte questo approccio comunque verrà sfruttato in una soluzione della <strong>classification</strong>.</p>
<p>Per la <strong>detection</strong> dei semafori e la <strong>detection</strong> delle lenti, ho provato ad utilizzare <strong>harris corner detector</strong>. Per immagini dettagliate funziona molto bene, riesce ad estrarre effettivamente tanti <strong>keypoints</strong>. Il problema è proprio quello: estrae troppe features. Inoltre, fa difficoltà a lavorare su immagini di qualità bassa con relativamente pochi pixel.</p>
<p>Esempio: con tre iterazioni estrae tanti keypoints ma non individua i semafori se non in parte<br><img src="https://github.com/mariomarra99/cool-nn-light-signals/blob/main/images/road_harris.png" alt=""></p>
<p>Per la <strong>detection</strong> delle regioni di interesse dei semafori (lenti), ho utilizzato <strong>blob detection</strong>. Su immagini molto dettagliate andava in <strong>‘overfitting’</strong>: effettuava detection di punti non davvero importanti. Per immagini poco dettagliate, non c’è molta affidabilità.</p>
<p>Per il <strong>preprocessing</strong> dell’immagine, ho provato ad utilizzare una <strong>maschera</strong> basata sul formato <strong>HLS</strong>. Individuo le zone delle immagini più luminose, su un semaforo presumiamo siano le lenti illuminate, e applichiamo la maschera sull’immagine originale in <strong>RGB</strong>. Purtroppo funziona bene solo sulle immagini molto dettagliate e non dà garanzie su immagini con pochi pixel e/o sfocate. </p>
<p>Esempio output filtro:<br><img src="https://github.com/mariomarra99/cool-nn-light-signals/blob/main/images/green_mask.png" alt=""></p>
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
<h2 id="h2-traffic-light-detection"><a name="Traffic Light Detection" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Traffic Light Detection</h2><h3 id="h3-algoritmi-yolo"><a name="Algoritmi YOLO" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Algoritmi YOLO</h3><p><strong>YOLO (You Look Only Once)</strong> è una famiglia di algoritmi di object-detection in tempo reale sviluppata da <strong>Joseph Redmon</strong> e <strong>Ali Farhadi</strong> che negli ultimi tempi gode di ampio successo, sia per diffusione che per risultati.  Il loro obiettivo è di effettuare <strong>predict</strong> con una singola <strong>forward propagation</strong>. </p>
<p>Struttura YOLOv3:<br><img src="https://github.com/mariomarra99/cool-nn-light-signals/blob/main/images/yolov3_arch.png" alt=""></p>
<p>Gli algoritmi sono stati selezionati con criterio soprattutto a fronte della loro <strong>robustezza</strong> nell’individuare piccoli e grandi oggetti senza intaccare la qualità dell’immagine finale con un’architettura relativamente semplice (<strong>Layer convoluzionali</strong>, <strong>ResNet</strong> con <strong>ReLU</strong> e <strong>Batch Normalization</strong> , <strong>FPN</strong>, <strong>softmax</strong>,  <strong>Cross entropy</strong> come funzione di <strong>loss</strong>). Non mi soffermo nel funzionamento stretto dell’architettura in quanto non nell’obiettivo del progetto, tuttavia né studeriemo i risultati.</p>
<p>Noi per facilità d’uso utilizzeremo le implementazioni di <a href="https://github.com/ultralytics" title="ultralytics">ultralytics</a>, molto semplici da utilizzare in tutti i suoi aspetti.</p>
<h4 id="h4-yolov3"><a name="YOLOv3" class="reference-link"></a><span class="header-link octicon octicon-link"></span>YOLOv3</h4><p>Con <strong>61922845</strong> parametri, <strong>YOLOv3</strong> è il primo della famiglia a sfruttare <strong>FPN</strong>, un network in grado di prendere in input immagini di qualunque scala e di darle in output in maniera robusta a qulunque scala. Questa è la forza di <strong>YOLOv3</strong>: <strong>robustezza</strong>.</p>
<p>Per un veloce ricapitolio su cui mi sono formato rimando a <a href="http://https://towardsdatascience.com/yolo-v3-explained-ff5b850390f" title="qui">qui</a> e al <a href="https://arxiv.org/abs/1804.02767" title="paper">paper</a>.</p>
<h4 id="h4-yolov5"><a name="YOLOv5" class="reference-link"></a><span class="header-link octicon octicon-link"></span>YOLOv5</h4><p><strong>YOLOv5</strong> è una versione sviluppata da <strong>Glenn Jocher</strong>  con la seguente architettura:</p>
<pre class="prettyprint linenums prettyprinted" style=""><ol class="linenums"><li class="L0"><code><span class="typ">Backbone</span><span class="pun">:</span><span class="pln"> </span><span class="typ">New</span><span class="pln"> CSP</span><span class="pun">-</span><span class="typ">Darknet53</span></code></li><li class="L1"><code><span class="typ">Neck</span><span class="pun">:</span><span class="pln"> SPPF</span><span class="pun">,</span><span class="pln"> </span><span class="typ">New</span><span class="pln"> CSP</span><span class="pun">-</span><span class="pln">PAN</span></code></li><li class="L2"><code><span class="typ">Head</span><span class="pun">:</span><span class="pln"> </span><span class="typ">YOLOv3</span><span class="pln"> </span><span class="typ">Head</span></code></li></ol></pre><p>Questa struttura  inificia la robustezza, ma è caratterizzata da una maggiore <strong>precision</strong> e <strong>confidence</strong>. Noi visiteremo <strong>YOLOv5 nano</strong> con  <strong>1867405</strong> parametri, <strong>YOLOv5 medium</strong> con <strong>21172173</strong> parametri e <strong>YOLOv5 extreme 6</strong> con <strong>140730220</strong> parametri. Per i dettagli rimando al prossimo paragrafo.</p>
<p>Per la struttura di <strong>YOLOv5</strong> non c’è ancora un paper ma rimando a <a href="http://https://github.com/ultralytics/yolov5/issues/6998" title="qui">qui</a>.</p>
<h3 id="h3-sperimentazione"><a name="Sperimentazione" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Sperimentazione</h3><p>Effettuo le detect su un batch di <strong>400</strong> immagini presi da <strong>S2TLD</strong>. Utilizzo le implementazioni di <a href="https://github.com/ultralytics" title="ultralytics">ultralytics</a> con i <strong>pre-trained weight</strong> per facilità d’uso e accessibilità.</p>
<ul>
<li><strong>GPU</strong>: Tesla T4</li><li><strong>CPU</strong>: Intel(R) Xeon(R)</li></ul>
<p><strong>Metriche</strong>:</p>
<ul>
<li><strong>Precision</strong> : indicatore di <strong>prediction</strong> senza <strong>falsi positivi</strong>.</li><li><strong>Recall</strong> : indicatore di <strong>prediction</strong> senza <strong>falsi negativi</strong>.</li><li><strong>F1-score</strong>: verifica l’<strong>accuratezza</strong>, indicatore di <strong>robustezza</strong>, indica anche la correlazione tra <strong>precision</strong> e <strong>recall</strong>.</li><li><strong>mAP</strong>: indicatore principale di <strong>robustezza</strong> e <strong>accuratezza</strong> in quanto pesa molto di più la differenza tra <strong>precision</strong> e <strong>recall</strong>.</li><li><strong>IoU</strong>: <strong>Intersection over Union</strong>, indicatore dell’abilità dell’algoritmo di riuscire a effettuare <strong>detect</strong> di dimensioni più o meno vicine alla posizione reale dell’oggetto. Molto importante per gli algoritmi di <strong>detection</strong></li></ul>
<p>Impongo un <strong>vincolo</strong> basato anche su osservazioni empiriche : studio solo i casi con una <strong>confidence</strong> &gt; <strong>0.5</strong> . Di solito una <strong>confidence minore</strong> è direttamente proporzionale a <strong>distanze maggiori</strong>, per cui se lo montiamo su una macchina, grazie ai tempi molto brevi di calcolo delle <strong>predict</strong>, ci prendiamo il rischio. Inoltre, di fronte ad alcuni tiri di prova effettuati con <strong>confidence minore</strong>, otteniamo risultato molto meno uniformi e sensati.  </p>
<table>
<thead>
<tr>
<th>n = 400</th>
<th>Parametri</th>
<th>Precision</th>
<th>Recall</th>
<th>F1-Score</th>
<th>mAP</th>
<th>IoU</th>
<th>GPU</th>
<th>CPU</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>YOLOv3</strong></td>
<td>61922845</td>
<td>0.95</td>
<td><strong>0.43</strong></td>
<td><strong> 0.59</strong></td>
<td><strong>0.41</strong></td>
<td><strong>&gt;1.0</strong></td>
<td>25-30 secondi</td>
<td>10 minuti</td>
</tr>
<tr>
<td><strong>YOLOv5n</strong></td>
<td><strong>1867405</strong></td>
<td><strong>0.99</strong></td>
<td>0.23</td>
<td>0.34</td>
<td>0.25</td>
<td>0.93</td>
<td><strong>17-20 secondi</strong></td>
<td><strong>1 minuto</strong></td>
</tr>
<tr>
<td><strong>YOLOv5m</strong></td>
<td>21172173</td>
<td>0.96</td>
<td>0.31</td>
<td>0.47</td>
<td>0.30</td>
<td>~1.0</td>
<td>34-50 secondi</td>
<td><strong>1 minuto</strong></td>
</tr>
<tr>
<td><strong>YOLOv5x6</strong></td>
<td>140730220</td>
<td>0.95</td>
<td>0.3</td>
<td>0.46</td>
<td>0.29</td>
<td><strong>&gt;1.0</strong></td>
<td>40 - 50 secondi</td>
<td>NaN</td>
</tr>
</tbody>
</table>
<h3 id="h3-risultati-e-confronti"><a name="Risultati e Confronti" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Risultati e Confronti</h3><p>Notiamo come il confronto difatto è utile solo tra <strong>YOLOv3</strong> e <strong>YOLOv5n</strong> in quanto per <strong>YOLOv5m</strong> e <strong>YOLOv5x6</strong> il gioco non vale la candela. I parametri sono molti, il tempo impiegato è nettamente superiore ai primi due e le metriche non sono entusiasmanti. Inoltre evidenziamo già da adesso quanto sia difficile per questo task individuare i <strong>falsi negativi</strong>, i valori di <strong>recall</strong> sono tutti sotto lo <strong>0.5</strong>.</p>
<p>Notiamo, come previsto, una maggiore <strong>mAP</strong> per <strong>YOLOv3</strong>. Questo è un indicatore di quanto sia <strong>robusto</strong>, in grado molto di più rispetto agli altri sia di evitare i <strong>falsi positivi</strong> e i <strong>falsi negativi</strong>. La <strong>IoU</strong> è praticamente perfetta. Tuttavia ha molti <strong>parametri</strong>, che diminuisce di molto la <strong>portabilità</strong> dell’algoritmo.</p>
<p>Invece per <strong>YOLOv5n</strong> abbiamo un numero molto minore di <strong>parametri</strong>, che ne aumenta la <strong>portabilità</strong>, e tempi <strong>minori</strong> nell’effettuare predizioni. Ciò consente di dare più tempo alla macchina di prendere decisioni. Tuttavia ha una <strong>robustezza</strong> e una <strong>IoU</strong> minore. Nota di merito è il fatto che su una <strong>CPU</strong> destinata a diventare media nei prossimi anni, impiega <strong>1 minuto</strong>. Niente. </p>
<p>Facendo un confronto tra le <strong>inferenze</strong> effettuate con le <strong>GPU</strong> e la <strong>CPU</strong>, generalmente i tempi delle <strong>GPU</strong> sono molto minori mentre le <strong>metriche</strong> legate alla <strong>CPU</strong> sono più solide e migliori.</p>
<p>Confronto YOLOv3 vs YOLOv5n:<br><img src="https://github.com/mariomarra99/cool-nn-light-signals/blob/main/images/y3_vs_y5n.png" alt=""></p>
<h2 id="h2-color-classification"><a name="Color Classification" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Color Classification</h2><h3 id="h3-hsv-classifier"><a name="HSV classifier" class="reference-link"></a><span class="header-link octicon octicon-link"></span>HSV classifier</h3><p>L’approccio più legato alla <strong>Computer Vision</strong> nel senso stretto del termine.<br>Il suo funzionamento è molto semplice: prendo un semaforo, faccio uno slice dell’immagini dividendolo in tre parti, individuo attraverso una somma qual è l’immagine con una <strong>brigthness</strong> maggiore (presumibilmente quella dove è contenuta la lente più luminosa e di interesse) e la seleziono. <strong>Veloce</strong> e computazionalmente <strong>efficiente</strong>.</p>
<p>Pur provenendo da un’intuizione personale, ho trovato un metodo molto efficace proposto proprio dalla <a href="http://https://github.com/jeremyscatigna/Traffic_light_classifier" title="stessa repository">stessa repository</a> del secondo <strong>dataset</strong>.</p>
<p><img src="https://github.com/mariomarra99/cool-nn-light-signals/blob/main/images/feature_ext_steps.png" alt=""></p>
<h3 id="h3-k-means-clustering"><a name="K-Means Clustering" class="reference-link"></a><span class="header-link octicon octicon-link"></span>K-Means Clustering</h3><p><strong>K-Means</strong> è un algoritmo di <strong>clustering</strong> che si pone come obiettivo di <strong>minimizzare</strong> la <strong>varianza</strong> totale intra-gruppo, ogni gruppo viene identificato mediante un <strong>centroide</strong> o punto medio e partiziona l’insieme di dati in <strong>k</strong> gruppi. </p>
<p>Ma se il <strong>centroide</strong> ce lo abbiamo già? Possiamo trasformarlo in un algoritmo di classificazione. La scelta arbitraria dei <strong>centroidi</strong> ci dà un grado di libertà molto ampio che consente di rendere la classificazione <strong>versatile </strong> e di spaziare tra tanti colori.</p>
<p>Esempio dei colori estratti da K-Means:<br><img src="https://github.com/mariomarra99/cool-nn-light-signals/blob/main/images/clustering.png" alt=""></p>
<h3 id="h3-decision-tree"><a name="Decision Tree" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Decision Tree</h3><p><strong>Decision Tree</strong> è un algoritmo di <strong>machine learning supervisionato</strong> utilizzato per classificare in base a decisioni (<strong>label</strong>) a fronte di dati (<strong>input</strong>)  già inseriti. <strong>Training</strong> veloce e semplice.</p>
<h3 id="h3-sperimentazioni"><a name="Sperimentazioni" class="reference-link"></a><span class="header-link octicon octicon-link"></span>Sperimentazioni</h3><p>In quanto due metodi non sono computazionalmente molto impegnativi, non facciamo distinzione tra <strong>GPU</strong> e <strong>CPU</strong>. </p>
<p>Invece è importante verificare che sia efficace sia su un <strong>dataset</strong> “nativo” (dove viene effettuato il <strong>training</strong> oppure su cui è testato l’algoritmo) sia su un <strong>dataset</strong> che risponde all’esigenza reale di <strong>classification</strong> dopo la detection di <strong>YOLO</strong>. Quindi:</p>
<ul>
<li><strong>Dataset #1</strong>: <strong>jeremyscatigna</strong> su un numero di immagini determinato da <strong>YOLO</strong>.<ul>
<li><strong>HSV</strong> : <strong>488</strong> immagini.<br>-<strong>K-Means</strong> : <strong> 335 </strong> immagini.<br>-<strong>DT</strong> : <strong> x </strong> immagini.</li></ul>
</li><li><strong>Dataset #2</strong>: <strong>S2TLD</strong> su <strong>306</strong> immagini.</li></ul>
<p><strong>Metrica</strong>:</p>
<ul>
<li><strong>Precision</strong>: difatto l’unica metrica utile a questo scopo in quanto non ci sono <strong>true negative</strong> da classificare, indica quanti <strong>falsi positivi</strong> influiscono sull’output.</li></ul>
<p><strong>Vincoli HSV classifier</strong>:</p>
<ul>
<li>Assume che il semaforo sia a tre lenti</li><li>Assume che ci sia solo una lente più luminosa</li><li>Assume che i colori siano solo tre e sempre nella stessa posizione (verde, giallo, rosso)</li></ul>
<p><strong>Vincoli K-Means Clustering</strong>:</p>
<ul>
<li>Assume che ci sia solo una lente luminosa</li><li>Ricerca dei <strong>Centroidi</strong></li><li>Computazionalmente impegnativo </li></ul>
<p><strong>Vincoli Decision Tree</strong>:</p>
<ul>
<li>C’è bisogno di <strong>training</strong> :  può essere sia un vantaggio che uno svantaggio. Nello scenario di ampia disponibilità di <strong>dataset</strong> è un vantaggio, sennò va fatto un lavoro annoso.</li></ul>
<table>
<thead>
<tr>
<th></th>
<th>Precision Dataset #1</th>
<th>Precision Dataset #2</th>
<th>n. Vincoli</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>HSV</strong></td>
<td><strong>0.97</strong></td>
<td><strong>0.92</strong></td>
<td>3</td>
</tr>
<tr>
<td><strong>K-Means</strong></td>
<td>0.94</td>
<td>0.91</td>
<td>3</td>
</tr>
<tr>
<td><strong>DT</strong></td>
<td><strong>0.97</strong></td>
<td>x</td>
<td><strong>0 - 1</strong></td>
</tr>
</tbody>
</table>
<p><strong>HSV Classifier</strong> ha vincoli molto stringenti, questo non gli consente di <strong>generalizzare</strong> ma in compenso ha una <strong>precision</strong> molto efficace. </p>
<p><strong>K-Means Clustering</strong> invece è efficace ma necessita una ricerca <strong>ad hoc</strong> del <strong>centroide</strong> per ogni <strong>dataset</strong>. Inoltre per effettuare <strong>classificazione</strong> sul <strong>Dataset #1</strong> impiega <strong>20 minuti</strong>…</p>
<p><strong>Decision Tree</strong> <strong>allenato</strong> ( in un <strong>1 secondo</strong>) sul <strong>training dataset</strong> di <strong>Dataset #1</strong> con un <strong>resize</strong> di <strong>32x32</strong> e una <strong>depth</strong> di <strong>3</strong> ha la <strong>precision</strong> migliore in proporzione ai <strong>vincoli</strong>. </p>
<p><img src="https://github.com/mariomarra99/cool-nn-light-signals/blob/main/images/tree_struct.png" alt=""></p>
<p>Sul <strong>Dataset #2</strong> non sono riuscito a effettuare <strong>prediction</strong> per problemi tecnici all’ultimo minuto. In ogni caso mi aspetto risultati soddisfacenti soprattuto a fronte di <strong>resize</strong> e della <strong>generalizzazione</strong> che offre la <strong>profondità</strong> non elevata dell’algoritmo.</p>
