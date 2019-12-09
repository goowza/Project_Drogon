def tableEmetteur(type):
    if type=="voiture":
        return 0
    elif type=="pieton":
        return 1
    elif type=="borne":
        return 2
    elif type=="urgence":
        return 3
    else:
        return 'z'

def tableEvenement(type):
    if type=="accident":
        return 0
    elif type=="embouteillage":
        return 1
    elif type=="localisation":
        return 2
    else:
        return 'z'

def encodage(idEmetteur, idEvenement, data):
    message = str(tableEmetteur(idEmetteur))+str(tableEvenement(idEvenement))+str(data)
    return message
