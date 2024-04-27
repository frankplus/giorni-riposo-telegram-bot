import lib

constraints = "I dipendenti del ristorante sono: Lu, Cri, Ayi, Ferdaus, Islam, Saiful, Ashraful, JD, Hosen, Gelo. I giorni disponibili per il riposo sono: Lunedì, Martedì, Giovedì. Ogni giorno, un massimo di 4 persone può riposare. Alcune coppie di dipendenti devono riposare lo stesso giorno: Ferdaus e Saiful. Altre coppie non devono riposare lo stesso giorno: Lu e Cri, Cri e Ayi, Ferdaus e Islam, Lu e Islam, JD e Gelo. Preferenze di giorni fissi: nessuna."

print("\n\nresult: \n\n" + str(lib.set_new_constraints_data_from_text(constraints)))

print(lib.describe_scheduling_constraints())

print(lib.generate_weekly_schedule())
