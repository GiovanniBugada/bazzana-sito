/* Motor Garden Bazzana — dati prodotti
   Specs e caratteristiche dai dati ufficiali dei produttori
   (Stihl, Active, Oleo-Mac, Kress, Shindaiwa, Ligier, Geotech, motori Honda).
*/
window.BAZZANA_PRODUCTS = [
  {
    slug: 'stihl-ms-251',
    brand: 'Stihl',
    model: 'MS 251',
    modelFull: 'Stihl MS 251 C-BE',
    category: 'Motosega da bosco',
    tagline: 'Da bosco, vera.',
    lead: 'Equilibrio fra leggerezza e potenza. La motosega che serve a chi taglia legna ogni stagione, non solo a Natale.',
    description: 'Motore 2-MIX 45.6 cc a basse emissioni, con lubrificazione automatica della catena e freno catena Quickstop Super. La spranga 45 cm permette tagli puliti su tronchi fino a 40 cm di diametro. Per chi fa legna in proprio, taglio rami grossi, abbattimento di alberi medi: copre tutto senza pesare troppo sulla spalla in mezza giornata di lavoro.',
    specs: [
      { label: 'Cilindrata', value: '45.6 cc' },
      { label: 'Potenza', value: '2.2 kW · 3.0 CV' },
      { label: 'Spranga', value: '45 cm' },
      { label: 'Peso a vuoto', value: '4.6 kg' },
      { label: 'Capacità serbatoio', value: '0.50 L' },
      { label: 'Garanzia', value: '2 anni' }
    ],
    highlights: [
      { title: 'Motore 2-MIX', value: 'Riduce consumi ed emissioni fino al 20% rispetto a un 2 tempi tradizionale.' },
      { title: 'ErgoStart (E)', value: 'Avviamento dolce anche a freddo: meno strappi sulla corda.' },
      { title: 'Quickstop Super', value: 'Freno catena con attivazione inerziale per arresto immediato in caso di rinculo.' }
    ]
  },
  {
    slug: 'stihl-fs-131',
    brand: 'Stihl',
    model: 'FS 131',
    modelFull: 'Stihl FS 131',
    category: 'Decespugliatore professionale',
    tagline: 'La spalla destra di chi taglia.',
    lead: 'Motore 4-MIX di Stihl: meno emissioni, più coppia, niente miscela complicata da preparare.',
    description: 'Cilindrata 36.3 cc con motore 4-MIX a 4 tempi che gira a benzina-olio. Manubrio a due impugnature, cinghia ergonomica, accessori intercambiabili (testina filo AutoCut, lama 3 denti, lama 80 denti per arbusti). Per professionisti del verde, agricoltori part-time, comuni: tiene tutto il giorno e affronta erba alta, sterpi, piccoli polloni senza calare di giri.',
    specs: [
      { label: 'Cilindrata', value: '36.3 cc · motore 4-MIX' },
      { label: 'Potenza', value: '1.4 kW · 1.9 CV' },
      { label: 'Peso', value: '5.8 kg' },
      { label: 'Capacità serbatoio', value: '0.71 L' },
      { label: 'Livello vibrazioni', value: '3.5 / 3.5 m/s²' },
      { label: 'Garanzia', value: '2 anni privati' }
    ],
    highlights: [
      { title: 'Motore 4-MIX', value: 'Coppia tipica di un 4 tempi, semplicità di manutenzione di un 2 tempi.' },
      { title: 'ElastoStart', value: 'Maniglia avviamento ammortizzata che assorbe i picchi di forza iniziali.' },
      { title: 'Manubrio bike-handle', value: 'Doppia impugnatura per controllo in piano su grandi superfici.' }
    ]
  },
  {
    slug: 'stihl-bg-86',
    brand: 'Stihl',
    model: 'BG 86',
    modelFull: 'Stihl BG 86',
    category: 'Soffiatore a benzina',
    tagline: 'L’autunno, ripulito in mezz’ora.',
    lead: 'Velocità dell’aria a 86 m/s, regolatore di gas al pollice, peso contenuto. Per cortili, viali, vialetti, piazzali.',
    description: 'Motore 2-MIX da 27.2 cc a basso consumo con tubo soffiatore facilmente smontabile per il trasporto. Comando dell’acceleratore con fermo per uso prolungato senza affaticare il dito. Volume aria 810 m³/h: sposta foglie bagnate, taglio d’erba, polvere fine dai capannoni. La versione SHE (a richiesta) aggiunge funzione aspirazione e trinciatura del fogliame.',
    specs: [
      { label: 'Cilindrata', value: '27.2 cc' },
      { label: 'Velocità aria', value: '86 m/s' },
      { label: 'Volume aria', value: '810 m³/h' },
      { label: 'Peso', value: '4.4 kg' },
      { label: 'Capacità serbatoio', value: '0.44 L' },
      { label: 'Garanzia', value: '2 anni' }
    ],
    highlights: [
      { title: 'Motore 2-MIX', value: 'Tre canali di travaso: meno benzina sprecata, più ore di lavoro.' },
      { title: 'Comando multifunzione', value: 'Acceleratore, fermo gas e stop tutti gestiti con una mano.' },
      { title: 'Versione SHE', value: 'Optional di aspirazione/trinciatura: riduce il volume foglie ~10:1.' }
    ]
  },
  {
    slug: 'stihl-imow',
    brand: 'Stihl',
    model: 'iMow 6 EVO',
    modelFull: 'Stihl iMow 6 EVO',
    category: 'Robot tagliaerba',
    tagline: 'Il prato si fa da solo.',
    lead: 'App nello smartphone, GPS antifurto, taglio in fasce parallele. Lo installiamo noi, lo manuteniamo noi.',
    description: 'Robot pensato per giardini fino a 4.000 m², capace di gestire pendenze fino al 45%. Programma automaticamente le sessioni in base alla crescita dell’erba e meteo, comunica via Bluetooth e iMow App. Sensori antiurto, antisollevamento, allarme con PIN e localizzazione GPS antifurto. Manutenzione lame e batteria gestita in officina: spegnimento invernale e rimessa in linea a primavera incluse nel servizio.',
    specs: [
      { label: 'Area massima', value: 'Fino a 4000 m²' },
      { label: 'Larghezza taglio', value: '28 cm' },
      { label: 'Pendenza max', value: '45%' },
      { label: 'Connettività', value: 'iMow App · GPS · Bluetooth' },
      { label: 'Installazione', value: 'Inclusa, dal nostro tecnico' },
      { label: 'Garanzia', value: '2 anni' }
    ],
    highlights: [
      { title: 'GPS antifurto', value: 'Localizzazione e blocco da remoto: il robot diventa inservibile se rubato.' },
      { title: 'Taglio in fasce', value: 'Schema parallelo razionale, niente percorsi casuali sul prato.' },
      { title: 'Service incluso', value: 'Installazione, configurazione cavo perimetrale e tagliando primo anno da noi.' }
    ]
  },
  {
    slug: 'honda-hrx-476',
    brand: 'Honda',
    model: 'HRX 476',
    modelFull: 'Honda HRX 476 VY',
    category: 'Rasaerba semovente a benzina',
    tagline: 'Il rasaerba di chi insegna.',
    lead: 'Scocca in NeXite, motore Honda GCV: dura quanto un’auto, taglia come una lama nuova ogni volta.',
    description: 'Quattro funzioni in una: raccolta in cesto da 70 L, mulching con sistema Versamow regolabile, scarico posteriore, scarico laterale (opzionale). Trazione Select Drive a leva con velocità variabile, comoda anche su pendenze importanti. La scocca in NeXite è leggera e non arrugginisce: non si deforma e non scolora dopo anni di stagioni. Per giardini medio-grandi (oltre 1.200 m²) e chi tiene al risultato a fine taglio.',
    specs: [
      { label: 'Motore', value: 'Honda GCV 170 · 166 cc' },
      { label: 'Larghezza taglio', value: '47 cm' },
      { label: 'Capacità cesto', value: '70 L' },
      { label: 'Trazione', value: 'Variabile · Select Drive' },
      { label: 'Peso', value: '40 kg' },
      { label: 'Garanzia', value: '5 anni (uso privato)' }
    ],
    highlights: [
      { title: 'Scocca NeXite', value: 'Tecnopolimero: non arrugginisce, non si ammacca, garantita 10 anni.' },
      { title: 'Versamow System', value: 'Regola in continuo il rapporto raccolta/mulching con una leva.' },
      { title: 'Select Drive', value: 'Trazione a velocità variabile: si adatta al passo di chi spinge.' }
    ]
  },
  {
    slug: 'honda-hrn',
    brand: 'Honda',
    model: 'HRN 536',
    modelFull: 'Honda HRN 536 C VY',
    category: 'Rasaerba mulching semovente',
    tagline: 'Prato perfetto, senza riempire sacchi.',
    lead: 'Il mulching non è una moda: è il modo in cui l’erba diventa concime mentre la tagli.',
    description: 'Motore GCVx 170 di nuova generazione, più silenzioso ed efficiente del GCV precedente. Larghezza taglio 53 cm e funzioni Clip Director (raccolta, mulching, scarico posteriore). Sistema Roto-Stop che ferma la lama senza spegnere il motore — utile quando bisogna attraversare un viale in ghiaia o spostare un tubo. Telaio in acciaio resistente, leva trazione semovente standard. Pensato per chi vuole velocità di taglio su prati medio-grandi.',
    specs: [
      { label: 'Motore', value: 'Honda GCVx 170 · 167 cc' },
      { label: 'Larghezza taglio', value: '53 cm' },
      { label: 'Roto-Stop', value: 'Sì (frizione lama)' },
      { label: 'Funzioni', value: 'Raccolta · Mulching · Scarico' },
      { label: 'Peso', value: '43 kg' },
      { label: 'Garanzia', value: '5 anni (uso privato)' }
    ],
    highlights: [
      { title: 'Motore GCVx', value: 'Nuova generazione: meno vibrazioni, partenza al primo strappo, consumi ridotti.' },
      { title: 'Roto-Stop', value: 'Frizione che ferma la lama lasciando girare il motore: stop e ripartenza in 1 secondo.' },
      { title: 'Clip Director', value: 'Una leva sceglie tra raccolta, mulching e scarico senza smontare nulla.' }
    ]
  },
  {
    slug: 'honda-eu22i',
    brand: 'Honda',
    model: 'EU22i',
    modelFull: 'Honda EU22i',
    category: 'Generatore inverter portatile',
    tagline: 'Corrente pulita, in silenzio.',
    lead: 'L’inverter più conosciuto al mondo. Alimenta laptop, frigoriferi, utensili, luci da palco. Senza picchi.',
    description: 'Generatore inverter sinusoidale puro da 2200 W di picco e 1800 W continui. Modalità Eco-Throttle che regola i giri del motore in base al carico — meno benzina consumata, meno rumore quando l’assorbimento è basso. Doppia presa schuko + USB. Collegabile in parallelo a un secondo EU22i tramite cavo dedicato per raddoppiare la potenza disponibile. Motore Honda GXR120 4 tempi, scelto da elettricisti, camperisti, organizzatori di eventi all’aperto.',
    specs: [
      { label: 'Potenza max', value: '2200 W' },
      { label: 'Potenza continua', value: '1800 W' },
      { label: 'Motore', value: 'Honda GXR120 · 121 cc' },
      { label: 'Rumore', value: '48 — 57 dB(A)' },
      { label: 'Peso', value: '21 kg' },
      { label: 'Autonomia', value: 'fino a 8 ore (Eco)' },
      { label: 'Garanzia', value: '3 anni privati' }
    ],
    highlights: [
      { title: 'Sinusoide pura', value: 'Onda inverter pulita: alimenta sicuro PC, schede madri, dispositivi medicali.' },
      { title: 'Eco-Throttle', value: 'Il motore segue il carico: consumo dimezzato a basso assorbimento.' },
      { title: 'Parallelo 2x', value: 'Due EU22i in tandem = 3600 W disponibili con un cavo dedicato.' }
    ]
  },
  {
    slug: 'active-4860',
    brand: 'Active',
    model: '4860 SH',
    modelFull: 'Active 4860 SH 4in1',
    category: 'Rasaerba semovente 4 in 1',
    tagline: 'Made in Italy.',
    lead: 'Progettato e assemblato in provincia di Bergamo. Quattro funzioni, una scocca, ruote larghe per i terreni veri.',
    description: 'Motore Briggs & Stratton 750 EXi (161 cc) con starter facilitato e senza primer. Telaio in acciaio verniciato, regolazione altezza centralizzata a 7 posizioni (25-75 mm), manubrio ergonomico ripiegabile a doppia altezza. Quattro funzioni standard: raccolta in cesto 65 L, mulching, scarico posteriore, scarico laterale. Trazione semovente. Per giardini fino a circa 1.500 m², chi cerca un Made in Italy serio e ricambi facili da reperire.',
    specs: [
      { label: 'Motore', value: 'B&S 750 EXi · 161 cc' },
      { label: 'Larghezza taglio', value: '48 cm' },
      { label: 'Funzioni', value: '4 in 1 (raccolta · mulching · scarico post./lat.)' },
      { label: 'Trazione', value: 'Semovente' },
      { label: 'Capacità cesto', value: '65 L' },
      { label: 'Altezza taglio', value: '25 — 75 mm (7 pos.)' },
      { label: 'Garanzia', value: '2 anni' }
    ],
    highlights: [
      { title: '4 funzioni standard', value: 'Mulching e scarico laterale di serie, non optional come su altri.' },
      { title: 'Made in Italy', value: 'Progettato e assemblato in provincia di Bergamo: ricambi sempre reperibili.' },
      { title: 'Motore B&S EXi', value: 'Starter senza primer, parte al primo strappo anche dopo mesi di fermo.' }
    ]
  },
  {
    slug: 'active-mz-cm',
    brand: 'Active',
    model: 'MZ CM',
    modelFull: 'Active MZ CM con Honda GP 160',
    category: 'Motozappa a benzina',
    tagline: 'L’orto preparato in mezza mattina.',
    lead: 'Motore Honda GP 160 — il riferimento per chi vuole sicurezza di partenza anche a marzo, dopo l’inverno fermo.',
    description: 'Motozappa con frese in acciaio temprato e larghezza di lavoro regolabile fino a 80 cm. Trasmissione a bagno d’olio con marcia avanti e retromarcia per uscire dai filari senza dover sollevare la macchina. Stegole regolabili in altezza e lateralmente, per non camminare nel solco appena fatto. Motore Honda GP 160 (163 cc) a 4 tempi a benzina: leggero, affidabile, costo gestione basso. Per orti familiari medi e piccoli appezzamenti.',
    specs: [
      { label: 'Motore', value: 'Honda GP 160 · 163 cc' },
      { label: 'Larghezza lavoro', value: 'fino a 80 cm' },
      { label: 'Profondità', value: 'regolabile via timone' },
      { label: 'Cambio', value: '1 AV + 1 RM' },
      { label: 'Frese', value: 'Acciaio temprato' },
      { label: 'Garanzia', value: '2 anni' }
    ],
    highlights: [
      { title: 'Motore Honda GP 160', value: 'Avviamento sicuro dopo soste lunghe: parte anche a fine inverno.' },
      { title: 'Stegole regolabili', value: 'Altezza e laterale: si lavora fuori dal solco appena dissodato.' },
      { title: 'Retromarcia', value: 'Esce dai filari senza dover sollevare 60 kg di macchina.' }
    ]
  },
  {
    slug: 'cippatore-tritone',
    brand: 'Geotech',
    model: 'Tritone Sprint',
    modelFull: 'Geotech Tritone Sprint',
    category: 'Biotrituratore a benzina',
    tagline: 'I rami in cippato.',
    lead: 'Per chi pota grandi piante e non vuole bruciarle. Cippato pronto per la pacciamatura o la stufa a legna.',
    description: 'Biotrituratore a benzina con motore Briggs & Stratton da 6.5 HP (208 cc), tramoggia ampia con imbuto antinfortunistico e ruote pneumatiche per spostarlo dove serve. Diametro massimo di taglio 75 mm: gestisce rami da potatura di frutteti, siepi alte, arbusti ornamentali. Uscita laterale che proietta il cippato direttamente in un cassone o pila pacciamatura. Ideale per agriturismi, parchi privati, manutentori del verde che vogliono evitare il falò.',
    specs: [
      { label: 'Motore', value: 'B&S 6.5 HP · 208 cc · benzina' },
      { label: 'Diametro max ramo', value: '75 mm' },
      { label: 'Tramoggia', value: 'Ampia con imbuto di sicurezza' },
      { label: 'Ruote', value: 'Pneumatiche' },
      { label: 'Peso', value: '~50 kg' },
      { label: 'Uscita', value: 'Cippato (laterale)' },
      { label: 'Garanzia', value: '2 anni' }
    ],
    highlights: [
      { title: 'Diametro 75 mm', value: 'Trita rami consistenti: copre potature frutteti, siepi alte, arbusti.' },
      { title: 'Ruote pneumatiche', value: 'Si sposta in fondo al frutteto senza scaricarlo dal furgone.' },
      { title: 'Motore B&S', value: '6.5 HP a benzina, partenza affidabile e ricambi facili da reperire.' }
    ]
  },
  {
    slug: 'ligier-myli',
    brand: 'Ligier',
    model: 'Myli',
    modelFull: 'Ligier Myli (L6e)',
    category: 'Microcar elettrica L6e',
    tagline: 'La microcar disegnata.',
    lead: 'Stile francese, ergonomia da auto vera, pannello digitale da 10". Quattro versioni — da quella essenziale a quella full optional.',
    description: 'Microcar elettrica omologata L6e: si guida con la patente AM dai 14 anni. Motore elettrico, cambio automatico, sistema multimediale con Apple CarPlay e Android Auto sul display da 10". Quattro allestimenti, con possibilità di tetto panoramico vetrato, retrocamera e sensori di parcheggio. Batteria al litio con autonomia WMTC fino a 192 km e ricarica da presa schuko domestica. Per ragazzi neopatentati AM, anziani che hanno perso la patente B, professionisti urbani che vogliono parcheggiare ovunque.',
    specs: [
      { label: 'Omologazione', value: 'L6e (quadriciclo leggero)' },
      { label: 'Velocità max', value: '45 km/h' },
      { label: 'Autonomia (WMTC)', value: 'fino a 192 km' },
      { label: 'Posti', value: '2' },
      { label: 'Ricarica', value: 'Presa schuko domestica' },
      { label: 'Età minima', value: '14 anni (patente AM)' },
      { label: 'Garanzia', value: '2 anni' }
    ],
    highlights: [
      { title: 'Display 10"', value: 'Apple CarPlay e Android Auto di serie: navigatore e musica come in auto.' },
      { title: 'Autonomia 192 km', value: 'Tra le più alte della categoria L6e: una settimana di tragitti urbani senza ricaricare.' },
      { title: '4 allestimenti', value: 'Da Myli essenziale a Myli full optional con tetto panoramico vetrato.' }
    ]
  },
  {
    slug: 'weibang-wb-506-scv',
    brand: 'Weibang',
    model: 'WB 506 SCV',
    modelFull: 'Weibang WB 506 SCV',
    category: 'Rasaerba semovente',
    tagline: 'Spinta facile, taglio pulito.',
    lead: 'Rasaerba semovente da 51 cm di taglio, telaio robusto e trasmissione progressiva. Foto del modello in arrivo.',
    description: 'Rasaerba a spinta semovente di fascia professionale, larghezza taglio 51 cm. Pensato per giardini medio-grandi e uso intensivo. Per scheda tecnica completa, prezzo aggiornato e disponibilità, chiamaci o passa in negozio.',
    specs: [
      { label: 'Larghezza taglio', value: '51 cm' },
      { label: 'Trazione', value: 'Semovente' },
      { label: 'Categoria', value: 'Professionale' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' },
      { label: 'Garanzia', value: 'Standard produttore' }
    ],
    highlights: [
      { title: 'Foto in arrivo', value: 'Sto per ricevere le foto del modello dal magazzino — chiamaci per vederlo in negozio.' },
      { title: 'Semovente 51 cm', value: 'Larghezza di taglio adatta a giardini di media estensione.' },
      { title: 'Service interno', value: 'Tutta la manutenzione la facciamo noi in officina, ricambi sempre disponibili.' }
    ]
  },
  {
    slug: 'weibang-wb-506-hcv',
    brand: 'Weibang',
    model: 'WB 506 HCV',
    modelFull: 'Weibang WB 506 HCV',
    category: 'Rasaerba semovente con motore Honda',
    tagline: 'Spinta facile, motore Honda.',
    lead: 'Rasaerba semovente da 51 cm con motore Honda. Foto del modello in arrivo.',
    description: 'Versione con motore a 4 tempi Honda, per giardini medio-grandi e uso frequente. Per scheda tecnica completa, prezzo aggiornato e disponibilità, chiamaci o passa in negozio a Cene (BG).',
    specs: [
      { label: 'Larghezza taglio', value: '51 cm' },
      { label: 'Trazione', value: 'Semovente' },
      { label: 'Motore', value: 'Honda 4 tempi' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' },
      { label: 'Garanzia', value: 'Standard produttore' }
    ],
    highlights: [
      { title: 'Motore Honda', value: 'Affidabilità del 4 tempi Honda con la trasmissione professionale Weibang.' },
      { title: 'Semovente', value: 'Avanzamento autonomo: nessuno sforzo anche su pendenze leggere.' },
      { title: 'Foto in arrivo', value: 'Foto del modello in produzione: scrivici per vederlo in negozio.' }
    ]
  },
  {
    slug: 'weibang-wb-537-scv-bbc',
    brand: 'Weibang',
    model: 'WB 537 SCV BBC',
    modelFull: 'Weibang WB 537 SCV BBC',
    category: 'Rasaerba professionale BBC',
    tagline: 'Il professionale per giardinieri.',
    lead: 'Rasaerba professionale 53 cm con freno lama BBC. Foto del modello in arrivo.',
    description: 'Sistema BBC (Blade Brake Clutch): il motore resta acceso anche quando la lama è ferma, ideale per chi sposta spesso la macchina o svuota il cesto. Pensato per giardinieri professionisti. Per scheda tecnica completa e disponibilità, chiamaci.',
    specs: [
      { label: 'Larghezza taglio', value: '53 cm' },
      { label: 'Trazione', value: 'Semovente' },
      { label: 'Freno lama', value: 'BBC (Blade Brake Clutch)' },
      { label: 'Categoria', value: 'Professionale' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' }
    ],
    highlights: [
      { title: 'Freno lama BBC', value: 'Ferma la lama senza spegnere il motore: stop e ripartenza istantanea.' },
      { title: '53 cm taglio', value: 'Larghezza ideale per uso quotidiano da giardiniere.' },
      { title: 'Foto in arrivo', value: 'Stiamo aspettando le foto del modello: chiama per vederlo in negozio.' }
    ]
  },
  {
    slug: 'weibang-wb-656-slcv-bbc',
    brand: 'Weibang',
    model: 'WB 656 SLCV BBC',
    modelFull: 'Weibang WB 656 SLCV BBC',
    category: 'Rasaerba professionale BBC 65 cm',
    tagline: 'Il top di gamma a spinta.',
    lead: 'Rasaerba professionale 65 cm con freno lama BBC. Foto del modello in arrivo.',
    description: 'Larghezza di taglio 65 cm per coprire più superficie con meno passate. Sistema BBC (Blade Brake Clutch) per sicurezza in uso intensivo. Per scheda tecnica completa e disponibilità, chiamaci.',
    specs: [
      { label: 'Larghezza taglio', value: '65 cm' },
      { label: 'Trazione', value: 'Semovente' },
      { label: 'Freno lama', value: 'BBC (Blade Brake Clutch)' },
      { label: 'Categoria', value: 'Professionale' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' }
    ],
    highlights: [
      { title: '65 cm taglio', value: 'Più superficie per ogni passata: meno tempo a tagliare grandi giardini.' },
      { title: 'Freno lama BBC', value: 'Sicurezza professionale: la lama si ferma in pochi secondi.' },
      { title: 'Foto in arrivo', value: 'Foto in produzione — vieni in negozio o chiama per vederlo dal vivo.' }
    ]
  },
  {
    slug: 'weibang-p40-bull',
    brand: 'Weibang',
    model: 'P40 BULL',
    modelFull: 'Weibang P40 BULL',
    category: 'Rasaerba a batteria professionale',
    tagline: 'Silenzioso, zero emissioni.',
    lead: 'Rasaerba professionale a batteria. Foto del modello in arrivo.',
    description: 'Tagliaerba elettrico a batteria, silenzioso e senza emissioni. Per modello, autonomia e accessori disponibili, chiamaci o passa in negozio.',
    specs: [
      { label: 'Alimentazione', value: 'Batteria' },
      { label: 'Categoria', value: 'Professionale silenzioso' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' },
      { label: 'Garanzia', value: 'Standard produttore' },
      { label: 'Vantaggio', value: 'Zero emissioni, basso rumore' }
    ],
    highlights: [
      { title: 'Zero emissioni', value: 'Niente benzina, niente fumi: ottimo in giardini residenziali e parchi.' },
      { title: 'Silenzioso', value: 'Tagli all\'alba o al tramonto senza disturbare il vicinato.' },
      { title: 'Foto in arrivo', value: 'Foto del modello in arrivo: scrivici per vederlo in negozio.' }
    ]
  },
  {
    slug: 'weibang-wb-1100-pro',
    brand: 'Weibang',
    model: 'WB 1100 PRO',
    modelFull: 'Weibang WB 1100 PRO',
    category: 'Trattorino tagliaerba',
    tagline: 'Trattorino comodo per il tuo giardino.',
    lead: 'Trattorino tagliaerba Weibang serie 1100. Foto del modello in arrivo.',
    description: 'Trattorino tagliaerba per giardini medio-grandi. Per cilindrata, larghezza di taglio e disponibilità, chiamaci o passa in negozio a Cene (BG).',
    specs: [
      { label: 'Tipologia', value: 'Trattorino tagliaerba' },
      { label: 'Categoria', value: 'Hobby / semi-pro' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' },
      { label: 'Garanzia', value: 'Standard produttore' },
      { label: 'Consegna', value: 'Su appuntamento' }
    ],
    highlights: [
      { title: 'Trattorino comodo', value: 'Per chi non vuole più spingere: si guida seduti, in scioltezza.' },
      { title: 'Per giardini medi', value: 'Pensato per superfici da circa 1.500-3.000 m² con taglio frequente.' },
      { title: 'Foto in arrivo', value: 'Foto del modello in arrivo dal magazzino — chiamaci per vederlo dal vivo.' }
    ]
  },
  {
    slug: 'weibang-wb-456-scv',
    brand: 'Weibang',
    model: 'WB 456 SCV',
    modelFull: 'Weibang WB 456 SCV',
    category: 'Rasaerba semovente compatto',
    tagline: 'Compatto, agile, semovente.',
    lead: 'Rasaerba semovente compatto da 46 cm. Foto del modello in arrivo.',
    description: 'Versione compatta da 46 cm di taglio, ideale per giardini fino a 800 m². Trasmissione semovente, leggero e maneggevole. Per scheda tecnica e disponibilità, chiamaci o passa in negozio.',
    specs: [
      { label: 'Larghezza taglio', value: '46 cm' },
      { label: 'Trazione', value: 'Semovente' },
      { label: 'Categoria', value: 'Hobby evoluto' },
      { label: 'Area consigliata', value: 'Fino a 800 m²' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' }
    ],
    highlights: [
      { title: '46 cm taglio', value: 'Compatto: passa nei viali stretti e tra le siepi.' },
      { title: 'Semovente', value: 'Avanzamento autonomo: nessuno sforzo anche su salite leggere.' },
      { title: 'Foto in arrivo', value: 'Foto in produzione — vieni in negozio o chiama per vederlo dal vivo.' }
    ]
  },
  {
    slug: 'weibang-wb-537-scv',
    brand: 'Weibang',
    model: 'WB 537 SCV',
    modelFull: 'Weibang WB 537 SCV',
    category: 'Rasaerba semovente',
    tagline: 'Il semovente serio, senza fronzoli.',
    lead: 'Rasaerba semovente 53 cm versione standard. Foto del modello in arrivo.',
    description: 'Versione standard della famiglia 537 (senza freno lama BBC), pensata per chi cerca un semovente serio senza il sovrapprezzo del sistema professionale. Per disponibilità e prezzo, chiamaci.',
    specs: [
      { label: 'Larghezza taglio', value: '53 cm' },
      { label: 'Trazione', value: 'Semovente' },
      { label: 'Categoria', value: 'Semi-pro' },
      { label: 'Area consigliata', value: '1000 - 2000 m²' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' }
    ],
    highlights: [
      { title: '53 cm di taglio', value: 'Larghezza generosa: meno passate sullo stesso prato.' },
      { title: 'Senza BBC, prezzo onesto', value: 'Per chi non ferma e riparte tutto il giorno, il BBC non serve.' },
      { title: 'Foto in arrivo', value: 'Foto del modello in arrivo: scrivici per vederlo in negozio.' }
    ]
  },
  {
    slug: 'weibang-wb-506-sc',
    brand: 'Weibang',
    model: 'WB 506 SC',
    modelFull: 'Weibang WB 506 SC',
    category: 'Rasaerba a spinta',
    tagline: 'Il classico a spinta, fatto bene.',
    lead: 'Rasaerba a spinta 51 cm versione economica. Foto del modello in arrivo.',
    description: 'Versione a spinta (non semovente) del WB 506, indicata per giardini piccoli e medi e per chi preferisce avere controllo manuale del ritmo di taglio. Per disponibilità, chiamaci.',
    specs: [
      { label: 'Larghezza taglio', value: '51 cm' },
      { label: 'Trazione', value: 'Spinta manuale' },
      { label: 'Categoria', value: 'Hobby' },
      { label: 'Area consigliata', value: 'Fino a 1000 m²' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' }
    ],
    highlights: [
      { title: 'A spinta', value: 'Il taglio lo decidi tu: ritmo manuale, niente parti meccaniche in più.' },
      { title: 'Economico e robusto', value: 'Meno componenti = meno guasti, manutenzione semplificata.' },
      { title: 'Foto in arrivo', value: 'Foto del modello in arrivo dal magazzino — chiamaci per vederlo dal vivo.' }
    ]
  },
  {
    slug: 'weibang-wb-484-sbv-pro',
    brand: 'Weibang',
    model: 'WB 484 SBV PRO',
    modelFull: 'Weibang WB 484 SBV PRO',
    category: 'Rasaerba professionale',
    tagline: 'Telaio in acciaio, lavoro continuo.',
    lead: 'Rasaerba professionale 48 cm con telaio in acciaio. Foto del modello in arrivo.',
    description: 'Telaio in acciaio rinforzato e trasmissione professionale, pensato per giardinieri che cercano un 48 cm capace di lavorare ore senza scaldarsi. Per scheda completa e disponibilità, chiamaci.',
    specs: [
      { label: 'Larghezza taglio', value: '48 cm' },
      { label: 'Telaio', value: 'Acciaio rinforzato' },
      { label: 'Trazione', value: 'Semovente variabile' },
      { label: 'Categoria', value: 'Professionale' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' }
    ],
    highlights: [
      { title: 'Telaio in acciaio', value: 'Resistente agli urti accidentali e al calore del motore in uso intensivo.' },
      { title: 'Trazione variabile', value: 'Velocità di avanzamento adattabile al passo del giardiniere.' },
      { title: 'Foto in arrivo', value: 'Foto del modello in arrivo: passa in negozio per vederlo.' }
    ]
  },
  {
    slug: 'weibang-wb-384-rb',
    brand: 'Weibang',
    model: 'WB 384 RB',
    modelFull: 'Weibang WB 384 RB',
    category: 'Robot tagliaerba',
    tagline: 'Il prato si fa da solo.',
    lead: 'Robot tagliaerba Weibang con perimetrale. Foto del modello in arrivo.',
    description: 'Robot tagliaerba con perimetrale, programmazione automatica e ritorno in base. Per area massima coperta, autonomia e disponibilità, chiamaci o passa in negozio.',
    specs: [
      { label: 'Tipologia', value: 'Robot tagliaerba' },
      { label: 'Alimentazione', value: 'Batteria + base ricarica' },
      { label: 'Installazione', value: 'Inclusa, dal nostro tecnico' },
      { label: 'Disponibilità', value: 'Chiamaci per info' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' },
      { label: 'Garanzia', value: 'Standard produttore' }
    ],
    highlights: [
      { title: 'Programmazione automatica', value: 'Decide quando tagliare in base al programma che imposti.' },
      { title: 'Installazione inclusa', value: 'Posa cavo perimetrale e prima configurazione da noi.' },
      { title: 'Foto in arrivo', value: 'Foto del modello in arrivo — chiamaci per vederlo dal vivo.' }
    ]
  }
];
