from sklearn import svm


# --- Get the actual water volume present in the soil ---
# How ? depending on the soil type (1, 2 or 3)
# soilType = 1  => Drainant (sableux/caillouteux)
# soilType = 2  =>  Equilibré
# soilType = 3  =>  Argileux (peu drainant)
# Regression algorithm with data from our experience
# L'algorithm analyse les données et permet de prédire le niveau d'eau (en mm) présent dans le sol
# selon les conditions actuelles mesurées (humidité, tempéreture, type de sol, lumiunosité, vitesse du vent) envoyées en paramètre

def getMillemetersOfWaterInSoil(soilType, soilHumidity, soilTemperature):
    # SVM Support Vector Regression
    soilType = soilType  # 1--X   2--Y  3--Z

    if soilType == 1:
        X = [[16.1, 26], [46.5, 25], [72.3, 25.2], [82.6, 25], [85.2, 25.5], [85.7, 26.2], [81.6, 26.5]]  # Environment conditions parameters
        y = [0, 2.5, 5, 7.5, 10, 12.5, 15]  # Volume of H2O (mm)
    elif soilType == 2:
        X = [[19.1, 30], [57.4, 30], [79.1, 27.6], [87.8, 27], [90.4, 27.4], [95.7, 26.5], [97.8, 27.2]]  # Environment conditions parameters
        y = [0, 2.5, 5, 7.5, 10, 12.5, 15]  # Volume of H2O (mm)
    elif soilType == 3:
        X = [[21.4, 27], [77, 25], [90, 25.6], [93, 26], [93.5, 25.9], [97.4, 27], [100, 27]]  # Environment conditions parameters
        y = [0, 2.5, 5, 7.5, 10, 12.5, 15]  # Volume of H2O (mm)

    regr_soil = svm.SVR()
    regr_soil.fit(X, y)

    millimetersOfWater = regr_soil.predict([[soilHumidity, soilTemperature]])  # Prediction of water volume in this soil conditions

    return millimetersOfWater  # en mm (hauteur)
