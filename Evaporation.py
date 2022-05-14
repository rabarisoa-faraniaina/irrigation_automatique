import math


def getMillimetersOfEvaporation(T, alt, j, RH, phi, windSpeed):
    # constants
    c_p = 1.013
    epsilon = 0.622
    I_s = 4921  # Solar constant, kJ/m^2/h
    a_s = 0.355
    b_s = 0.68
    Albedo = 0.25  # Albedo constant
    a_e = 0.56
    b_e = 0.08
    a_l = 0.2
    sigma = 0.0000049  # Stefan-Boltzmann constant, kJ/(m^2 K^4 d)

    coef = 0.33
    c2 = 90
    c3 = 273
    # Specific heat (kJ/kg) for a given temperature (oC)
    templamda = 2501 - 2.361 * T
    # Standard pressure (hPa) for a given elevation (m)
    temppressure = 1013 * (1 - 0.00002256 * alt) ** 5.256
    # Air density (kg/m^3) at a given air pressure (hPa) and temperature (oC)
    tempdensity = 0.3486 * temppressure / (273 + T)
    # Psychrometric constant (hPa/oC) for a given pressure (hPa) and Specific heat (kJ/kg)
    tempgamma = (c_p / epsilon) * temppressure / templamda
    # Saturation vapor pressure (hPa) for a given temperature (oC)
    tempe_s = 6.11 * math.exp(17.27 * T / (237.3 + T))
    # Slope of the saturation vapor pressure curve (hPa/oC) for a given temperature (oC)
    tempdelta = 4098 * tempe_s / (237.3 + T) ** 2

    # vapor pressure (hPa)
    tempe = tempe_s * RH

    # Solar declination (rad) for a given day
    tempdeclination = -0.4093 * math.cos(2 * math.pi * j / 365 + 0.16)
    # Eccentricity for a given day
    tempeccentricity = 1 + 0.034 * math.cos(2 * math.pi * j / 365 - 0.05)
    # Sunset angle (rad) for a given day and lattitude
    tempphi_rad = phi * math.pi / 180
    tempphi = - math.tan(tempphi_rad) * math.tan(tempdeclination)
    # For lattitude > 66.5 (or < - 66.5)
    tempo_s = tempphi
    if math.fabs(tempo_s) > 1.161:
        o_s = 0
    else:
        o_s = float(math.acos(tempo_s))
    tempN = (24 / math.pi) * o_s
    cl = 1 / tempN
    # Extraterrestial shortwave radiation (kJ/m^2/d) for a given day and lattitude
    S0temp = (24 / math.pi) * I_s * tempeccentricity
    tempS_0 = S0temp * (o_s * math.sin(tempphi_rad) * math.sin(tempdeclination) + math.cos(tempphi_rad) * math.cos(
        tempdeclination) * math.sin(o_s))
    tempf_s = a_s + b_s * (1 - cl)
    # Shortwave radiation (kJ/m^2/d) for given albedo, fraction of sunshine duration
    tempS_n = (1 - Albedo) * tempf_s * tempS_0
    # Lo
    tempe_n = a_e - b_e * math.sqrt(tempe)
    tempf_l = a_l + (1 - a_l) * (1 - cl)
    # Longwave radiation (kJ/m^2/d) for given temperature (oC), fraction of sunshine duration
    tempL_n = tempe_n * tempf_l * sigma * (T + 273) ** 4
    # Mass transfer term for various cases of evaporation calculations
    tempgamma_rc = (1 + coef * windSpeed) * tempgamma
    # Mass transfer term (kg/(hPa m^2 d)) of reference crop for given wind speed (m/s)
    tempF_rc = (c2 / (T + c3)) * windSpeed
    # Penman-Montieth method
    # A=Δ/(Δ+γ')
    tempA = tempdelta / (tempdelta + tempgamma_rc)
    # Β= γ/(Δ+γ')
    tempB = tempgamma / (tempdelta + tempgamma_rc)
    tempD = tempe_s - tempe
    tempRn = tempS_n - tempL_n
    temp_Epm = tempA * tempRn / templamda + tempB * tempF_rc * tempD
    E = temp_Epm / 3
    return E  # L/jour/m2   ou une hauteur de 1mm
