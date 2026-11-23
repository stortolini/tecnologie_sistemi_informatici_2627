def main() -> None:
    json_testo = '{"nome": "Mario", "descrizione": "' + "bla " * 50 + '", "eta": 17}'

    # cercare "eta" nel JSON
    passi = 0
    for i in range(len(json_testo)):
        passi += 1
        if json_testo[i:i+5] == '"eta"':
            print("Trovato! Ho letto", passi, "caratteri")
            break

    # BSON
    bson_finto = [
        ("nome", 5, "Mario"),
        ("descrizione", 200, "bla " * 50),
        ("eta", 2, 17)
    ]

    passi = 0
    for nome, lunghezza, valore in bson_finto:
        passi += 1
        if nome == "eta":
            print("Trovato! Valore =", valore, "- passi fatti:", passi)
            break
        print("Non è", nome, "-> salto", lunghezza, "caratteri in un colpo")



if __name__ == "__main__":
    """
    Piccolo script per capire il funzionamento della ricerca di un campo: "eta" 
    in JSON e BSON fittizi.
    """
    main()
