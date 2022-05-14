import Evaporation
import WaterInSoil
import WaterNeededForGrapes
from datetime import datetime

# -------------- ANALYSE ALL DATA AND MANAGE VALVE (ON - OFF) WITH AI -----------------

def manageValve(altidud, phi, soilType, soilHumidity, soilTemperature, airHumidity, airTemperature, rain, windSpeed, fieldArea):

    # ----- STEP 1: Get the actual water volume present in the soil ---
    # How ? depending on the soil type (1, 2 or 3)
    # soilType = 1  => Drainant (sableux/caillouteux)
    # soilType = 2  =>  Equilibré
    # soilType = 3  =>  Argileux (peu drainant)
    # Regression algorithm with data from our experience
    # L'algorithm analyse les données et permet de prédire le niveau d'eau (en mm) présent dans le sol
    # selon les conditions actuelles mesurées (humidité, tempéreture, type de sol, lumiunosité, vitesse du vent) envoyées en paramètre

    waterInSoil = WaterInSoil.getMillemetersOfWaterInSoil(soilType, soilHumidity, soilTemperature) # en mm (hauteur)


    # ----- STEP 2: Get the water need of the plant (Grape) for today -----
    # How ? depending on the annual Grape needs (data from the scientific paper)
    # Regression algorithm
    # L'algorithm analyse les données et permet de prédire les besoin de la Vigne selon le jour de l'année
    first_jan = datetime(datetime.today().year, 1, 1)
    jour = (datetime.today() - first_jan).days + 1  # day in the year (1,366)
    waterNeeded = WaterNeededForGrapes.getMillimetersOfWaterNeeded(jour)


    # ----- STEP 3: Get the water Evaporation -----
    # for a given location
    evaporation = Evaporation.getMillimetersOfEvaporation(airTemperature, altidud, jour, airHumidity, phi, windSpeed)


    # ----- STEP 4: Calculate the water volume required -----
    # en mm de hauteur

    print('\nWaterNeeded =', waterNeeded, 'mm   WaterInSoil =', waterInSoil,
          'mm   Evaporation =', evaporation, 'mm')
    waterRequired = waterNeeded - waterInSoil + evaporation
    print('WaterRequired = ', waterRequired, 'mm\n')



    # ----- STEP 5: ON or OFF Valve -----
    # S'il y a un volume d'eau requis, et la probabilité de pleuvoir est faible => ON
    # ou si la terre est trop seche, un seuil d'humidité dépassée, on arrose peut importe la météo.
    # sinon on arrose pas.

    # Humidity Treshholds
    H_treshhold = 0.4

    # --- System flow (1L = 1mm de hauteur/m2) ---
    # exemples de debit:
    # 1 hectar de vigne 8000L/h (4000 gouteur à 2L/h)
    # goute a goute jardin 3L/h
    fieldArea = fieldArea  # en m2
    nbGoutteur = fieldArea/2.5  # un goutteur couvre 2,5m2
    debitGoutteur = 2  # 2Litre/h   ou   2mm/m2/h
    hauteurDeauGoutteur = debitGoutteur/2.5   # mm/h
    debitTotal = debitGoutteur*nbGoutteur
    hauteurTotal = debitTotal/fieldArea   # mm/h sur la totalité du terrain

    print('Le dispositif d\'arrosage:')
    print('Aire du terrain:', fieldArea, 'm2    Nombre de goutteurs:', nbGoutteur,
          '    Débit des goutteurs:', debitGoutteur, 'L/h    Débit total:', debitTotal, 'L/h\n')



    if (waterRequired > 0 and rain < 0.5 or soilHumidity < H_treshhold):
        wateringTime = waterRequired / hauteurTotal
        A = 1
    else:
        A = 0

    if (A):
        print('Arrosage ON')
        print('Temp d\'arrosage: ', wateringTime, ' heures', '    Eau nécessaire:', debitTotal*wateringTime, 'L')
    else:
        print('Arrosage OFF')



# ------- Ce qui était prévu avant les changements -------

# capteur de luminosité
# type de sol (3 modèles différents) => absorption potentielle variable => vitesse d'arrosage , au frequence d'arrosage
# courbe de croisssance, besoin en eau varie selon la taille (le poid de la plante)
# prendre en compte la transpiration => éviter certaines heures d'arrosage
# augmenter l'apport en eau selon => lumière, température air, humidité air (trop sec)


# --- prevoir une analyse toutes les 5-10 min pour avoir une frequence optimale ---- (a voir selon vitesse de drainage du sol)
# ou determiner un debit si vanne à débit variable

# consommation de base (en fonction du poids de la plante) (formule degre jour)

# prendre en compte les facteur externe pour ajuster la consommation (multiplicateur du poid de la plante)
#           -  confronter avec les donnée reelle (arduino)

# determiner l'humidité necessaire du sol (prenant en compte le type et le drainage)

# prendre en compte l'heure (ne pas arroser entre 11h et 15h)

# prendre en compte la meteo:
#               - prevoir un surchage si conditions futures trop chaude, lumineuses
#               - ne pas arroser s'il peut dans les heures qui viennent (à voir le delai)

# si humidité insuffisante, on ouvre (retourne 1)
# si humidité suffisante, on ferme (retourne 0)

# si vanne à debit variable, on retourn un debit (entre 0.0 et 1.0)


# par la suite: évaluation du systeme : a ton bien arrosé? suffisament? pas assez? trop? consommation d'eau adaptée?
#  - courbe de besoin en eau théorique VS courbe eau consommée
#  - courbe de besoin en humidité du sol théorique VS courbe d'humidité du sol obtenu
#  - croissance de la plante théorique VS croissance de la plante réelle
