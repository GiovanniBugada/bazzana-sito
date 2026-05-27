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
    slug: 'weibang-wb-506-sc',
    brand: 'Weibang',
    model: 'WB 506 SC',
    modelFull: 'Weibang WB 506 SC',
    category: 'Rasaerba semovente Home Series',
    tagline: 'Semovente Home, motore Loncin.',
    lead: 'Tagliaerba semovente da 50 cm con motore Loncin 159 cc, ideale per superfici fino a 1.000 mq.',
    description: 'Rasaerba a scoppio semovente della serie Home, motore Loncin 1P65FE-2 da 159 cc 6 HP a 4 tempi. Scocca in acciaio con triplo strato di vernice Komaxit anti-corrosione, ruote 8 e 9 pollici. Funzione mulching incluso. Per prezzo aggiornato e disponibilita, chiamaci o passa in negozio.',
    specs: [
      { label: 'Larghezza taglio', value: '50 cm' },
      { label: 'Motore', value: 'Loncin 1P65FE-2 · 159 cc · 6 HP' },
      { label: 'Trazione', value: 'Semovente · 1 velocita' },
      { label: 'Altezza taglio', value: '20-70 mm (8 posizioni)' },
      { label: 'Capacita cesto', value: '60 L' },
      { label: 'Peso', value: '40,3 kg' },
      { label: 'Superficie consigliata', value: 'Fino a 1.000 mq' },
      { label: 'Funzioni', value: 'Raccolta · Mulching' }
    ],
    highlights: [
      { title: 'Motore Loncin 159 cc', value: 'Motore 4T affidabile da 6 HP, partenza facile e ricambi reperibili.' },
      { title: 'Scocca Komaxit', value: 'Triplo strato di vernice anti-corrosione: dura nel tempo anche con umidita.' },
      { title: 'Smart positioning', value: 'Si inclina sulla parte posteriore per pulizia lama in sicurezza.' }
    ]
  },
  {
    slug: 'weibang-wb-506-sc3',
    brand: 'Weibang',
    model: 'WB 506 SC3',
    modelFull: 'Weibang WB 506 SC3',
    category: 'Rasaerba semovente Home 3in1',
    tagline: 'Semovente 3in1, tre modi di tagliare.',
    lead: 'Tagliaerba 50 cm semovente 3in1: raccolta, mulching, scarico laterale. Motore Loncin 159 cc.',
    description: 'Versione 3in1 (raccolta + mulching + scarico laterale) del WB506SC, motore Loncin 1P65FE-2 da 159 cc 6 HP, coppia 8,9 Nm. Scocca acciaio Komaxit, 8 livelli di taglio. Ideale per giardini 400-1.000 mq.',
    specs: [
      { label: 'Larghezza taglio', value: '50 cm' },
      { label: 'Motore', value: 'Loncin 1P65FE-2 · 159 cc · 6 HP · 8,9 Nm' },
      { label: 'Trazione', value: 'Semovente · 1 velocita' },
      { label: 'Altezza taglio', value: '20-70 mm (8 posizioni)' },
      { label: 'Capacita cesto', value: '60 L' },
      { label: 'Peso', value: '41,3 kg' },
      { label: 'Superficie consigliata', value: '400 - 1.000 mq' },
      { label: 'Funzioni', value: '3in1: Raccolta · Mulching · Scarico laterale' }
    ],
    highlights: [
      { title: '3in1 reale', value: 'Raccolta + mulching + scarico laterale: scegli la modalita senza smontare nulla.' },
      { title: 'Motore Loncin 159 cc', value: '4 tempi, 8,9 Nm coppia: tiene anche in erba alta e umida.' },
      { title: 'Per giardini 400-1000 mq', value: 'Dimensione ideale per la villa con giardino strutturato.' }
    ]
  },
  {
    slug: 'weibang-wb-537-sc3',
    brand: 'Weibang',
    model: 'WB 537 SC3',
    modelFull: 'Weibang WB 537 SC3',
    category: 'Rasaerba semovente Home 53 cm 3in1',
    tagline: 'Motore Weibang 196 cc, 53 cm.',
    lead: 'Tagliaerba semovente 53 cm 3in1, motore Weibang 196 cc 7 HP, per giardini 1.000-3.000 mq.',
    description: 'Step superiore rispetto al WB506SC3, larghezza taglio 53 cm e motore proprietario Weibang 1P70FC da 196 cc 7 HP con coppia 10,9 Nm. Distribuzione OHV, regolazione aria automatica, bobina elettronica per avviamento facilitato.',
    specs: [
      { label: 'Larghezza taglio', value: '53 cm' },
      { label: 'Motore', value: 'Weibang 1P70FC · 196 cc · 7 HP · 10,9 Nm' },
      { label: 'Trazione', value: 'Semovente' },
      { label: 'Altezza taglio', value: '20-85 mm (6 posizioni)' },
      { label: 'Funzioni', value: '3in1: Raccolta · Mulching · Scarico laterale' },
      { label: 'Superficie consigliata', value: '1.000 - 3.000 mq' },
      { label: 'Avviamento', value: 'A strappo, regolazione aria automatica' },
      { label: 'Serbatoio', value: '1,7 L benzina' }
    ],
    highlights: [
      { title: 'Motore Weibang 196 cc', value: 'Proprietario OHV, 10,9 Nm di coppia, raffreddamento ad aria: progettato per durare.' },
      { title: 'Avviamento facilitato', value: 'Bobina elettronica + regolazione aria automatica: parte sempre.' },
      { title: '53 cm di taglio', value: 'Larghezza generosa per giardini fino a 3.000 mq con meno passate.' }
    ]
  },
  {
    slug: 'weibang-wb-456-scve3',
    brand: 'Weibang',
    model: 'WB 456 SCVE3',
    modelFull: 'Weibang WB 456 SCVE3',
    category: 'Rasaerba semovente Home 46 cm 3in1',
    tagline: 'Compatto, agile, 3in1.',
    lead: 'Tagliaerba compatto 46 cm semovente 3in1 della Home Series Weibang.',
    description: 'Versione compatta della Home Series, 46 cm di taglio per giardini medio-piccoli. Sistema 3in1 (raccolta, mulching, scarico laterale). Per cilindrata, peso e prezzo aggiornati, chiamaci.',
    specs: [
      { label: 'Larghezza taglio', value: '46 cm' },
      { label: 'Trazione', value: 'Semovente' },
      { label: 'Funzioni', value: '3in1: Raccolta · Mulching · Scarico laterale' },
      { label: 'Serie', value: 'Home Series' },
      { label: 'Categoria', value: 'Hobby evoluto' },
      { label: 'Disponibilita', value: 'Chiamaci per scheda completa' },
      { label: 'Assistenza', value: 'Officina interna Bazzana' }
    ],
    highlights: [
      { title: '46 cm compatto', value: 'Passa nei viali stretti e tra le siepi: maneggevole anche per chi taglia da poco.' },
      { title: '3in1 di serie', value: 'Raccolta, mulching e scarico laterale: scegli ogni volta come trattare l erba.' },
      { title: 'Home Series', value: 'Pensato per uso domestico settimanale: robusto ma facile da gestire.' }
    ]
  },
  {
    slug: 'weibang-wb-466-scm',
    brand: 'Weibang',
    model: 'WB 466 SCM',
    modelFull: 'Weibang WB 466 SCM',
    category: 'Rasaerba mulching a spinta',
    tagline: 'Mulching puro, niente sacchi da svuotare.',
    lead: 'Tagliaerba 46 cm a spinta dedicato al mulching: erba sminuzzata e ridistribuita come concime naturale.',
    description: 'Rasaerba a spinta della Home Series, motore a benzina ~166 cc, scocca in acciaio con trattamento anti-corrosione e regolazione centralizzata altezza. Funzione mulching dedicata: tritura finemente l erba per ridistribuirla come nutrimento naturale del prato.',
    specs: [
      { label: 'Larghezza taglio', value: '46 cm' },
      { label: 'Motore', value: 'Benzina 4T · ~166 cc' },
      { label: 'Trazione', value: 'Spinta manuale' },
      { label: 'Funzione', value: 'Mulching dedicato' },
      { label: 'Scocca', value: 'Acciaio anti-corrosione' },
      { label: 'Superficie consigliata', value: '400 - 1.000 mq' },
      { label: 'Vantaggio', value: 'Niente raccolta sacchi: l erba diventa concime' }
    ],
    highlights: [
      { title: 'Mulching dedicato', value: 'Lama e scocca progettate solo per mulching: l erba esce trinciatissima.' },
      { title: 'A spinta', value: 'Il taglio lo gestisci tu: ritmo manuale, niente parti di trazione che possono guastarsi.' },
      { title: 'Concime naturale', value: 'L erba sminuzzata nutre il prato: meno acqua, meno fertilizzante, prato piu sano.' }
    ]
  },
  {
    slug: 'weibang-wb-537-scval',
    brand: 'Weibang',
    model: 'WB 537 SCVAL',
    modelFull: 'Weibang WB 537 SCVAL',
    category: 'Rasaerba professionale alluminio 53 cm',
    tagline: 'Alluminio, cardano, 3 marce.',
    lead: 'Tagliaerba professionale 53 cm in alluminio, trasmissione cardanica a 3 velocita.',
    description: 'Della Professional Series Weibang. Scocca in alluminio (piu leggera, non arrugginisce, dura nel tempo). Trasmissione cardanica con 3 velocita selezionabili. Per peso e dotazioni specifiche, chiamaci.',
    specs: [
      { label: 'Larghezza taglio', value: '53 cm' },
      { label: 'Scocca', value: 'Alluminio' },
      { label: 'Trasmissione', value: 'Cardanica · 3 velocita' },
      { label: 'Serie', value: 'Professional Series' },
      { label: 'Categoria', value: 'Professionale' },
      { label: 'Vantaggio', value: 'Niente ruggine, durata superiore' },
      { label: 'Disponibilita', value: 'Chiamaci per scheda completa' }
    ],
    highlights: [
      { title: 'Scocca in alluminio', value: 'Piu leggera del cugino in acciaio, immune alla ruggine: investimento a lungo termine.' },
      { title: 'Cardano 3 velocita', value: 'Trasmissione meccanica robusta: adatta velocita di avanzamento al tipo di prato.' },
      { title: 'Professional Series', value: 'Pensato per giardinieri che lavorano ore al giorno: scocca + trasmissione progettate per durare.' }
    ]
  },
  {
    slug: 'weibang-wb-537-scvalb',
    brand: 'Weibang',
    model: 'WB 537 SCVALB',
    modelFull: 'Weibang WB 537 SCVALB',
    category: 'Professionale alluminio con freno lama',
    tagline: 'Alluminio + freno lama: il top a spinta.',
    lead: 'Tagliaerba professionale 53 cm in alluminio con frizione freno lama (BBC). 70 L cesto, 196 cc, 65 kg.',
    description: 'Top di gamma della Professional Series con frizione freno lama (BBC): il motore resta in moto anche quando la lama e ferma, ideale per spostamenti e svuotamento cesto frequente. Scocca alluminio + trasmissione cardanica 3 velocita + mulching.',
    specs: [
      { label: 'Larghezza taglio', value: '53 cm' },
      { label: 'Motore', value: 'Weibang · 196 cc' },
      { label: 'Scocca', value: 'Alluminio' },
      { label: 'Trasmissione', value: 'Cardanica · 3 velocita' },
      { label: 'Freno lama', value: 'BBC (frizione freno lama)' },
      { label: 'Altezza taglio', value: '25-76 mm (7 posizioni)' },
      { label: 'Capacita cesto', value: '70 L' },
      { label: 'Peso', value: '65 kg' },
      { label: 'Mulching', value: 'Si' },
      { label: 'Superficie consigliata', value: '1.000 - 3.000 mq' }
    ],
    highlights: [
      { title: 'Freno lama BBC', value: 'Motore acceso, lama ferma: stop e ripartenza in pochi secondi.' },
      { title: 'Alluminio + cardano', value: 'Combo top per durata e affidabilita: scocca senza ruggine + trasmissione meccanica robusta.' },
      { title: 'Cesto 70 L', value: 'Capacita superiore alla media: meno svuotamenti in giornate intense.' }
    ]
  },
  {
    slug: 'weibang-wb-537-scvm',
    brand: 'Weibang',
    model: 'WB 537 SCVM',
    modelFull: 'Weibang WB 537 SCVM',
    category: 'Professionale mulching 53 cm',
    tagline: 'Mulching pro: l erba diventa concime.',
    lead: 'Tagliaerba professionale Weibang 53 cm dedicato al mulching, Professional Series.',
    description: 'Versione mulching-dedicated della Professional Series 537, pensata per chi vuole solo la funzione mulching senza il cesto di raccolta. Restituisce alla terra l erba come fertilizzante naturale, riducendo rifiuti e tempi di lavoro.',
    specs: [
      { label: 'Larghezza taglio', value: '53 cm' },
      { label: 'Serie', value: 'Professional Series' },
      { label: 'Funzione', value: 'Mulching dedicato (no raccolta)' },
      { label: 'Trasmissione', value: 'Semovente' },
      { label: 'Categoria', value: 'Professionale' },
      { label: 'Disponibilita', value: 'Chiamaci per scheda completa' },
      { label: 'Vantaggio', value: 'Concime naturale, zero svuotamenti' }
    ],
    highlights: [
      { title: 'Mulching dedicato', value: 'Solo mulching, niente raccolta: lama specifica + scocca chiusa per tritura ottimale.' },
      { title: 'Zero svuotamenti', value: 'Niente cesto da gestire: lavori ore senza interruzioni.' },
      { title: 'Concime naturale', value: 'L erba ridistribuita nutre il prato: tagli piu frequenti, prato piu sano.' }
    ]
  },
  {
    slug: 'weibang-wb-778-scv3',
    brand: 'Weibang',
    model: 'WB 778 SCV3',
    modelFull: 'Weibang WB 778 SCV3',
    category: 'Bilama professionale 77 cm 3in1',
    tagline: 'Bilama 77 cm, 3 velocita, 300 cc.',
    lead: 'Tagliaerba bilama 77 cm con motore 300 cc, trasmissione meccanica 3 velocita. Pulisce fino a 3.000 mq.',
    description: 'Top assoluto della Professional Series Weibang: due lame di forma diversa per coprire 77 cm in una sola passata. Motore 300 cc, trasmissione meccanica a 3 velocita, mulching incluso, sacco da 90 L. Pensato per giardinieri professionisti su grandi superfici.',
    specs: [
      { label: 'Larghezza taglio', value: '77 cm (bilama)' },
      { label: 'Motore', value: '300 cc' },
      { label: 'Trasmissione', value: 'Meccanica · 3 velocita' },
      { label: 'Mulching', value: 'Si' },
      { label: 'Capacita cesto', value: '90 L' },
      { label: 'Peso', value: '97 kg' },
      { label: 'Altezza taglio', value: '15-129 mm (regolabile)' },
      { label: 'Superficie', value: 'Fino a 3.000 mq' },
      { label: 'Funzioni', value: '3in1: Raccolta · Mulching · Scarico' }
    ],
    highlights: [
      { title: 'Bilama 77 cm', value: 'Due lame di forma diversa: copertura record, taglio uniforme anche su terreni difficili.' },
      { title: 'Motore 300 cc', value: 'Cilindrata adeguata alla larghezza: tiene il giro anche su erba alta e umida.' },
      { title: '90 L cesto', value: 'Capacita XXL: meno svuotamenti, piu ore di lavoro continuativo.' }
    ]
  },
  {
    slug: 'weibang-wb-452-he',
    brand: 'Weibang',
    model: 'WB 452 HE',
    modelFull: 'Weibang WB 452 HE',
    category: 'Rasaerba a batteria 120V',
    tagline: 'Elettrico 120V, silenzioso, zero emissioni.',
    lead: 'Tagliaerba a batteria 45 cm, sistema 120V 4Ah, sacco 50 L, peso 34,2 kg.',
    description: 'Rasaerba elettrico a batteria Litio Li-Ion 120V/4Ah, larghezza taglio 45 cm. Silenzioso, zero emissioni, ideale per giardini residenziali fino a 400 mq. Altezza di taglio regolabile in 8 posizioni. Batteria e caricatore originali Weibang inclusi.',
    specs: [
      { label: 'Larghezza taglio', value: '45 cm' },
      { label: 'Alimentazione', value: 'Batteria Litio Li-Ion 120V · 4 Ah' },
      { label: 'Altezza taglio', value: '20-70 mm (8 posizioni)' },
      { label: 'Capacita cesto', value: '50 L' },
      { label: 'Peso', value: '34,2 kg' },
      { label: 'Superficie consigliata', value: 'Fino a 400 mq' },
      { label: 'Trazione', value: 'Spinta manuale' },
      { label: 'Inclusi', value: 'Batteria 120V/4Ah + caricatore rapido' }
    ],
    highlights: [
      { title: '120V Li-Ion', value: 'Voltaggio alto: coppia adeguata anche su erba folta, senza i limiti dei 36V/40V.' },
      { title: 'Zero rumore, zero fumi', value: 'Perfetto per giardini residenziali: tagli all alba senza disturbare nessuno.' },
      { title: 'Leggero 34 kg', value: 'Si solleva, si trasporta, si appoggia: ideale per donne, anziani, terrazze con scale.' }
    ]
  },
  {
    slug: 'weibang-wb-462-sem',
    brand: 'Weibang',
    model: 'WB 462 SEM',
    modelFull: 'Weibang WB 462 SEM',
    category: 'Rasaerba a batteria semovente 120V',
    tagline: 'Semovente a batteria, fino a 1.100 mq.',
    lead: 'Tagliaerba semovente a batteria 46 cm, 120V 4Ah, trazione posteriore. Fino a 1.100 mq.',
    description: 'Versione semovente del sistema batteria Weibang 120V: trazione posteriore, larghezza 46 cm, mulching dedicato (senza cesto di raccolta). Autonomia variabile da 367 a 1.100 mq in base alle condizioni d uso.',
    specs: [
      { label: 'Larghezza taglio', value: '46 cm' },
      { label: 'Alimentazione', value: 'Batteria 120V · 4 Ah' },
      { label: 'Trazione', value: 'Semovente · ruote posteriori' },
      { label: 'Altezza taglio', value: '18-65 mm (7 posizioni)' },
      { label: 'Funzione', value: 'Mulching dedicato (no raccolta)' },
      { label: 'Peso', value: '39,8 kg' },
      { label: 'Superficie', value: '367 - 1.100 mq' },
      { label: 'Inclusi', value: 'Batteria + caricatore Weibang' }
    ],
    highlights: [
      { title: 'Semovente elettrico', value: 'Trazione posteriore + batteria 120V: avanzamento autonomo senza inquinare.' },
      { title: '1.100 mq su singola carica', value: 'Top di gamma per autonomia: copre giardini medi senza ricarica intermedia.' },
      { title: 'Mulching automatico', value: 'Niente cesto da svuotare: l erba ridistribuita nutre il prato naturalmente.' }
    ]
  }
];
