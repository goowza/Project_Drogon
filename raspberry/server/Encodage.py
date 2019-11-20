def tableEmetteur(type):
    if type=="voiture":
        return 0
    elif type=="pieton":
        return 1
    elif type=="borne":
        return 2
    else:
        return 'Z'

def tableEvenement(type):
    if type=="accident":
        return 0
    elif type=="embouteillage":
        return 1
    else:
        return 'Z'

def encodage(idEmetteur, idEvenement, data):
    message = str(tableEmetteur(idEmetteur))+str(tableEvenement(idEvenement))+str(data)
    return message

print(encodage("pieton","accident","105.85.45"))