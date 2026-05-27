/* =========================================================
   FOTO ROTATIONS — override manuale per foto ruotate.
   Mappa: indice (1-based, come foto-NNN.jpg) -> gradi di rotazione.
   Valori validi: 90, 180, 270 (in senso orario).

   COME AGGIUNGERE UNA FOTO RUOTATA:
   1. Apri la galleria, individua la foto sbagliata (numero in basso a dx)
   2. Aggiungi qui: 42: 90  (per ruotare la foto 042 di 90° in senso orario)
   3. Salva il file e ricarica la pagina

   Questo file viene caricato da foto.html PRIMA di foto-gallery.js.
   ========================================================= */
window.BAZZANA_FOTO_ROTATIONS = {
  // 42: 90,
  // 73: 180,
  // 95: 270,
};
