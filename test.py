import lib

constraints = "I dipendenti del ristorante sono: Lu, Coli, Cri, Ferdaus, Islam, Saiful, Ashraful, JD, Hosen. I giorni disponibili per il riposo sono: Lunedì, Martedì, Mercoledì, Giovedì. Ogni giorno, un massimo di 3 persone può riposare. Alcune coppie di dipendenti devono riposare lo stesso giorno: Ferdaus e Saiful. Altre coppie non devono riposare lo stesso giorno: Lu e Cri, Cri e Ayi, Ferdaus e Islam, Lu e Islam."

print("\n\nresult: \n\n" + str(lib.process_constraints_to_object(constraints)))
