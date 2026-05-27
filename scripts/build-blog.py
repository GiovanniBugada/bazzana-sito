"""
Generatore del blog "Note dal banco" — Motor Garden Bazzana.
12 articoli evergreen/stagionali + pagina indice.

Ogni articolo ha:
- HTML completo (header, footer, JSON-LD Article, OG meta)
- Categoria
- Hero image (riusa foto del catalogo/bazzana esistenti)
- Body strutturato con H2/H3
- Box "In sintesi"
- CTA contatto
- Nav prev/next
"""
from pathlib import Path
import re
import json

ROOT = Path(__file__).resolve().parent.parent
NOTE_DIR = ROOT / "note"
NOTE_DIR.mkdir(exist_ok=True)
INDEX_PATH = ROOT / "note.html"

SITE = "https://www.motorgardenbazzana.it"
NAV_DATE = "2026-05-25"

# ——— Articoli ———
ARTICLES = [
    {
        "slug": "affilatura-catena-motosega",
        "title": "Affilatura catena motosega",
        "subtitle": "ogni quanto e perché",
        "category": "Manutenzione",
        "date": "2026-05-25",
        "date_human": "25 Maggio 2026",
        "read": "5 min",
        "excerpt": "Una catena affilata taglia in 3 secondi quello che una catena consumata fa in 30. E consuma metà benzina. Quando va fatta, come si capisce, perché farla in officina.",
        "image": "assets/img/bazzana/scena-08.jpg",
        "body": """
<p>La catena della motosega è la lama che fa il lavoro vero. Tutto il resto — cilindrata, peso, ergonomia — non conta nulla se la catena è consumata. Eppure è la cosa che <strong>tutti trascurano per primi</strong>.</p>

<h2>Come capire che è ora di affilare</h2>
<p>Ci sono tre segnali inequivocabili. Se ne riconosci anche uno solo, è già tardi:</p>
<ul>
  <li><strong>La motosega non "tira giù" più da sola.</strong> Devi spingere sulla barra per farla penetrare nel legno. Una catena affilata cala da sola, la macchina la accompagni soltanto.</li>
  <li><strong>I trucioli sono polvere fine</strong>, simile a segatura. Una catena buona produce trucioli grossi, fettine di legno larghe almeno mezzo cm.</li>
  <li><strong>Il taglio è storto.</strong> Tagli dritto ma la spranga vira a destra o a sinistra — significa che i denti su un lato sono più consumati dell'altro.</li>
</ul>

<h2>Affilatura "fatta in casa" vs in officina</h2>
<p>Si può affilare a mano con lima tonda e portaguida. Funziona, ma <strong>devi conoscere il passo della catena</strong> (1/4", 0.325", 3/8" Low Profile, 3/8" Standard, 0.404"), l'angolo dei denti (di solito 30°), la profondità dei delimitatori e cambiare lima ogni 5-10 affilature.</p>
<p>In officina usiamo affilatrici elettriche calibrate: ogni dente esce con la stessa angolazione e la stessa lunghezza. La catena dura il doppio rispetto a una affilata male.</p>

<h2>Ogni quanto?</h2>
<p>Dipende da cosa tagli. Indicativamente:</p>
<ul>
  <li><strong>Legno tenero (abete, pioppo)</strong>: affilatura ogni 8-10 ore di taglio.</li>
  <li><strong>Legno duro (rovere, faggio, ulivo)</strong>: ogni 4-5 ore.</li>
  <li><strong>Legna a terra con sabbia o sporco</strong>: anche ogni ora. La sabbia consuma in 10 secondi quello che il legno consuma in un giorno.</li>
</ul>
<p>Una buona regola: <em>se durante il rifornimento di miscela ti sembra che la catena lavori peggio di prima, è ora di passarla.</em></p>

<h2>Quando cambiare la catena</h2>
<p>Una catena si può affilare 10-15 volte. Dopo, i denti sono diventati troppo piccoli per garantire un taglio efficace e sicuro. Verifica visivamente: se il dente è meno della metà della sua altezza originale, sostituiscila.</p>
<p>Anche la <strong>spranga</strong> ha vita limitata: tipicamente dura per 2-3 catene. Una spranga consumata genera vibrazioni, scarica più velocemente la catena e — peggio — può rompersi.</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Affila se la motosega non "scende" da sola o se i trucioli sono polvere.</li>
    <li>Affilatura in officina: catena dura il doppio.</li>
    <li>Legno duro = affilatura ogni 4-5h. Legno sporco = anche ogni ora.</li>
    <li>Dopo 10-15 affilature: si cambia.</li>
    <li>Spranga: cambia ogni 2-3 catene.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "rimessaggio-invernale-macchine",
        "title": "Rimessaggio invernale",
        "subtitle": "come preparare le macchine alla pausa",
        "category": "Stagionalità",
        "date": "2026-10-15",
        "date_human": "15 Ottobre 2026",
        "read": "6 min",
        "excerpt": "Una motosega lasciata con la miscela in carburatore per 4 mesi è una motosega che a marzo non parte. Tre operazioni che fanno la differenza fra una stagione e zero.",
        "image": "assets/img/bazzana/foto-067.jpg",
        "body": """
<p>L'inverno è il peggior nemico delle macchine a motore termico. Non il freddo in sé — quello, motoseghe e rasaerba lo reggono. Il problema è <strong>la benzina ferma</strong>, l'acqua di condensa, l'olio che decanta. Ad aprile parti, tiri la corda, niente. E pensi che la macchina sia rotta. Quasi mai lo è.</p>

<h2>1. Svuotare il serbatoio (o farlo girare a secco)</h2>
<p>La miscela 2 tempi inizia a degradarsi dopo 30 giorni. Dopo 90 giorni in serbatoio, il carburante diventa appiccicoso e ostruisce il carburatore. La gomma degli o-ring si secca. Il filtro intasa.</p>
<p>Soluzione: <strong>fai girare il motore al minimo finché non si spegne da solo</strong>. Così bruci anche il residuo nel carburatore. Operazione: 5 minuti. Costo: 0 €. Beneficio: la macchina parte ad aprile.</p>

<h2>2. Olio motore (per i 4 tempi: rasaerba, generatori, motozappe)</h2>
<p>L'olio motore "vecchio" contiene <strong>acidi che corrodono</strong> le superfici interne durante i mesi di fermo. Cambialo PRIMA dell'inverno, non dopo. Costo: 5-10 €. Beneficio: motore che dura 3-5 anni in più.</p>
<p>Per i motori Honda GCV (rasaerba HRX, HRN) e GX (motozappe, generatori): olio SAE 10W-30, capacità tipica 0.5-0.6 L.</p>

<h2>3. Pulizia accurata + grasso protettivo</h2>
<p>Erba secca, polvere, terra: sono spugna per umidità. Tutta l'umidità che assorbono durante l'inverno la cedono al metallo, che ruggina. Lava bene, asciuga, applica una pellicola di grasso protettivo (anche WD-40) su catena, lama, parti metalliche scoperte.</p>

<h2>Dove conservare</h2>
<p>Non in cantina umida. Non in garage chiuso ermeticamente. Idealmente: <strong>locale asciutto, ventilato, fresco</strong>. Se proprio devi tenerla in cantina, copri con telo traspirante (mai plastica chiusa: crea condensa).</p>

<h2>Batterie (Kress, robot, attrezzi a batteria)</h2>
<p>Le batterie al litio NON vanno conservate cariche al 100% né scariche a 0%. La conservazione ideale è al <strong>40-60% di carica</strong>, a temperatura ambiente. Sotto i 5°C la batteria si danneggia.</p>
<p>I robot tagliaerba con batteria integrata: lasciali in casa, NON sulla base esterna. La pioggia non li distrugge subito ma li accorcia la vita.</p>

<h2>Il servizio "rimessaggio" in officina</h2>
<p>Se non hai tempo o sicurezza per farlo bene: lo facciamo noi. Tagliando completo + pulizia + olio nuovo + grasso protettivo + ritiro a primavera, già controllato e pronto. Costo medio €50-80 a macchina. Vale tutto l'inverno tranquillo.</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Brucia la benzina nel carburatore: fallo girare al minimo finché non si spegne.</li>
    <li>Cambia l'olio PRIMA del fermo, non a marzo.</li>
    <li>Pulisci tutto, grasso protettivo su catena e parti metalliche.</li>
    <li>Batterie al litio: 40-60% di carica, in casa.</li>
    <li>Locale asciutto, ventilato, fresco. Mai chiuso in plastica.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "robot-tagliaerba-cosa-sapere",
        "title": "Robot tagliaerba",
        "subtitle": "tutto quello che devi sapere prima di comprarlo",
        "category": "Guida acquisto",
        "date": "2026-04-10",
        "date_human": "10 Aprile 2026",
        "read": "7 min",
        "excerpt": "Costa quanto 3 rasaerba normali ma ne sostituisce uno. Capisci se ne vale la pena per il tuo giardino — e cosa controllare prima di firmare.",
        "image": "assets/img/prodotti/foto-catalogo/Kress/Robot rasaerba/KR101E.webp",
        "body": """
<p>Il robot tagliaerba è probabilmente il prodotto del settore "verde" che divide di più. Chi ce l'ha non torna indietro. Chi non l'ha pensa sia spreco. La verità sta in mezzo, e dipende quasi tutto dalla forma del tuo giardino.</p>

<h2>Quando ha senso (3 scenari classici)</h2>
<ul>
  <li><strong>Giardino sopra i 500 m²</strong> con erba che cresce velocemente. Il robot taglia poco e spesso, l'erba resta sempre alla stessa altezza, non devi più "fare il prato" il sabato.</li>
  <li><strong>Persone occupate</strong> che vogliono prato perfetto senza tempo da dedicargli. Investimento iniziale alto, ma sostituisce 20 anni di sabati spesi col rasaerba.</li>
  <li><strong>Seconde case</strong> dove vai 2-3 volte al mese. Senza robot: trovi prato selvaggio. Con robot: trovi prato ordinato.</li>
</ul>

<h2>Quando NON ha senso</h2>
<ul>
  <li>Giardini molto piccoli (sotto i 200 m²): il rasaerba a spinta è più conveniente.</li>
  <li>Giardini con tanti ostacoli (vialetti, aiuole, fioriere): l'installazione del cavo perimetrale diventa complicata e antiestetica.</li>
  <li>Pendenze sopra il 35%: serve un modello specifico (più costoso). Se hai una scarpata, fattela controllare.</li>
</ul>

<h2>Cavo perimetrale vs senza cavo (GPS)</h2>
<p>I robot più moderni (es. Kress KR Series) lavorano <strong>senza cavo perimetrale</strong>, con GPS-RTK ad alta precisione. Vantaggi: niente filo nel prato, installazione più rapida, puoi modificare la zona di taglio dall'app.</p>
<p>I robot tradizionali (Stihl iMow, Husqvarna Automower base) usano il <strong>filo perimetrale</strong>: va interrato a 2-3 cm. Più economici (200-500 € in meno), ma se zappi nel giardino rischi di tagliarlo. Riparare il filo richiede tempo.</p>

<h2>Cose da chiedere prima di comprare</h2>
<ol>
  <li><strong>L'installazione è inclusa nel prezzo?</strong> Da noi sì (anche cavo, base, configurazione app, prima manutenzione). Diffida di chi te lo lascia in scatola.</li>
  <li><strong>Quanti anni di garanzia sulla batteria?</strong> 2 anni minimo, alcuni 3-5 anni. La batteria al litio è il pezzo che si consuma per primo.</li>
  <li><strong>Quanto costa il ricambio lame?</strong> Variano da 10 a 50 € per set. Si cambiano ogni 2-3 mesi durante la stagione.</li>
  <li><strong>L'app funziona offline?</strong> Alcune richiedono connessione obbligatoria al cloud del produttore. Se quel cloud chiude, il robot diventa "stupido". È capitato a più brand di smart home negli anni.</li>
</ol>

<h2>Costi reali di gestione</h2>
<ul>
  <li><strong>Lame</strong>: ~30-50 € l'anno</li>
  <li><strong>Batteria</strong>: ogni 5-7 anni, ~150-250 € sostituzione</li>
  <li><strong>Elettricità</strong>: trascurabile, ~5-10 € l'anno per giardini medi</li>
  <li><strong>Manutenzione officina</strong>: 1 tagliando l'anno consigliato, ~50-80 €</li>
</ul>

<h2>I modelli che teniamo</h2>
<p>Trattiamo principalmente <a href="../prodotti.html?q=Kress+KR">Kress KR Series</a> (GPS, senza filo, batteria potente) e <a href="../prodotti/stihl-imow.html">Stihl iMow 6 EVO</a> (cavo perimetrale, robusto, semplice da gestire). Il Kress è la scelta tech, lo Stihl quella sicura.</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Sì sopra i 500 m². Forse sotto. No sotto i 200 m².</li>
    <li>GPS = comodità, niente filo. Filo perimetrale = più economico.</li>
    <li>Chiedi che l'installazione sia inclusa, non solo "consigliata".</li>
    <li>Batteria si cambia ogni 5-7 anni. Mettilo in conto.</li>
    <li>App offline > app cloud-only.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "scegliere-prima-motosega",
        "title": "Scegliere la prima motosega",
        "subtitle": "evita gli errori da principiante",
        "category": "Guida acquisto",
        "date": "2026-09-12",
        "date_human": "12 Settembre 2026",
        "read": "6 min",
        "excerpt": "Comprare la motosega più potente non sempre è la scelta giusta. Per chi fa legna in proprio, conta più il peso e la lunghezza della spranga. Tre domande prima di entrare in negozio.",
        "image": "assets/img/prodotti/foto-catalogo/Active/Motoseghe/Da Abbattimento/56.56-300x300.webp",
        "body": """
<p>"Mi serve una motosega. Cosa prendo?" Domanda che riceviamo tutti i giorni. La risposta non è "questa", ma <strong>tre domande</strong> che dobbiamo farti prima.</p>

<h2>Domanda 1: cosa devi tagliare?</h2>
<ul>
  <li><strong>Rami fino a 15 cm di diametro</strong> (potatura, pulizia siepi, qualche tronchetto): basta una motosega da 30-35 cc, spranga 30-35 cm. Peso 3.5-4 kg. Esempi: Stihl MS 180, Active 31.</li>
  <li><strong>Legna da camino, alberi fino a 30 cm</strong> (uso "fai legna ogni inverno"): 40-45 cc, spranga 40 cm. Peso 4.5-5 kg. La <a href="../prodotti/stihl-ms-251.html">Stihl MS 251</a> è il cavallo da battaglia di questa categoria.</li>
  <li><strong>Alberi fino a 50 cm, abbattimenti seri</strong>: 50-60 cc, spranga 45-50 cm. Peso 5.5-6.5 kg. Active 56, Oleo-Mac GS 510.</li>
  <li><strong>Lavoro professionale, taglio in bosco quotidiano</strong>: 70 cc+, spranga 50-70 cm. Peso 7+ kg.</li>
</ul>

<h2>Domanda 2: quanto lavori in una giornata?</h2>
<p>Una motosega più potente di quello che ti serve è una motosega <strong>più pesante</strong>. E il peso, dopo 2 ore di lavoro, è quello che fa la differenza fra continuare e tornare a casa con la schiena rotta.</p>
<p>Esempio reale: se devi tagliare 20 ceppi all'anno, una 251 da 4.6 kg è perfetta. Se prendi una 462 da 6.0 kg "per sicurezza", la odi dopo il decimo taglio.</p>

<h2>Domanda 3: 2 tempi o batteria?</h2>
<h3>2 tempi (benzina + miscela)</h3>
<ul>
  <li><strong>Pro</strong>: potenza piena, autonomia infinita (riempi e vai), prezzo iniziale più basso, robustezza decennale.</li>
  <li><strong>Contro</strong>: rumore, peso più alto, miscela da preparare, manutenzione filtro/candela.</li>
</ul>

<h3>Batteria (Kress 60V, Echo eForce, Stihl AK/AP)</h3>
<ul>
  <li><strong>Pro</strong>: silenziosa, leggera, parte al primo colpo, zero manutenzione del motore, perfetta per uso "saltuario" o quartieri residenziali.</li>
  <li><strong>Contro</strong>: autonomia limitata (30-60 min per batteria), batteria di ricambio costosa (150-300 €), perde potenza con batteria scarica.</li>
</ul>

<p>Regola pratica: <strong>se la usi 1-2 ore al mese, batteria. Se la usi 1-2 ore al giorno, benzina.</strong></p>

<h2>Errori da evitare</h2>
<ol>
  <li><strong>Comprare online "perché costa 30€ in meno".</strong> La motosega NON è un elettrodomestico. Va provata, ti deve calzare in mano. E quando si rompe — succede a tutte — devi avere chi la ripara. Online: nessuno te la guarda.</li>
  <li><strong>Risparmiare sulla catena.</strong> Stihl, Oregon, Husqvarna fanno catene buone. Le marche generiche da Amazon durano un terzo, si rompono, e a volte sono pericolose.</li>
  <li><strong>Non comprare i DPI.</strong> Pantaloni antitaglio, guanti, casco con visiera e cuffie. Non è "esagerare" — è un'obbligo se vuoi vedere i tuoi figli adulti. Costo totale ~150 €, una volta.</li>
</ol>

<h2>Cosa ti consigliamo noi</h2>
<p>Per il 70% dei nostri clienti privati la risposta è una di queste tre:</p>
<ul>
  <li><a href="../prodotti.html?q=Active+motosega">Active 51.51</a> — Made in Italy, 51 cc, prezzo onesto, ricambi facili.</li>
  <li><a href="../prodotti/stihl-ms-251.html">Stihl MS 251</a> — la "Toyota" del mestiere, 45 cc, costo medio-alto ma dura una vita.</li>
  <li>Kress 60V CSA 200 (catalogo) — se preferisci la batteria.</li>
</ul>
<p>Vieni in negozio: te le facciamo prendere in mano. La differenza si sente subito.</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Cosa tagli? Quanto a lungo? Benzina o batteria?</li>
    <li>Più potente ≠ meglio. Pesa di più, ti stanchi prima.</li>
    <li>Batteria per uso saltuario. Benzina per uso pesante.</li>
    <li>Non comprare online: motosega va provata e curata.</li>
    <li>DPI sempre. 150 € che salvano dita.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "microcar-l6e-vs-50cc",
        "title": "Microcar L6e",
        "subtitle": "cosa cambia dal 50cc",
        "category": "Microcar",
        "date": "2026-06-08",
        "date_human": "8 Giugno 2026",
        "read": "5 min",
        "excerpt": "Stessa patente AM, stessa età minima, stessi 45 km/h. Ma la microcar è un'auto vera. Il 50cc è un motorino. Le differenze che pesano (e i costi reali).",
        "image": "assets/img/prodotti/foto-catalogo/Active/Generatori/INVERTER/3500I-300x300.webp",
        "body": """
<p>L'omologazione è la stessa: <strong>L6e</strong>. L'età minima per la guida è la stessa: <strong>14 anni</strong>. La velocità massima è la stessa: <strong>45 km/h</strong>. Eppure microcar e scooter 50 cc sono due mondi diversi. Capiamo perché.</p>

<h2>Cosa cambia davvero</h2>

<h3>Sicurezza</h3>
<p>Una microcar L6e (es. <a href="../prodotti/ligier-myli.html">Ligier Myli</a>) ha:</p>
<ul>
  <li><strong>Telaio</strong> con barre di rinforzo</li>
  <li><strong>Airbag</strong> (sui modelli più recenti)</li>
  <li><strong>Cinture di sicurezza</strong> a 3 punti</li>
  <li><strong>ABS</strong> sui modelli premium</li>
  <li><strong>Carrozzeria</strong> che ti protegge in caso di urto</li>
</ul>
<p>Uno scooter 50 cc ti lascia esposto. Una caduta a 30 km/h può finire male. Una microcar a 30 km/h ti porta in officina, non al pronto soccorso.</p>

<h3>Comodità</h3>
<ul>
  <li>Microcar: viaggi <strong>asciutto e al caldo</strong> sempre. Pioggia, neve, freddo: dentro stai bene.</li>
  <li>Scooter: con la pioggia ti bagni, d'inverno geli, d'estate sudi al semaforo.</li>
</ul>

<h3>Praticità</h3>
<ul>
  <li>Microcar: <strong>2 posti</strong>, bagagliaio per spesa/zaino scuola/sacche sport.</li>
  <li>Scooter: 1 posto (legalmente — anche se ne vedi due), sottosella per casco.</li>
</ul>

<h2>Costi a confronto (5 anni di uso)</h2>
<table style="width:100%; border-collapse: collapse; margin: 1.4rem 0; font-family: var(--font-mono); font-size: 0.85rem;">
  <thead>
    <tr style="border-bottom: 1px solid rgba(244,241,234,0.18); text-align: left;">
      <th style="padding: 0.5rem 0;">Voce</th>
      <th style="padding: 0.5rem 0;">Scooter 50cc</th>
      <th style="padding: 0.5rem 0;">Microcar L6e</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid rgba(244,241,234,0.08);"><td style="padding: 0.4rem 0;">Acquisto nuovo</td><td>~2.000 €</td><td>~12.000 €</td></tr>
    <tr style="border-bottom: 1px solid rgba(244,241,234,0.08);"><td style="padding: 0.4rem 0;">Assicurazione 5 anni</td><td>~1.500 €</td><td>~2.500 €</td></tr>
    <tr style="border-bottom: 1px solid rgba(244,241,234,0.08);"><td style="padding: 0.4rem 0;">Carburante 5.000 km/anno</td><td>~1.500 €</td><td>~700 € (elettrico)</td></tr>
    <tr style="border-bottom: 1px solid rgba(244,241,234,0.08);"><td style="padding: 0.4rem 0;">Manutenzione/usura</td><td>~1.000 €</td><td>~500 €</td></tr>
    <tr><td style="padding: 0.4rem 0;"><strong>Totale 5 anni</strong></td><td><strong>~6.000 €</strong></td><td><strong>~15.700 €</strong></td></tr>
  </tbody>
</table>
<p>La microcar costa il doppio, è vero. Ma ti dà sicurezza che <strong>non ha prezzo</strong>, soprattutto a 14 anni quando la maturità di guida non c'è ancora.</p>

<h2>Microcar elettrica o termica?</h2>
<p>Le elettriche oggi sono la scelta più diffusa, e per buone ragioni:</p>
<ul>
  <li>Ricarica da presa di casa (4-8 ore)</li>
  <li>Autonomia 90-190 km (a seconda del modello e batteria)</li>
  <li>Costo per km: ~6 centesimi di elettricità (vs ~10 cent. di benzina)</li>
  <li>Manutenzione meccanica quasi nulla (motore elettrico ha 2-3 parti in movimento, il termico ne ha 100+)</li>
  <li>Silenziose. Ottime in città.</li>
</ul>
<p>Le termiche restano valide in due casi: uso fuori città su strade extraurbane lunghe (autonomia infinita col pieno) e se non hai dove ricaricare (nessuna presa di casa raggiungibile).</p>

<h2>Patente AM: cosa serve sapere</h2>
<ul>
  <li>Età minima: 14 anni</li>
  <li>Costo patente: ~150-250 € (a seconda della scuola guida)</li>
  <li>Esame: teorico (quiz) + pratico (prova in pista)</li>
  <li>Validità: 10 anni, poi va rinnovata</li>
  <li>Con la patente B (>18 anni) puoi guidare anche L6e: non serve l'AM separata.</li>
</ul>

<h2>Le due microcar che teniamo</h2>
<p>In showroom hai due opzioni che rappresentano due filosofie diverse:</p>
<ul>
  <li><a href="../prodotti/ligier-myli.html"><strong>Ligier Myli</strong></a> — stile francese, ergonomia da auto vera, display 10", autonomia 192 km. 4 allestimenti.</li>
  
</ul>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Stessa patente AM, stessa età 14 anni, stessi 45 km/h.</li>
    <li>Microcar = auto vera (sicurezza, comfort, 2 posti). Scooter = motorino esposto.</li>
    <li>Costo: microcar 2.5x lo scooter su 5 anni.</li>
    <li>Elettrica meglio della termica in 90% dei casi (consumo, manutenzione, silenzio).</li>
    <li>Ligier Myli: il top di gamma microcar L6e per stile e autonomia.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "motozappa-vs-motocoltivatore",
        "title": "Motozappa o motocoltivatore?",
        "subtitle": "la differenza che conta",
        "category": "Orto e giardino",
        "date": "2026-03-15",
        "date_human": "15 Marzo 2026",
        "read": "4 min",
        "excerpt": "Sembrano la stessa cosa. Non lo sono. Una serve per dissodare l'orto, l'altra per arare a livello pro. Capisci subito quale ti serve.",
        "image": "assets/img/prodotti/foto-catalogo/Active/Motozappe/MOTOZAPPA-1100.webp",
        "body": """
<p>Domanda ricorrente in negozio, soprattutto a marzo. "Devo prendere una motozappa." Bene, ma intanto: stiamo parlando di motozappa o di motocoltivatore? Sono due macchine diverse.</p>

<h2>Motozappa: la più diffusa</h2>
<p>È quella con <strong>frese rotanti davanti</strong> e stegole dietro. La spingi/tiri tu, le frese fanno il lavoro. Adatta a:</p>
<ul>
  <li><strong>Orto familiare</strong> (fino a 500-800 m²)</li>
  <li><strong>Terreni già lavorati</strong>, che vanno rinfrescati ogni anno</li>
  <li><strong>Profondità di lavoro</strong> 15-25 cm (massimo)</li>
</ul>
<p>Peso tipico 40-70 kg. Si trasporta facilmente con un furgone o anche una station wagon (con le frese smontate). Prezzo: 400-1.500 €.</p>

<h2>Motocoltivatore: il fratello "grosso"</h2>
<p>Ha <strong>2 ruote motrici davanti</strong> e dietro attacchi vari (frese, aratro, rimorchio, falciatrice...). È una piccola trattrice. Adatto a:</p>
<ul>
  <li><strong>Orti grandi</strong> (oltre 1.000 m²) o piccoli campi</li>
  <li><strong>Terreni mai lavorati</strong> o molto duri</li>
  <li><strong>Multi-uso</strong>: con gli attacchi giusti fai aratura, fresatura, taglio erba, trasporto</li>
  <li><strong>Profondità</strong> 25-40 cm</li>
</ul>
<p>Peso tipico 80-200 kg. Molto più potente, molto più costoso. Prezzo: 1.500-5.000 €.</p>

<h2>Come capire quale ti serve</h2>
<p>Tre domande:</p>
<ol>
  <li><strong>Quanti metri quadri lavori?</strong> Sotto i 1.000: motozappa. Sopra: comincia a valere la pena di un motocoltivatore.</li>
  <li><strong>Il terreno è duro o già coltivato?</strong> Argilloso, sassoso, mai lavorato → motocoltivatore. Terra di campo già lavorata → motozappa.</li>
  <li><strong>Ti serve solo per l'orto o anche per altro?</strong> Solo orto: motozappa. Vuoi anche tagliare erba alta, trasportare letame, arare → motocoltivatore con attacchi.</li>
</ol>

<h2>Motore: benzina o batteria?</h2>
<p>Quasi tutte le motozappe oggi sono <strong>a benzina</strong>. Le elettriche esistono ma sono per orti minimi (50-100 m²). Per qualunque lavoro serio: benzina.</p>
<p>I motori più affidabili sono i <strong>Honda GP/GX</strong> (4 tempi) e i Briggs & Stratton. Partono sempre, anche dopo mesi di fermo (se hai fatto rimessaggio). Evita le motorizzazioni "asiatiche generiche" senza marca: 200 € risparmiati che diventano una rottura di scatole infinita.</p>

<h2>Le frese: parte critica</h2>
<p>Le frese si consumano. Dopo 5-10 stagioni di uso intenso vanno cambiate. Costano 50-150 €. <strong>Le frese in acciaio temprato durano il doppio</strong> di quelle in acciaio normale.</p>
<p>Diametro frese: 28-32 cm è lo standard. Più grandi (35-40 cm) servono per terreni duri o lavorazioni profonde.</p>

<h2>Cosa teniamo in showroom</h2>
<p>Per motozappe consigliamo principalmente <a href="../prodotti/active-mz-cm.html">Active MZ con Honda GP 160</a> (made in Italy, motore Honda, prezzo onesto). E i modelli Oleo-Mac (gamma più ampia per esigenze più grandi).</p>
<p>Per motocoltivatori: vendiamo su ordinazione, in base alle tue esigenze. Vieni in negozio, parliamone.</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Motozappa: orto familiare, terreni già lavorati, fino a 1.000 m².</li>
    <li>Motocoltivatore: orti grandi, terreni duri, multi-uso con attacchi.</li>
    <li>Motore Honda o B&S: affidabili. Evita marche generiche.</li>
    <li>Frese in acciaio temprato durano il doppio.</li>
    <li>Batteria solo per orto minimo. Tutto il resto: benzina.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "manutenzione-decespugliatore",
        "title": "Manutenzione decespugliatore",
        "subtitle": "il filo, la lama, il filtro aria",
        "category": "Manutenzione",
        "date": "2026-06-22",
        "date_human": "22 Giugno 2026",
        "read": "5 min",
        "excerpt": "Il decespugliatore è la macchina che lavoriamo di più in officina perché è quella che tutti usano peggio. Tre controlli che la fanno durare il doppio.",
        "image": "assets/img/prodotti/foto-catalogo/Active/Decespugliatori/Ad Asta Fissa/ST32.webp",
        "body": """
<p>Il decespugliatore è una macchina semplice: un motore, un asta, una testa rotante. Eppure è quella che vediamo più spesso al banco per problemi banali — quasi tutti evitabili con 10 minuti di manutenzione.</p>

<h2>Il filo: come cambiarlo (bene)</h2>
<p>Il filo nylon è il consumabile principale. Va cambiato:</p>
<ul>
  <li><strong>Diametro giusto</strong> per la testa: 2.0 mm per piccole superfici, 2.4 mm uso medio, 3.0 mm uso pro/sterpaglia.</li>
  <li><strong>Tipo profilato</strong> (sezione quadrata o spigolata): taglia il triplo del filo tondo standard. Costa il 20% in più ma ne vale la pena.</li>
  <li><strong>Avvolto stretto</strong> intorno alla bobina: se è lasco, si aggroviglia dopo 2 minuti di lavoro.</li>
</ul>

<h3>Errore comune</h3>
<p>"Lo lascio scarico, finché il filo non finisce." Sbagliato. Quando il filo è troppo corto, la testa lavora <strong>sbilanciata</strong>, vibra, rovina cuscinetti e supporti. Sostituisci appena il filo arriva a 4-5 cm dalla testa.</p>

<h2>La lama: quando va sostituita</h2>
<p>Le lame 3 denti o 4 denti per arbusti durano <strong>10-50 ore di lavoro</strong>, a seconda di cosa tagli e di come la usi.</p>
<p>Segnali che è ora di cambiare/affilare:</p>
<ul>
  <li>I denti sono visibilmente arrotondati o rotti</li>
  <li>Il decespugliatore "rimbalza" sui rami invece di tagliarli</li>
  <li>Vibrazioni anomale = lama sbilanciata o piegata</li>
</ul>
<p>Le lame 80 denti (a sega) per arbusti grossi vanno affilate ogni 5-8 ore: serve attrezzatura specifica. Le portiamo noi in officina, costo 10-15 €. Prova a farlo a casa e ti accorgi che non vale la pena.</p>

<h2>Il filtro aria: il killer silenzioso</h2>
<p>Il decespugliatore lavora in mezzo alla polvere. Il filtro aria intasa <strong>molto più velocemente</strong> di quello della motosega.</p>
<ul>
  <li><strong>Ogni 5-10 ore di lavoro</strong>: smontalo, soffialo con aria compressa (mai lavarlo se di carta).</li>
  <li><strong>Ogni 25-30 ore</strong>: sostituiscilo proprio. Costa 5-15 €, salva il motore.</li>
</ul>
<p>Un filtro intasato fa "soffocare" il motore: perde potenza, scalda, consuma il doppio di miscela. Dopo 50 ore di filtro non pulito, può grippare il pistone. Riparazione: 200-400 €. Filtro nuovo: 10 €.</p>

<h2>La candela: ogni inizio stagione</h2>
<p>Sgrassa, controlla la distanza degli elettrodi (di solito 0.5-0.7 mm), sostituisci se l'elettrodo è consumato o arrugginito. Spendi 5 €, eviti che a luglio la macchina non parta.</p>

<h2>La miscela: 1:50 per i 2 tempi</h2>
<p>La maggior parte dei decespugliatori a benzina sono <strong>2 tempi</strong>: serve miscela (benzina + olio sintetico 2T). Rapporto standard: <strong>50:1</strong> — 200 ml di olio per 10 L di benzina.</p>
<p>Errori da non fare:</p>
<ul>
  <li>Mai usare miscela vecchia di più di 30 giorni (separa olio e benzina, brucia male).</li>
  <li>Mai usare olio "auto" — è 4 tempi, non lubrifica.</li>
  <li>Mai aggiungere "più olio" pensando di proteggere meglio — sporca la candela.</li>
</ul>

<h2>Il tagliando di inizio stagione</h2>
<p>A marzo, prima della stagione, ti consigliamo un tagliando di un'ora in officina. Include: pulizia filtro aria, candela nuova, controllo carburatore, ingrassaggio testa, miscela fresca, controllo serraggio. Costo: 40-60 €. Beneficio: una stagione senza pensieri.</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Filo nylon: spigolato 2.4 mm per uso medio. Avvolto stretto.</li>
    <li>Lama: cambia/affila al primo segnale di vibrazione o rimbalzo.</li>
    <li>Filtro aria: soffia ogni 5-10h, cambia ogni 25-30h. Il killer silenzioso.</li>
    <li>Candela: controllo a inizio stagione, 5 € spesi bene.</li>
    <li>Miscela 50:1 sempre fresca. Mai più vecchia di 30 giorni.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "tagliasiepi-benzina-vs-batteria",
        "title": "Tagliasiepi: benzina o batteria?",
        "subtitle": "pro e contro veri (no marketing)",
        "category": "Guida acquisto",
        "date": "2026-05-08",
        "date_human": "8 Maggio 2026",
        "read": "4 min",
        "excerpt": "Le batterie sono migliorate moltissimo. Ma per certi lavori la benzina resta imbattibile. Capisci subito quale fa per te.",
        "image": "assets/img/prodotti/foto-catalogo/Active/tagliasiepi/SHARK_SITO_-300x300.webp",
        "body": """
<p>Per anni la risposta era ovvia: benzina, se vuoi lavorare seriamente. Oggi è meno ovvio. Le batterie al litio reggono bene il lavoro reale, e per molti utenti diventano la scelta giusta. Vediamo per chi.</p>

<h2>Tagliasiepi a benzina — punti di forza</h2>
<ul>
  <li><strong>Autonomia infinita</strong>: con un pieno di miscela lavori 1.5-2 ore continue. Riempi e via.</li>
  <li><strong>Potenza piena</strong>: tagli rami fino a 28-30 mm di diametro senza fatica. Le batterie scendono di potenza quando la batteria si scarica.</li>
  <li><strong>Robustezza</strong>: motori 2 tempi durano 10-15 anni se ben curati. Le batterie si degradano dopo 4-6 anni.</li>
  <li><strong>Lavoro in posti isolati</strong>: campagna, montagne, zone senza corrente per ricaricare. La benzina è universale.</li>
</ul>

<h3>Punti deboli</h3>
<ul>
  <li>Pesante (5-7 kg). Dopo un'ora si sente.</li>
  <li>Rumoroso (90-105 dB). Vicini felici? No.</li>
  <li>Vibrazioni. Stanca i polsi.</li>
  <li>Miscela da preparare e gestire.</li>
  <li>Avviamento a strappo (a volte serve insistere).</li>
</ul>

<h2>Tagliasiepi a batteria — punti di forza (oggi reali)</h2>
<ul>
  <li><strong>Silenzio</strong>: 70-80 dB. Lavori anche presto la mattina senza fastidio per nessuno.</li>
  <li><strong>Leggero</strong>: 2.5-4 kg. Lavoro più lungo possibile prima di stancarsi.</li>
  <li><strong>Avviamento istantaneo</strong>: premi il grilletto, parte. Sempre.</li>
  <li><strong>Zero manutenzione del motore</strong>: niente miscela, niente candela, niente filtro aria.</li>
  <li><strong>Vibrazioni quasi nulle</strong>: bene per chi ha problemi articolari.</li>
</ul>

<h3>Punti deboli</h3>
<ul>
  <li><strong>Autonomia</strong>: 40-90 min a batteria piena. Con siepi grandi serve una seconda batteria (costo 100-300 €).</li>
  <li>Costo iniziale alto se hai una sola batteria/caricabatterie.</li>
  <li>Potenza che cala con la carica.</li>
  <li>Batteria si degrada nel tempo (-20% dopo 4-5 anni di uso normale).</li>
  <li>Non taglia bene rami sopra i 22-24 mm.</li>
</ul>

<h2>Per chi è la batteria</h2>
<p>La batteria è giusta se:</p>
<ul>
  <li>Hai siepi piccole/medie (fino a 50 metri lineari)</li>
  <li>Usi il tagliasiepi <strong>poche volte al mese</strong></li>
  <li>Vuoi lavorare in orari "civili" senza disturbare</li>
  <li>Hai già altri attrezzi a batteria della stessa marca (Kress 60V, Stihl AP, Echo eForce)</li>
  <li>Sei più "casalingo" che professionista</li>
</ul>

<h2>Per chi è la benzina</h2>
<p>La benzina è giusta se:</p>
<ul>
  <li>Hai parchi, ville, condomini, terreni grandi</li>
  <li>Usi il tagliasiepi <strong>più ore consecutive</strong></li>
  <li>Tagli siepi grosse (oltre 25 mm di ramo)</li>
  <li>Sei un professionista del verde</li>
  <li>Lavori in posti senza corrente vicina</li>
</ul>

<h2>L'elettrico con cavo (vecchia scuola)</h2>
<p>Esiste ancora il tagliasiepi <strong>elettrico con cavo</strong>. Costa pochissimo (50-150 €), è leggero, ha potenza media, ma <strong>il cavo è un disastro</strong> nel lavoro reale: si impiglia, si taglia, ti limita all'estensione del filo. Sconsigliato salvo per piccoli giardini molto regolari.</p>

<h2>Cosa teniamo</h2>
<p>Lato benzina: <a href="../prodotti.html?q=Active+tagliasiepi">Active</a>, <a href="../prodotti/echo-hcr-185es.html">Echo HCR-185ES</a> (60 cm lama, professionale).</p>
<p>Lato batteria: gamma Kress 60V, Stihl HSA serie, Echo eForce. Tutti compatibili con batterie di altri attrezzi della stessa marca (se hai già il sistema, sfrutti la batteria).</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Benzina: lavoro pesante, siepi grandi, uso intensivo.</li>
    <li>Batteria: uso saltuario, silenzio, leggerezza, niente miscela.</li>
    <li>Elettrico con cavo: solo se proprio non puoi spendere e hai siepi minime.</li>
    <li>Se hai già altri attrezzi a batteria della stessa marca: prendi tagliasiepi della stessa famiglia.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "generatore-avr-inverter-sinusoidale",
        "title": "Generatore: AVR, inverter, sinusoidale?",
        "subtitle": "quale fa per te",
        "category": "Generatori",
        "date": "2026-07-20",
        "date_human": "20 Luglio 2026",
        "read": "5 min",
        "excerpt": "Comprato il generatore sbagliato → laptop bruciato. Le tre tecnologie disponibili e quale serve davvero, a seconda di cosa devi alimentare.",
        "image": "assets/img/prodotti/foto-catalogo/Active/Generatori/INVERTER/3500I-300x300.webp",
        "body": """
<p>"Mi serve un generatore." Domanda semplice, risposta che cambia tutto: <strong>per alimentare cosa?</strong> Una pompa d'acqua, un trapano, una luce ti accetta qualsiasi generatore. Un laptop, una scheda madre, un trapano cordless al carica → ti serve un certo tipo specifico. Sbagliare costa caro.</p>

<h2>Le tre famiglie</h2>

<h3>1. Generatore standard (a regolazione meccanica)</h3>
<p>Il più economico. Produce corrente alternata con una "qualità d'onda" approssimativa. Adatto per:</p>
<ul>
  <li>Utensili elettrici da cantiere (trapani, smerigliatrici, betoniere)</li>
  <li>Faretti alogeni o normali</li>
  <li>Pompe acqua, asciugacapelli, ferro da stiro</li>
</ul>
<p><strong>NON adatto per:</strong> elettronica sensibile (PC, TV, console, microonde digitali, ricariche batterie litio).</p>
<p>Prezzo: 200-500 €.</p>

<h3>2. Generatore con AVR (Automatic Voltage Regulator)</h3>
<p>Aggiunge un regolatore elettronico di tensione. La corrente è più "stabile" (non hai i cali di tensione tipici degli standard quando attacchi un carico pesante).</p>
<ul>
  <li>Va bene per quasi tutti gli utensili da cantiere</li>
  <li>Va bene per illuminazione, frigo, asciugacapelli</li>
  <li>Può alimentare alcuni elettrodomestici (lavatrice, microonde non digitale)</li>
</ul>
<p><strong>Ancora NON garantito per</strong>: PC, TV, console, dispositivi medicali, ricariche al litio.</p>
<p>Prezzo: 400-1.000 €.</p>

<h3>3. Generatore Inverter (sinusoidale pura)</h3>
<p>Il top per la qualità della corrente. La corrente in uscita è una <strong>sinusoide perfetta</strong>, identica a quella della rete elettrica casa. Sicura per tutto.</p>
<ul>
  <li><strong>Tutto</strong> quello che metteresti in casa: PC, server, TV, console, microonde, ricariche batterie, dispositivi medicali, attrezzature da palco/audio.</li>
  <li>Più <strong>silenziosi</strong> degli altri (48-58 dB vs 70-85 dB degli standard).</li>
  <li>Più <strong>efficienti</strong>: la modalità Eco-Throttle adatta i giri del motore al carico richiesto. Consumi dimezzati a basso assorbimento.</li>
  <li>Più <strong>leggeri</strong>.</li>
</ul>
<p>Prezzo: 700-2.500 €.</p>

<h2>Come scegliere</h2>

<h3>Domanda 1: cosa alimenti?</h3>
<ul>
  <li>Solo utensili da cantiere → standard o AVR</li>
  <li>Anche elettronica (PC, TV, ricariche) → <strong>SOLO inverter</strong></li>
  <li>Campeggio/camper con tutto incluso → inverter</li>
  <li>Eventi/concerti/audio → inverter sinusoidale pura</li>
</ul>

<h3>Domanda 2: quanta potenza?</h3>
<p>Somma i Watt di tutto quello che vuoi alimentare contemporaneamente. Aggiungi un 20-30% di margine per i picchi di avvio (motori, frigo).</p>
<p>Esempi pratici:</p>
<ul>
  <li>Camper con frigo + luci + ricariche: 1.500-2.000 W → inverter da 2.000-2.200 W</li>
  <li>Cantiere con trapano + smerigliatrice + faretti: 2.500-4.000 W → AVR da 4.000-5.000 W</li>
  <li>Casa in blackout (frigo + luci + TV + PC): 1.500-2.500 W → inverter da 2.200-3.000 W</li>
  <li>Tagliaerba elettrico professionale + caricabatterie: 1.500-3.000 W → inverter da 3.000 W</li>
</ul>

<h3>Domanda 3: ogni quanto lo userai?</h3>
<ul>
  <li>Uso saltuario (blackout 2 volte l'anno): standard/AVR economico va bene</li>
  <li>Uso frequente (camper, cantiere, eventi): inverter</li>
  <li>Uso quotidiano (mercati, lavoro in campagna): inverter premium (Honda EU22i o simili)</li>
</ul>

<h2>I modelli che teniamo</h2>
<p>Per uso "casa in emergenza / camper": <a href="../prodotti/honda-eu22i.html">Honda EU22i</a> — l'inverter più affidabile al mondo, 2.2 kW, 21 kg, silenziosissimo (48-57 dB).</p>
<p>Per uso cantiere/lavoro: gamma <a href="../prodotti.html?q=Oleo-Mac+Generatori">Oleo-Mac AVR</a> da 2.5 a 9.5 kW.</p>
<p>Per uso "tutti i giorni in agricoltura": gamma Active inverter da 2.1 e 3.5 kW.</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Standard: solo utensili da cantiere, niente elettronica.</li>
    <li>AVR: utensili + elettrodomestici base.</li>
    <li>Inverter sinusoidale: tutto, anche PC, TV, ricariche litio.</li>
    <li>Somma Watt + 20-30% di margine per picchi.</li>
    <li>Per la casa in blackout: scegli inverter, sempre.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "trattorino-vs-robot",
        "title": "Trattorino o robot?",
        "subtitle": "quando ha senso uno o l'altro",
        "category": "Tagliaerba",
        "date": "2026-04-25",
        "date_human": "25 Aprile 2026",
        "read": "5 min",
        "excerpt": "Due soluzioni completamente diverse per lo stesso problema (un prato grande). Capisci quale fa per te in base a giardino, tempo, budget.",
        "image": "assets/img/prodotti/foto-catalogo/Active/Tosaerba/Mulching/4760 SA.webp",
        "body": """
<p>Prato sopra i 1.000 m². Il rasaerba a spinta non basta più. Due alternative: <strong>trattorino</strong> o <strong>robot tagliaerba</strong>. Stesso problema, soluzioni opposte. Capiamo quale fa per te.</p>

<h2>Trattorino: la tradizione</h2>
<p>Lo conosciamo tutti. Macchina a sedere, motore davanti o dietro, tu guidi. Vantaggi reali:</p>
<ul>
  <li><strong>Velocità</strong>: tagli 1.500 m² in 30-45 minuti.</li>
  <li><strong>Raccolta efficiente</strong>: cesto da 200-300 L, ti fermi a vuotare ogni 1.000 m².</li>
  <li><strong>Robustezza</strong>: dura 15-20 anni con manutenzione minima.</li>
  <li><strong>Multi-uso</strong>: con attacchi puoi spalare neve, trasportare carriole, scarificare.</li>
  <li><strong>Pendenze</strong>: i trattorini stradard reggono fino al 15-20% di pendenza, alcuni modelli pro arrivano al 30%.</li>
</ul>

<h3>Svantaggi</h3>
<ul>
  <li>Investimento iniziale 1.500-5.000 €.</li>
  <li>Devi dedicargli tempo (1 ora settimanale).</li>
  <li>Rumoroso.</li>
  <li>Carburante.</li>
  <li>Ricovero invernale obbligatorio (occupa spazio).</li>
</ul>

<h2>Robot tagliaerba: il futuro (presente)</h2>
<p>Macchina autonoma che taglia da sola, tutti i giorni, poco alla volta. Vantaggi:</p>
<ul>
  <li><strong>Zero tempo</strong>: lo programmi una volta, lavora 5 anni.</li>
  <li><strong>Prato sempre perfetto</strong>: taglia 5-10 mm al giorno, l'erba non cresce mai abbastanza per "scappare".</li>
  <li><strong>Silenzioso</strong>: 55-65 dB, può lavorare anche di notte.</li>
  <li><strong>Mulching automatico</strong>: l'erba tagliata fertilizza il prato, niente sacchi da svuotare.</li>
  <li><strong>Pioggia, sole, freddo</strong>: lavora in qualunque condizione (entro i limiti del modello).</li>
</ul>

<h3>Svantaggi</h3>
<ul>
  <li>Investimento iniziale 1.500-4.500 €.</li>
  <li>Installazione (filo perimetrale o GPS) richiede setup iniziale.</li>
  <li>Lame e batteria sono consumabili: 50-300 €/anno mediamente.</li>
  <li>Non funziona bene con giardini molto complessi (tante aiuole, vialetti, alberi).</li>
  <li>Niente raccolta erba: se a te piace il "prato all'inglese taglio basso" senza una foglia per terra, il robot fa l'opposto (mulching).</li>
</ul>

<h2>Confronto diretto su 5 anni</h2>
<table style="width:100%; border-collapse: collapse; margin: 1.4rem 0; font-size: 0.9rem;">
  <thead><tr style="border-bottom: 1px solid rgba(244,241,234,0.18); text-align: left;"><th style="padding: 0.5rem 0;">Voce</th><th>Trattorino</th><th>Robot</th></tr></thead>
  <tbody>
    <tr style="border-bottom: 1px solid rgba(244,241,234,0.08);"><td style="padding: 0.4rem 0;">Acquisto</td><td>~2.500 €</td><td>~2.500 €</td></tr>
    <tr style="border-bottom: 1px solid rgba(244,241,234,0.08);"><td style="padding: 0.4rem 0;">Benzina 5 anni</td><td>~600 €</td><td>~50 € elettricità</td></tr>
    <tr style="border-bottom: 1px solid rgba(244,241,234,0.08);"><td style="padding: 0.4rem 0;">Manutenzione</td><td>~500 €</td><td>~600 € (lame+batt.)</td></tr>
    <tr style="border-bottom: 1px solid rgba(244,241,234,0.08);"><td style="padding: 0.4rem 0;">Tempo tuo (52 sab/anno x 1h x 5 anni)</td><td>260 ore</td><td>0 ore</td></tr>
    <tr><td style="padding: 0.4rem 0;"><strong>Totale</strong></td><td><strong>~3.600 € + 260h</strong></td><td><strong>~3.150 €</strong></td></tr>
  </tbody>
</table>

<h2>Quando trattorino, quando robot</h2>
<p><strong>Trattorino vince se:</strong></p>
<ul>
  <li>Vuoi il prato "tagliato corto" stile inglese</li>
  <li>Ti piace farlo (rilassante per molti)</li>
  <li>Hai giardino con tanti ostacoli (aiuole, alberi)</li>
  <li>Hai pendenze sopra il 35%</li>
  <li>Ti serve anche per altro (neve, trasporto)</li>
</ul>

<p><strong>Robot vince se:</strong></p>
<ul>
  <li>Non hai tempo o voglia di farlo</li>
  <li>Vuoi prato sempre perfetto senza "fare il giardino"</li>
  <li>Hai prato regolare con pochi ostacoli</li>
  <li>Pendenze gestibili (entro il 35-45% a seconda del modello)</li>
  <li>Sei spesso fuori casa</li>
</ul>

<h2>I modelli che teniamo</h2>
<p>Trattorini: gamma <a href="../prodotti.html?q=Active+Trattorini">Active</a> e Oleo-Mac, dai modelli "rider" da 70 cm di taglio fino ai più grandi per giardini da 3.000-5.000 m².</p>
<p>Robot: <a href="../prodotti/stihl-imow.html">Stihl iMow 6 EVO</a> per il classico cavo perimetrale, gamma Kress KR Series per la nuova generazione GPS senza filo.</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Trattorino: tu lo guidi, prato corto inglese, multi-uso, dura 15 anni.</li>
    <li>Robot: lavora da solo, mulching, prato sempre uniforme, niente tempo tuo.</li>
    <li>Costo simile su 5 anni, ma il robot ti regala 260 ore di vita.</li>
    <li>Pendenze >35% → trattorino o robot specifico.</li>
    <li>Giardino con tante aiuole → trattorino. Giardino regolare → robot.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "soffiatore-zaino-mano-batteria",
        "title": "Soffiatore: zaino, a mano, o batteria?",
        "subtitle": "la scelta giusta per ogni uso",
        "category": "Guida acquisto",
        "date": "2026-10-30",
        "date_human": "30 Ottobre 2026",
        "read": "4 min",
        "excerpt": "Autunno = foglie. Prima di comprare un soffiatore generico, capisci quale formato ti serve per evitare di pentirti dopo la prima ora di lavoro.",
        "image": "assets/img/prodotti/foto-catalogo/Oleo-Mac/Soffiatori per foglie/bv-300-s-1-1-300x300.webp",
        "body": """
<p>L'autunno è la stagione dei soffiatori. Il problema è che non sono tutti uguali. Comprare quello sbagliato significa lavorare il doppio. Tre famiglie, tre usi diversi.</p>

<h2>Soffiatore a mano (handheld)</h2>
<p>Il più diffuso. Piccolo, leggero (4-5 kg), tieni in una mano. Adatto per:</p>
<ul>
  <li>Cortili e vialetti privati</li>
  <li>Pulizia di foglie su balconi, terrazze</li>
  <li>Aree fino a 500 m²</li>
  <li>Uso saltuario (1-2 ore al massimo)</li>
</ul>
<p><strong>Limite</strong>: dopo 1 ora di uso il braccio non ti regge più. Per superfici grandi diventa stancante.</p>
<p>Esempio top di gamma: <a href="../prodotti/stihl-bg-86.html">Stihl BG 86</a> — 27 cc, 86 m/s di velocità aria, 4.4 kg.</p>

<h2>Soffiatore a zaino (backpack)</h2>
<p>Il motore sta sulla schiena, tu impugni solo il tubo. Adatto per:</p>
<ul>
  <li>Parchi, ville, scuole, condomini grandi</li>
  <li>Lavoro continuativo (3-5 ore consecutive)</li>
  <li>Aree dai 1.000 m² in su</li>
  <li>Uso professionale (manutentori del verde)</li>
</ul>
<p>Pesa di più (8-12 kg), ma il peso è sulla schiena → puoi lavorare per ore senza stancare il braccio. Più potente: 95-100 m/s di velocità aria, può spostare anche foglie bagnate.</p>
<p>Investimento iniziale 350-800 €, ma per chi lavora seriamente è l'unico che ha senso.</p>

<h2>Soffiatore a batteria</h2>
<p>Famiglia molto diffusa. Tre vantaggi reali:</p>
<ul>
  <li><strong>Silenzio</strong>: 60-75 dB vs 95-105 dB della benzina. Lavori anche presto la mattina o tardi senza disturbare.</li>
  <li><strong>Avviamento istantaneo</strong>.</li>
  <li><strong>Zero manutenzione motore</strong>.</li>
</ul>

<h3>Limiti reali</h3>
<ul>
  <li><strong>Autonomia</strong>: 20-50 min a batteria piena. Per uso pro serve una seconda batteria.</li>
  <li><strong>Potenza</strong>: i modelli a batteria oggi arrivano al 70-80% della potenza di un benzina equivalente. Bene per foglie secche, faticano con foglie bagnate o nevischio.</li>
  <li><strong>Costo iniziale alto</strong>: il pacco completo (soffiatore + batteria + caricabatterie) parte da 250-400 €.</li>
</ul>

<h2>Aspirazione + soffiaggio combinati</h2>
<p>Alcuni modelli (versioni "SHE" tipo Stihl BG 86 SHE) hanno la doppia funzione: <strong>soffi</strong> e poi puoi <strong>aspirare e trinciare</strong> le foglie. Il volume si riduce di 10:1, finisce in un sacco da svuotare.</p>
<p>Utile per chi vuole eliminare proprio le foglie (compostaggio, sacchetti differenziata). Senza aspirazione le foglie restano nel mucchio dove le hai radunate.</p>

<h2>Come scegliere</h2>
<ol>
  <li><strong>Quanti m² da pulire?</strong> Sotto 500 → handheld. 500-2.000 → zaino, oppure handheld potente. Oltre 2.000 → zaino professionale.</li>
  <li><strong>Quanto rumore puoi fare?</strong> Casa con vicini stretti, fascia oraria di lavoro civile → batteria. Campagna o spazi aperti senza vincoli → benzina.</li>
  <li><strong>Quanto a lungo lavori in una volta?</strong> Saltuario (max 1h) → handheld. Continuativo → zaino o doppia batteria.</li>
  <li><strong>Foglie bagnate o solo secche?</strong> Bagnate richiedono potenza vera (zaino benzina). Secche le sposti anche con batteria leggera.</li>
</ol>

<h2>Cosa NON fare</h2>
<ul>
  <li><strong>Non comprare modelli sotto i 100 €.</strong> Sono soffioni da poco, rotti dopo 1-2 stagioni, potenza insufficiente.</li>
  <li><strong>Non usare il soffiatore sui sassi o ghiaia.</strong> Sembra ovvio ma vediamo gente che lo fa: spara sassi a 100 km/h, romperà finestre o farà male a qualcuno.</li>
  <li><strong>Non lavorare senza cuffie antirumore.</strong> Anche per i modelli a batteria. Mezz'ora a quei livelli stressa l'udito.</li>
</ul>

<h2>I modelli che teniamo</h2>
<ul>
  <li>Handheld benzina: <a href="../prodotti/stihl-bg-86.html">Stihl BG 86</a></li>
  <li>Handheld batteria: gamma Stihl BGA, Kress 60V CSA</li>
  <li>Zaino benzina: Stihl BR 700, Oleo-Mac BV 300 S</li>
  <li>Combinato soffio+aspirazione: Stihl BG 86 SHE, Oleo-Mac BV 162</li>
</ul>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Handheld: cortili, vialetti, uso saltuario, sotto 500 m².</li>
    <li>Zaino: parchi, condomini, uso continuativo, oltre 1.000 m².</li>
    <li>Batteria: silenzio + leggerezza, ma con limiti di autonomia e potenza.</li>
    <li>Aspirazione+trinciatura: se vuoi eliminare le foglie nel sacco.</li>
    <li>Mai sotto i 100 €. Mai senza cuffie antirumore.</li>
  </ul>
</div>
""",
    },
    {
        "slug": "primavera-5-cose-prato-marzo",
        "title": "Marzo nel prato",
        "subtitle": "5 cose da fare a inizio stagione",
        "category": "Stagionalità",
        "date": "2026-03-01",
        "date_human": "1 Marzo 2026",
        "read": "5 min",
        "excerpt": "Il prato che vedi a giugno si decide a marzo. Cinque interventi rapidi che fanno la differenza per tutta la stagione successiva.",
        "image": "assets/img/bazzana/foto-098.jpg",
        "body": """
<p>Marzo è il mese più importante per chi tiene al prato. Quello che fai (o non fai) adesso si vede tutto l'anno. Cinque interventi rapidi, in ordine di importanza.</p>

<h2>1. Pulizia primaverile (la "rastrellatura della verità")</h2>
<p>Per primo: <strong>rimuovi il feltro</strong>. Dopo l'inverno, sul prato c'è uno strato di erba morta, foglie marcite, muschio. Si chiama "feltro" (thatch in inglese) e <strong>soffoca le radici nuove</strong>.</p>
<p>Si toglie con rastrello da prato (manuale per piccole aree) o con <strong>arieggiatore meccanico</strong> per superfici sopra i 200 m². L'arieggiatore "pettina" il prato in profondità, tira fuori il feltro, lascia il prato pulito.</p>
<p>Dopo l'arieggiatura il prato sembra distrutto. Non preoccuparti: in 2-3 settimane rinasce più folto.</p>

<h2>2. Concimazione di primavera</h2>
<p>Marzo-aprile = il prato si sveglia, ha bisogno di azoto per crescere foglie. Usa un <strong>concime granulare a lenta cessione</strong> con titolo azoto alto (es. 20-5-10 o 24-6-12). Distribuisci uniformemente con uno spandiconcime se hai superfici grandi.</p>
<p>Dose tipica: 30-40 g/m². Tradotto: 3-4 kg ogni 100 m² di prato. Costo: 20-40 €.</p>
<p>Innaffia subito dopo, altrimenti il concime "brucia" l'erba.</p>

<h2>3. Risemina dei punti vuoti</h2>
<p>Dopo l'inverno trovi spazi diradati, zone gialle, buchi. <strong>Reseminare adesso</strong>, prima che le malerbe occupino quegli spazi.</p>
<p>Procedura:</p>
<ol>
  <li>Smuovi leggermente il terreno coi denti di un rastrello</li>
  <li>Distribuisci semente da prato (mix Lolium + Festuca per uso domestico, ~30-40 g/m²)</li>
  <li>Copri leggermente con terriccio (1-2 mm)</li>
  <li>Innaffia delicatamente 2 volte al giorno per 10-14 giorni</li>
</ol>
<p>Tipo di semente: per giardino familiare cerca un "<strong>tappeto sportivo</strong>" o "rustico ornamentale". Per zone d'ombra esistono mix specifici. Costa 8-15 € al kg.</p>

<h2>4. Primo taglio: NON troppo basso</h2>
<p>Errore classico: prendere il rasaerba e tagliare a 3 cm la prima volta. <strong>Sbagliato</strong>. L'erba si stressa, si secca, lascia spazio a malerbe.</p>
<p>Regola: <strong>non togliere mai più di 1/3 dell'altezza</strong> al primo taglio. Se l'erba è alta 12 cm, taglia a 8 cm. La settimana dopo, da 8 a 5-6 cm. Poi mantieni 4-5 cm tutta la stagione.</p>
<p>Verifica anche la <strong>lama del rasaerba</strong>: se è arrugginita o consumata, "strappa" l'erba invece di tagliarla. Risultato: foglie sfilacciate, punte gialle, ingresso facile per malattie fungine. Affilatura/sostituzione lama: si fa in officina, 15-25 €.</p>

<h2>5. Controllo macchine (la nostra parte preferita)</h2>
<p>Prima di iniziare la stagione, dedica 30 minuti alle macchine. Se le hai fatto rimessaggio in autunno (<a href="rimessaggio-invernale-macchine.html">vedi nota dedicata</a>), basta poco. Altrimenti:</p>
<ul>
  <li><strong>Rasaerba</strong>: olio nuovo (se 4 tempi), candela controllata, lama affilata, ruote ingrassate.</li>
  <li><strong>Decespugliatore</strong>: filtro aria pulito, candela nuova, miscela fresca preparata.</li>
  <li><strong>Trattorino</strong>: batteria carica, tagliando completo se non l'hai fatto a ottobre.</li>
</ul>
<p>Tagliando di primavera in officina: 50-80 € a macchina, include tutto. Te le riconsegniamo pronte per essere tirare fuori senza pensieri.</p>

<div class="note-article__sintesi">
  <h3>In sintesi</h3>
  <ul>
    <li>Arieggia il prato: togli il feltro, le radici respirano.</li>
    <li>Concima granulare: 30-40 g/m², subito innaffiato.</li>
    <li>Risemina i punti vuoti prima che lo facciano le malerbe.</li>
    <li>Primo taglio mai sotto i 2/3 dell'altezza originale. Lama affilata.</li>
    <li>Controllo macchine: in officina o fai da te, ma prima di iniziare.</li>
  </ul>
</div>
""",
    },
]

# ——— Common HTML chunks ———
def page_head(title, description, slug=None):
    canonical = f"{SITE}/note/{slug}.html" if slug else f"{SITE}/note.html"
    og_image = f"{SITE}/assets/img/hero/facciata-esterna-rossa.jpg"
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="theme-color" content="#0E0F0E" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="{og_image}" />
<meta property="og:locale" content="it_IT" />
<link rel="canonical" href="{canonical}" />
<link rel="icon" type="image/svg+xml" href="../assets/favicon/favicon.svg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="image" href="../assets/brand/logo-bazzana.png" />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="../css/main.css?v=66" />
</head>
<body>

<a class="skip-link" href="#main">Vai al contenuto</a>

<div class="loader" aria-hidden="true">
  <div class="loader__inner">
    <div class="loader__logo">
      <div class="loader__logo-stage">
        <img src="../assets/brand/logo-bazzana.png" alt="" width="460" height="160" loading="eager" fetchpriority="high">
      </div>
    </div>
    <div class="loader__progress">
      <div class="loader__bar"></div>
      <div class="loader__meta">
        <span class="loader__brand">MOTOR GARDEN BAZZANA</span>
        <span class="loader__pct" aria-live="polite">000%</span>
      </div>
    </div>
  </div>
</div>

<header class="site-header">
  <div class="site-header__inner">
    <a class="brand" href="../index.html" aria-label="Motor Garden Bazzana — Home"><img class="brand__logo" src="../assets/brand/logo-bazzana.png" alt="Motor Garden Bazzana" width="240" height="80"></a>
    <nav class="nav" aria-label="Navigazione principale">
      <a href="../officina.html">Officina</a>
      <a href="../prodotti.html">Prodotti</a>
      <a href="../foto.html">Foto</a>
      <a href="../note.html" aria-current="page">Note</a>
      <a href="../storia.html">Storia</a>
      <a href="../contatti.html">Contatti</a>
    </nav>
    <div class="header-actions">
      <a class="tel-link" href="tel:+393464156981" data-cursor="Chiama">346 4156981</a>
      <button class="menu-toggle" aria-label="Apri menu"><span></span></button>
    </div>
  </div>
</header>

<div class="menu-overlay" aria-hidden="true">
  <div class="menu-overlay__top"><span class="mono">Menu</span><button class="menu-overlay__close" aria-label="Chiudi menu">×</button></div>
  <nav class="menu-overlay__list" aria-label="Menu mobile">
    <a href="../officina.html">Officina</a>
    <a href="../prodotti.html">Prodotti</a>
    <a href="../foto.html">Foto</a>
    <a href="../note.html">Note</a>
    <a href="../storia.html">Storia</a>
    <a href="../contatti.html">Contatti</a>
  </nav>
</div>
"""

FOOTER = """
<footer class="site-footer">
  <div class="site-footer__strip" aria-hidden="true">
    <div class="site-footer__strip-track">
      <span>Stihl official dealer</span><span class="site-footer__strip-dot"></span>
      <span>Officina autorizzata</span><span class="site-footer__strip-dot"></span>
      <span>Ricambi originali in 48h</span><span class="site-footer__strip-dot"></span>
      <span>Cene · Val Seriana</span><span class="site-footer__strip-dot"></span>
      <span>Aperti 2026 · esperienza decennale</span><span class="site-footer__strip-dot"></span>
      <span>Stihl · Active · Oleo-Mac · Kress · Shindaiwa · Ligier · Yashi · motori Honda</span><span class="site-footer__strip-dot"></span>
      <span>Stihl official dealer</span><span class="site-footer__strip-dot"></span>
      <span>Officina autorizzata</span><span class="site-footer__strip-dot"></span>
      <span>Ricambi originali in 48h</span><span class="site-footer__strip-dot"></span>
      <span>Cene · Val Seriana</span><span class="site-footer__strip-dot"></span>
    </div>
  </div>
  <div class="site-footer__inner">
    <div class="site-footer__main">
      <div class="site-footer__brand">
        <a class="site-footer__brand-mark" href="../index.html" aria-label="Motor Garden Bazzana — Home">
          <img src="../assets/brand/logo-bazzana.png" alt="Motor Garden Bazzana" width="200" height="68" loading="lazy">
        </a>
        <p class="site-footer__motto">Cene, valle Seriana.<br><em>Aperti 2026 — esperienza decennale.</em></p>
      </div>
      <nav class="site-footer__col" aria-label="Naviga">
        <h4 class="site-footer__h">Naviga</h4>
        <ul>
          <li><a href="../officina.html">Officina<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="../prodotti.html">Prodotti<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="../note.html">Note<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="../storia.html">Storia<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
          <li><a href="../contatti.html">Contatti<span class="site-footer__arrow" aria-hidden="true">→</span></a></li>
        </ul>
      </nav>
      <div class="site-footer__col">
        <h4 class="site-footer__h">Contatti</h4>
        <ul>
          <li><a href="tel:+393464156981">+39 346 4156981</a></li>
          <li><a href="https://wa.me/393464156981" target="_blank" rel="noopener">WhatsApp</a></li>
          <li><a href="mailto:bazzanamotorgarden@gmail.com">bazzanamotorgarden@gmail.com</a></li>
        </ul>
      </div>
      <div class="site-footer__col site-footer__col--find">
        <h4 class="site-footer__h">Trovaci</h4>
        <address class="site-footer__addr">Via U. Bellora, 73<br>24020 Cene (BG)<br>Italia</address>
      </div>
    </div>
    <div class="site-footer__bottom">
      <div class="site-footer__bottom-left">
        <span class="site-footer__copy">© <span data-year>2026</span> Motor Garden Bazzana</span>
        <span class="site-footer__sep" aria-hidden="true">·</span>
        <span>P.IVA 02234180169</span>
      </div>
      <nav class="site-footer__legal" aria-label="Legal">
        <a href="../privacy.html">Privacy</a>
        <a href="../index.html">Home</a>
      </nav>
      <span class="site-footer__credit">Cene · BG · Italia</span>
    </div>
  </div>
</footer>

<div class="fab-stack" id="fab-stack" aria-label="Azioni rapide">
  <a class="fab-stack__btn fab-stack__btn--wa" href="https://wa.me/393464156981" target="_blank" rel="noopener" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.05 4.91A9.82 9.82 0 0 0 12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01zM12.04 20.15c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.26 8.26 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.24-8.24 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c.02 4.54-3.68 8.23-8.22 8.23z"/></svg>
  </a>
  <a class="fab-stack__btn fab-stack__btn--phone" href="tel:+393464156981" aria-label="Chiama">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>
  <button class="fab-stack__btn fab-stack__btn--top" id="fab-top" aria-label="Torna su">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>
  </button>
</div>

<script src="../js/webp-upgrade.js?v=1" defer></script>
<script src="../js/main.js?v=45"></script>
<script src="../js/search-index.js?v=2" defer></script>
<script src="../js/search.js?v=4" defer></script>
<script src="../js/site-fx.js?v=50" defer></script>
<script src="../js/extras.js?v=41" defer></script>
</body>
</html>
"""

def article_jsonld(art):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{art['title']} — {art['subtitle']}",
        "description": art["excerpt"],
        "image": f"{SITE}/{art['image']}",
        "datePublished": art["date"],
        "dateModified": art["date"],
        "author": {"@type": "Organization", "name": "Motor Garden Bazzana"},
        "publisher": {
            "@type": "Organization",
            "name": "Motor Garden Bazzana",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/brand/logo-bazzana.png"}
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/note/{art['slug']}.html"}
    }, ensure_ascii=False)

def render_article(art, prev_art, next_art):
    head = page_head(
        f"{art['title']} — Note dal banco · Motor Garden Bazzana",
        art["excerpt"],
        slug=art["slug"]
    )
    nav_links = []
    if prev_art:
        nav_links.append(f'<a class="note-article__nav-link" href="{prev_art["slug"]}.html">← {prev_art["title"]}</a>')
    else:
        nav_links.append('<span></span>')
    if next_art:
        nav_links.append(f'<a class="note-article__nav-link" href="{next_art["slug"]}.html">{next_art["title"]} →</a>')
    else:
        nav_links.append('<span></span>')

    return f"""{head}
<script type="application/ld+json">{article_jsonld(art)}</script>

<main id="main" class="note-article">
  <p class="note-article__crumbs"><a href="../index.html">Home</a> / <a href="../note.html">Note dal banco</a> / {art['title']}</p>

  <header class="note-article__head">
    <span class="note-article__cat">{art['category']}</span>
    <h1>{art['title']}<br><em>{art['subtitle']}</em></h1>
    <div class="note-article__meta">
      <span>{art['read']} di lettura</span>
      <span>Note dal banco</span>
    </div>
  </header>

  <div class="note-article__hero-img">
    <img src="../{art['image']}" alt="{art['title']}" loading="eager">
  </div>

  <article class="note-article__body">
    {art['body'].strip()}
  </article>

  <aside class="note-article__cta">
    <h3>Vuoi un consiglio<br><em>diretto al banco?</em></h3>
    <p>Passa in showroom a Cene (BG) o scrivici. Ti diciamo cosa fa per te, senza la fretta di vendere.</p>
    <div class="note-article__cta-row">
      <a class="note-article__cta-btn note-article__cta-btn--primary" href="https://wa.me/393464156981?text=Ciao%2C%20ho%20letto%20la%20nota%20%22{art['slug']}%22%20e%20avrei%20una%20domanda" target="_blank" rel="noopener">WhatsApp →</a>
      <a class="note-article__cta-btn note-article__cta-btn--ghost" href="../contatti.html">Vieni a trovarci</a>
    </div>
  </aside>

  <nav class="note-article__nav" aria-label="Altre note">
    {nav_links[0]}
    {nav_links[1]}
  </nav>
</main>

{FOOTER}
"""

def render_index(arts):
    cats = sorted(set(a["category"] for a in arts))
    cat_chips = '<button class="note-index__filter is-active" data-filter="all">Tutte</button>\n'
    for c in cats:
        cat_chips += f'        <button class="note-index__filter" data-filter="{c}">{c}</button>\n'

    cards = ""
    for a in arts:
        cards += f"""        <a class="note-card" href="note/{a['slug']}.html" data-cat="{a['category']}">
          <div class="note-card__media">
            <img src="{a['image']}" alt="{a['title']}" loading="lazy">
            <span class="note-card__cat">{a['category']}</span>
          </div>
          <div class="note-card__body">
            <div class="note-card__meta">
              <span>{a['read']} di lettura</span>
              <span>Note dal banco</span>
            </div>
            <h2 class="note-card__title">{a['title']} — <em>{a['subtitle']}</em></h2>
            <p class="note-card__excerpt">{a['excerpt']}</p>
            <span class="note-card__read">Leggi <span aria-hidden="true">→</span></span>
          </div>
        </a>
"""

    head = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Note dal banco — Guide, manutenzione, consigli · Motor Garden Bazzana</title>
<meta name="description" content="Note tecniche dal banco di Motor Garden Bazzana: guide acquisto, manutenzione, consigli di stagione. Motoseghe, robot, rasaerba, microcar e altro." />
<meta name="theme-color" content="#0E0F0E" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Note dal banco — Motor Garden Bazzana" />
<meta property="og:description" content="Guide, manutenzione e consigli di stagione dal banco di Motor Garden Bazzana, Cene (BG)." />
<meta property="og:image" content="https://www.motorgardenbazzana.it/assets/img/hero/facciata-esterna-rossa.jpg" />
<meta property="og:locale" content="it_IT" />
<link rel="canonical" href="https://www.motorgardenbazzana.it/note.html" />
<link rel="icon" type="image/svg+xml" href="assets/favicon/favicon.svg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="image" href="assets/brand/logo-bazzana.png" />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="css/main.css?v=66" />
</head>
<body>

<a class="skip-link" href="#main">Vai al contenuto</a>

<div class="loader" aria-hidden="true">
  <div class="loader__inner">
    <div class="loader__logo">
      <div class="loader__logo-stage">
        <img src="assets/brand/logo-bazzana.png" alt="" width="460" height="160" loading="eager" fetchpriority="high">
      </div>
    </div>
    <div class="loader__progress">
      <div class="loader__bar"></div>
      <div class="loader__meta">
        <span class="loader__brand">MOTOR GARDEN BAZZANA</span>
        <span class="loader__pct" aria-live="polite">000%</span>
      </div>
    </div>
  </div>
</div>

<header class="site-header">
  <div class="site-header__inner">
    <a class="brand" href="index.html" aria-label="Motor Garden Bazzana — Home"><img class="brand__logo" src="assets/brand/logo-bazzana.png" alt="Motor Garden Bazzana" width="240" height="80"></a>
    <nav class="nav" aria-label="Navigazione principale">
      <a href="officina.html">Officina</a>
      <a href="prodotti.html">Prodotti</a>
      <a href="foto.html">Foto</a>
      <a href="note.html" aria-current="page">Note</a>
      <a href="storia.html">Storia</a>
      <a href="contatti.html">Contatti</a>
    </nav>
    <div class="header-actions">
      <a class="tel-link" href="tel:+393464156981" data-cursor="Chiama">346 4156981</a>
      <button class="menu-toggle" aria-label="Apri menu"><span></span></button>
    </div>
  </div>
</header>

<div class="menu-overlay" aria-hidden="true">
  <div class="menu-overlay__top"><span class="mono">Menu</span><button class="menu-overlay__close" aria-label="Chiudi menu">×</button></div>
  <nav class="menu-overlay__list" aria-label="Menu mobile">
    <a href="officina.html">Officina</a>
    <a href="prodotti.html">Prodotti</a>
    <a href="foto.html">Foto</a>
    <a href="note.html">Note</a>
    <a href="storia.html">Storia</a>
    <a href="contatti.html">Contatti</a>
  </nav>
</div>
"""

    footer_index = FOOTER.replace('../', '')

    body = f"""
<main id="main" class="note-index">
  <header class="note-index__hero">
    <p class="eyebrow">Note dal banco</p>
    <h1>Guide, manutenzione,<br><em>consigli di stagione.</em></h1>
    <p>Quello che diciamo al banco ai clienti che ci chiedono "ma quale prendo?", "come faccio a…", "ogni quanto si fa?". Scritto qui, gratis, senza giri di parole.</p>
  </header>

  <div class="note-index__filters" role="tablist" aria-label="Filtra per categoria">
        {cat_chips}
  </div>

  <div class="note-index__grid">
{cards}  </div>
</main>

{footer_index}

<script>
// Filtro categoria
(function() {{
  const chips = document.querySelectorAll('.note-index__filter');
  const cards = document.querySelectorAll('.note-card');
  chips.forEach(c => c.addEventListener('click', () => {{
    chips.forEach(x => x.classList.remove('is-active'));
    c.classList.add('is-active');
    const f = c.dataset.filter;
    cards.forEach(card => {{
      const ok = f === 'all' || card.dataset.cat === f;
      card.classList.toggle('is-filtered', !ok);
    }});
  }}));
}})();
</script>
"""
    return head + body

# ——— Build ———
# Sort articles by date (recent first)
arts_sorted = sorted(ARTICLES, key=lambda a: a["date"], reverse=True)

# Write each article
for i, art in enumerate(arts_sorted):
    prev_art = arts_sorted[i+1] if i+1 < len(arts_sorted) else None
    next_art = arts_sorted[i-1] if i > 0 else None
    out_path = NOTE_DIR / f"{art['slug']}.html"
    out_path.write_text(render_article(art, prev_art, next_art), encoding="utf-8")
    print(f"  scritto: note/{art['slug']}.html")

# Write index page
INDEX_PATH.write_text(render_index(arts_sorted), encoding="utf-8")
print(f"  scritto: note.html (index con {len(arts_sorted)} articoli)")

print(f"\nOK: {len(arts_sorted)} articoli + indice generati")
