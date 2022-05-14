from sklearn import svm


# --- Get the water need of the plant (Grape) for today ---
# How ? depending on the annual Grape needs (data from the scientific paper)
# Regression algorithm
# L'algorithm analyse les données et permet de prédire les besoin de la Vigne selon le jour de l'année
def getMillimetersOfWaterNeeded(jour):
    # SVM Support Vector Regression

    X = [[0], [31], [50], [81], [111], [142], [172], [203], [233], [263], [294], [325]]  # Days
    y = [100/30, 140/30, 170/30, 185/30, 212/30, 198/30, 137/30, 136/30, 161/30, 154/30, 97/30, 81/30]  # Volume of H2O (mm) per day, Data from paper

    regr_requirement = svm.SVR()
    regr_requirement.fit(X, y)

    millimetersOfWaterNeeded = regr_requirement.predict([[jour]])

    return millimetersOfWaterNeeded  # en mm (hauteur)
