# -*- coding: utf-8 -*-
"""
Données mockées riches pour le développement et les tests.
- 20 pilotes
- 10 écuries
- Classements pilotes réalistes (ordre/points issus de ta capture)
- Classement constructeurs calculé automatiquement (cohérent)
- Calendrier élargi + dernière course factice
"""

from datetime import date

# ────────────────────────────────────────────────────────────────────────────────
# ÉCURIES
# ────────────────────────────────────────────────────────────────────────────────

MOCK_CONSTRUCTORS = [
    {"constructorId": "mclaren",       "name": "McLaren",        "nationality": "British"},
    {"constructorId": "red_bull",      "name": "Red Bull",       "nationality": "Austrian"},
    {"constructorId": "mercedes",      "name": "Mercedes",       "nationality": "German"},
    {"constructorId": "ferrari",       "name": "Ferrari",        "nationality": "Italian"},
    {"constructorId": "williams",      "name": "Williams",       "nationality": "British"},
    {"constructorId": "racing_bulls",  "name": "Racing Bulls",   "nationality": "Italian"},
    {"constructorId": "sauber",        "name": "Sauber",         "nationality": "Swiss"},
    {"constructorId": "aston_martin",  "name": "Aston Martin",   "nationality": "British"},
    {"constructorId": "haas",          "name": "Haas",           "nationality": "American"},
    {"constructorId": "alpine",        "name": "Alpine",         "nationality": "French"},
]

_CONSTRUCTORS_BY_ID = {c["constructorId"]: c for c in MOCK_CONSTRUCTORS}


# ────────────────────────────────────────────────────────────────────────────────
# PILOTES (20)
# Ajout d'un champ "constructorId" pour relier proprement aux écuries.
# ────────────────────────────────────────────────────────────────────────────────

MOCK_DRIVERS = [
    # McLaren
    {"driverId": "piastri",    "permanentNumber": "81", "code": "PIA", "givenName": "Oscar",   "familyName": "Piastri",   "dateOfBirth": "2001-04-06", "nationality": "Australian", "constructorId": "mclaren"},
    {"driverId": "norris",     "permanentNumber": "4",  "code": "NOR", "givenName": "Lando",   "familyName": "Norris",    "dateOfBirth": "1999-11-13", "nationality": "British",    "constructorId": "mclaren"},

    # Red Bull
    {"driverId": "verstappen", "permanentNumber": "1",  "code": "VER", "givenName": "Max",     "familyName": "Verstappen","dateOfBirth": "1997-09-30", "nationality": "Dutch",      "constructorId": "red_bull"},
    {"driverId": "tsunoda",    "permanentNumber": "22", "code": "TSU", "givenName": "Yuki",    "familyName": "Tsunoda",   "dateOfBirth": "2000-05-11", "nationality": "Japanese",   "constructorId": "racing_bulls"},

    # Mercedes
    {"driverId": "russell",    "permanentNumber": "63", "code": "RUS", "givenName": "George",  "familyName": "Russell",   "dateOfBirth": "1998-02-15", "nationality": "British",    "constructorId": "mercedes"},
    {"driverId": "antonelli",  "permanentNumber": "7",  "code": "ANT", "givenName": "Kimi",    "familyName": "Antonelli", "dateOfBirth": "2006-08-25", "nationality": "Italian",    "constructorId": "mercedes"},

    # Ferrari
    {"driverId": "leclerc",    "permanentNumber": "16", "code": "LEC", "givenName": "Charles", "familyName": "Leclerc",   "dateOfBirth": "1997-10-16", "nationality": "Monegasque", "constructorId": "ferrari"},
    {"driverId": "hamilton",   "permanentNumber": "44", "code": "HAM", "givenName": "Lewis",   "familyName": "Hamilton",  "dateOfBirth": "1985-01-07", "nationality": "British",    "constructorId": "ferrari"},

    # Williams
    {"driverId": "albon",      "permanentNumber": "23", "code": "ALB", "givenName": "Alex",    "familyName": "Albon",     "dateOfBirth": "1996-03-23", "nationality": "Thai",       "constructorId": "williams"},
    {"driverId": "sainz_jr",   "permanentNumber": "55", "code": "SAI", "givenName": "Carlos",  "familyName": "Sainz Jr.", "dateOfBirth": "1994-09-01", "nationality": "Spanish",    "constructorId": "williams"},  # mock selon ton tableau

    # Racing Bulls
    {"driverId": "hadjar",     "permanentNumber": "20", "code": "HAD", "givenName": "Isack",   "familyName": "Hadjar",    "dateOfBirth": "2004-09-28", "nationality": "French",     "constructorId": "racing_bulls"},
    {"driverId": "lawson",     "permanentNumber": "30", "code": "LAW", "givenName": "Liam",    "familyName": "Lawson",    "dateOfBirth": "2002-02-11", "nationality": "New Zealander","constructorId": "racing_bulls"},

    # Sauber
    {"driverId": "hulkenberg", "permanentNumber": "27", "code": "HUL", "givenName": "Nico",    "familyName": "Hülkenberg","dateOfBirth": "1987-08-19", "nationality": "German",     "constructorId": "sauber"},
    {"driverId": "bortoleto",  "permanentNumber": "50", "code": "BOR", "givenName": "Gabriel", "familyName": "Bortoleto", "dateOfBirth": "2004-10-14", "nationality": "Brazilian",  "constructorId": "sauber"},

    # Aston Martin
    {"driverId": "alonso",     "permanentNumber": "14", "code": "ALO", "givenName": "Fernando","familyName": "Alonso",    "dateOfBirth": "1981-07-29", "nationality": "Spanish",    "constructorId": "aston_martin"},
    {"driverId": "stroll",     "permanentNumber": "18", "code": "STR", "givenName": "Lance",   "familyName": "Stroll",    "dateOfBirth": "1998-10-29", "nationality": "Canadian",   "constructorId": "aston_martin"},

    # Haas
    {"driverId": "bearman",    "permanentNumber": "87", "code": "BEA", "givenName": "Oliver",  "familyName": "Bearman",   "dateOfBirth": "2005-05-08", "nationality": "British",    "constructorId": "haas"},
    {"driverId": "ocon",       "permanentNumber": "31", "code": "OCO", "givenName": "Esteban", "familyName": "Ocon",      "dateOfBirth": "1996-09-17", "nationality": "French",     "constructorId": "haas"},  # mock pour coller au tableau

    # Alpine
    {"driverId": "gasly",      "permanentNumber": "10", "code": "GAS", "givenName": "Pierre",  "familyName": "Gasly",     "dateOfBirth": "1996-02-07", "nationality": "French",     "constructorId": "alpine"},
    {"driverId": "colapinto",  "permanentNumber": "43", "code": "COL", "givenName": "Franco",  "familyName": "Colapinto", "dateOfBirth": "2003-05-27", "nationality": "Argentinian","constructorId": "alpine"},
]

_DRIVERS_BY_ID = {d["driverId"]: d for d in MOCK_DRIVERS}


# ────────────────────────────────────────────────────────────────────────────────
# CLASSEMENT PILOTES (ordre et points issus de ta capture, wins/podiums mock)
# ────────────────────────────────────────────────────────────────────────────────

# (position, driverId, points, wins, podiums)
_raw_driver_table = [
    (1,  "piastri",    336, 7, 14),
    (2,  "norris",     314, 5, 14),
    (3,  "verstappen", 273, 4, 9),
    (4,  "russell",    237, 2, 8),
    (5,  "leclerc",    173, 0, 5),
    (6,  "hamilton",   125, 0, 2),
    (7,  "antonelli",   88, 0, 1),
    (8,  "albon",       70, 0, 0),
    (9,  "hadjar",      39, 0, 1),
    (10, "hulkenberg",  37, 0, 1),
    (11, "alonso",      36, 0, 0),
    (12, "sainz_jr",    32, 0, 1),
    (13, "stroll",      32, 0, 0),
    (14, "lawson",      30, 0, 0),
    (15, "ocon",        28, 0, 0),
    (16, "gasly",       20, 0, 0),
    (17, "tsunoda",     20, 0, 0),
    (18, "bortoleto",   18, 0, 0),
    (19, "bearman",     18, 0, 0),
    (20, "colapinto",    0, 0, 0),
]

def _driver_entry(pos, driver_id, points, wins, podiums):
    d = _DRIVERS_BY_ID[driver_id]
    constructor = _CONSTRUCTORS_BY_ID[d["constructorId"]]
    return {
        "position": str(pos),
        "positionText": str(pos),
        "points": str(points),
        "wins": str(wins),
        "podiums": str(podiums),
        "Driver": {k: d[k] for k in ["driverId", "permanentNumber", "code", "givenName", "familyName", "dateOfBirth", "nationality"]},
        "Constructors": [constructor],
    }

MOCK_DRIVER_STANDINGS = [_driver_entry(*row) for row in _raw_driver_table]


# ────────────────────────────────────────────────────────────────────────────────
# CLASSEMENT CONSTRUCTEURS – calculé à partir des points pilotes
# ────────────────────────────────────────────────────────────────────────────────

def compute_constructor_standings_from_drivers(driver_standings):
    agg = {}
    for row in driver_standings:
        constructor = row["Constructors"][0]
        cid = constructor["constructorId"]
        pts = float(row["points"])
        wins = int(row.get("wins", "0"))
        if cid not in agg:
            agg[cid] = {"points": 0.0, "wins": 0, "Constructor": constructor}
        agg[cid]["points"] += pts
        agg[cid]["wins"] += wins

    # Tri par points décroissants puis wins
    ordered = sorted(agg.values(), key=lambda x: (x["points"], x["wins"]), reverse=True)
    result = []
    for i, item in enumerate(ordered, 1):
        result.append({
            "position": str(i),
            "positionText": str(i),
            "points": str(int(item["points"])),
            "wins": str(item["wins"]),
            "Constructor": item["Constructor"],
        })
    return result

MOCK_CONSTRUCTOR_STANDINGS = compute_constructor_standings_from_drivers(MOCK_DRIVER_STANDINGS)


# ────────────────────────────────────────────────────────────────────────────────
# CALENDRIER (quelques manches)
# ────────────────────────────────────────────────────────────────────────────────

MOCK_SCHEDULE = [
    {
        "season": "2025",
        "round": "1",
        "raceName": "Australian Grand Prix",
        "Circuit": {
            "circuitId": "albert_park",
            "circuitName": "Albert Park Circuit",
            "Location": {"lat": "-37.8497", "long": "144.968", "locality": "Melbourne", "country": "Australia"},
        },
        "date": "2025-03-16",
        "time": "05:00:00Z",
    },
    {
        "season": "2025",
        "round": "2",
        "raceName": "Saudi Arabian Grand Prix",
        "Circuit": {
            "circuitId": "jeddah",
            "circuitName": "Jeddah Corniche Circuit",
            "Location": {"lat": "21.6319", "long": "39.1044", "locality": "Jeddah", "country": "Saudi Arabia"},
        },
        "date": "2025-03-23",
        "time": "17:00:00Z",
    },
    {
        "season": "2025",
        "round": "3",
        "raceName": "Bahrain Grand Prix",
        "Circuit": {
            "circuitId": "bahrain",
            "circuitName": "Bahrain International Circuit",
            "Location": {"lat": "26.0325", "long": "50.5106", "locality": "Sakhir", "country": "Bahrain"},
        },
        "date": "2025-03-30",
        "time": "15:00:00Z",
    },
    {
        "season": "2025",
        "round": "4",
        "raceName": "Japanese Grand Prix",
        "Circuit": {
            "circuitId": "suzuka",
            "circuitName": "Suzuka Circuit",
            "Location": {"lat": "34.8431", "long": "136.541", "locality": "Suzuka", "country": "Japan"},
        },
        "date": "2025-04-13",
        "time": "06:00:00Z",
    },
    {
        "season": "2025",
        "round": "5",
        "raceName": "Emilia Romagna Grand Prix",
        "Circuit": {
            "circuitId": "imola",
            "circuitName": "Autodromo Enzo e Dino Ferrari",
            "Location": {"lat": "44.3439", "long": "11.7167", "locality": "Imola", "country": "Italy"},
        },
        "date": "2025-04-27",
        "time": "13:00:00Z",
    },
    {
        "season": "2025",
        "round": "6",
        "raceName": "Monaco Grand Prix",
        "Circuit": {
            "circuitId": "monaco",
            "circuitName": "Circuit de Monaco",
            "Location": {"lat": "43.7347", "long": "7.42056", "locality": "Monte Carlo", "country": "Monaco"},
        },
        "date": "2025-05-25",
        "time": "13:00:00Z",
    },
]


# ────────────────────────────────────────────────────────────────────────────────
# DERNIÈRE COURSE (résultats factices, mais cohérents avec les entités)
# ────────────────────────────────────────────────────────────────────────────────

def _driver_in_standings(driver_id):
    for row in MOCK_DRIVER_STANDINGS:
        if row["Driver"]["driverId"] == driver_id:
            return row["Driver"], row["Constructors"][0]
    raise KeyError(driver_id)

_1st_driver, _1st_ctor = _driver_in_standings("piastri")
_2nd_driver, _2nd_ctor = _driver_in_standings("norris")
_3rd_driver, _3rd_ctor = _driver_in_standings("verstappen")

MOCK_LAST_RACE = {
    "season": "2025",
    "round": "6",
    "raceName": "Monaco Grand Prix",
    "Circuit": {
        "circuitId": "monaco",
        "circuitName": "Circuit de Monaco",
        "Location": {"lat": "43.7347", "long": "7.42056", "locality": "Monte Carlo", "country": "Monaco"},
    },
    "date": str(date(2025, 5, 25)),
    "time": "13:00:00Z",
    "Results": [
        {
            "number": _1st_driver.get("permanentNumber", "0"),
            "position": "1",
            "positionText": "1",
            "points": "25",
            "Driver": _1st_driver,
            "Constructor": _1st_ctor,
            "grid": "2",
            "laps": "78",
            "status": "Finished",
            "Time": {"millis": "6289000", "time": "1:44:49.000"},
        },
        {
            "number": _2nd_driver.get("permanentNumber", "0"),
            "position": "2",
            "positionText": "2",
            "points": "18",
            "Driver": _2nd_driver,
            "Constructor": _2nd_ctor,
            "grid": "3",
            "laps": "78",
            "status": "Finished",
            "Time": {"millis": "6290500", "time": "+1.500"},
        },
        {
            "number": _3rd_driver.get("permanentNumber", "0"),
            "position": "3",
            "positionText": "3",
            "points": "15",
            "Driver": _3rd_driver,
            "Constructor": _3rd_ctor,
            "grid": "1",
            "laps": "78",
            "status": "Finished",
            "Time": {"millis": "6292200", "time": "+3.200"},
        },
    ],
}

# ────────────────────────────────────────────────────────────────────────────────
# Helpers d’export compatibles avec tes endpoints
# ────────────────────────────────────────────────────────────────────────────────

def get_drivers_current():
    """Liste des pilotes actuels."""
    return [d for d in MOCK_DRIVERS]

def get_constructors_current():
    """Liste des écuries actuelles."""
    return [c for c in MOCK_CONSTRUCTORS]

def get_driver_standings():
    """Classement pilotes (mock)."""
    return [row for row in MOCK_DRIVER_STANDINGS]

def get_constructor_standings():
    """Classement constructeurs (agrégé)."""
    return [row for row in MOCK_CONSTRUCTOR_STANDINGS]

def get_schedule_current():
    """Calendrier de la saison."""
    return [r for r in MOCK_SCHEDULE]

def get_last_race():
    """Dernière course (mock)."""
    return MOCK_LAST_RACE
