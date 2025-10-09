# Données mockées pour le développement et les tests

MOCK_DRIVERS = [
    {
        "driverId": "verstappen",
        "permanentNumber": "1",
        "code": "VER",
        "givenName": "Max",
        "familyName": "Verstappen",
        "dateOfBirth": "1997-09-30",
        "nationality": "Dutch"
    },
    {
        "driverId": "perez",
        "permanentNumber": "11",
        "code": "PER",
        "givenName": "Sergio",
        "familyName": "Pérez",
        "dateOfBirth": "1990-01-26",
        "nationality": "Mexican"
    },
    {
        "driverId": "hamilton",
        "permanentNumber": "44",
        "code": "HAM",
        "givenName": "Lewis",
        "familyName": "Hamilton",
        "dateOfBirth": "1985-01-07",
        "nationality": "British"
    },
    {
        "driverId": "leclerc",
        "permanentNumber": "16",
        "code": "LEC",
        "givenName": "Charles",
        "familyName": "Leclerc",
        "dateOfBirth": "1997-10-16",
        "nationality": "Monegasque"
    },
    {
        "driverId": "sainz",
        "permanentNumber": "55",
        "code": "SAI",
        "givenName": "Carlos",
        "familyName": "Sainz",
        "dateOfBirth": "1994-09-01",
        "nationality": "Spanish"
    },
    {
        "driverId": "russell",
        "permanentNumber": "63",
        "code": "RUS",
        "givenName": "George",
        "familyName": "Russell",
        "dateOfBirth": "1998-02-15",
        "nationality": "British"
    },
    {
        "driverId": "norris",
        "permanentNumber": "4",
        "code": "NOR",
        "givenName": "Lando",
        "familyName": "Norris",
        "dateOfBirth": "1999-11-13",
        "nationality": "British"
    },
    {
        "driverId": "alonso",
        "permanentNumber": "14",
        "code": "ALO",
        "givenName": "Fernando",
        "familyName": "Alonso",
        "dateOfBirth": "1981-07-29",
        "nationality": "Spanish"
    }
]

MOCK_CONSTRUCTORS = [
    {
        "constructorId": "red_bull",
        "name": "Red Bull Racing",
        "nationality": "Austrian"
    },
    {
        "constructorId": "ferrari",
        "name": "Ferrari",
        "nationality": "Italian"
    },
    {
        "constructorId": "mercedes",
        "name": "Mercedes",
        "nationality": "German"
    },
    {
        "constructorId": "mclaren",
        "name": "McLaren",
        "nationality": "British"
    },
    {
        "constructorId": "aston_martin",
        "name": "Aston Martin",
        "nationality": "British"
    }
]

MOCK_DRIVER_STANDINGS = [
    {
        "position": "1",
        "positionText": "1",
        "points": "575",
        "wins": "19",
        "Driver": {
            "driverId": "verstappen",
            "permanentNumber": "1",
            "code": "VER",
            "givenName": "Max",
            "familyName": "Verstappen",
            "dateOfBirth": "1997-09-30",
            "nationality": "Dutch"
        },
        "Constructors": [
            {
                "constructorId": "red_bull",
                "name": "Red Bull Racing",
                "nationality": "Austrian"
            }
        ]
    },
    {
        "position": "2",
        "positionText": "2",
        "points": "285",
        "wins": "2",
        "Driver": {
            "driverId": "perez",
            "permanentNumber": "11",
            "code": "PER",
            "givenName": "Sergio",
            "familyName": "Pérez",
            "dateOfBirth": "1990-01-26",
            "nationality": "Mexican"
        },
        "Constructors": [
            {
                "constructorId": "red_bull",
                "name": "Red Bull Racing",
                "nationality": "Austrian"
            }
        ]
    },
    {
        "position": "3",
        "positionText": "3",
        "points": "234",
        "wins": "0",
        "Driver": {
            "driverId": "hamilton",
            "permanentNumber": "44",
            "code": "HAM",
            "givenName": "Lewis",
            "familyName": "Hamilton",
            "dateOfBirth": "1985-01-07",
            "nationality": "British"
        },
        "Constructors": [
            {
                "constructorId": "mercedes",
                "name": "Mercedes",
                "nationality": "German"
            }
        ]
    },
    {
        "position": "4",
        "positionText": "4",
        "points": "206",
        "wins": "1",
        "Driver": {
            "driverId": "leclerc",
            "permanentNumber": "16",
            "code": "LEC",
            "givenName": "Charles",
            "familyName": "Leclerc",
            "dateOfBirth": "1997-10-16",
            "nationality": "Monegasque"
        },
        "Constructors": [
            {
                "constructorId": "ferrari",
                "name": "Ferrari",
                "nationality": "Italian"
            }
        ]
    },
    {
        "position": "5",
        "positionText": "5",
        "points": "200",
        "wins": "1",
        "Driver": {
            "driverId": "sainz",
            "permanentNumber": "55",
            "code": "SAI",
            "givenName": "Carlos",
            "familyName": "Sainz",
            "dateOfBirth": "1994-09-01",
            "nationality": "Spanish"
        },
        "Constructors": [
            {
                "constructorId": "ferrari",
                "name": "Ferrari",
                "nationality": "Italian"
            }
        ]
    }
]

MOCK_CONSTRUCTOR_STANDINGS = [
    {
        "position": "1",
        "positionText": "1",
        "points": "860",
        "wins": "21",
        "Constructor": {
            "constructorId": "red_bull",
            "name": "Red Bull Racing",
            "nationality": "Austrian"
        }
    },
    {
        "position": "2",
        "positionText": "2",
        "points": "406",
        "wins": "2",
        "Constructor": {
            "constructorId": "ferrari",
            "name": "Ferrari",
            "nationality": "Italian"
        }
    },
    {
        "position": "3",
        "positionText": "3",
        "points": "409",
        "wins": "0",
        "Constructor": {
            "constructorId": "mercedes",
            "name": "Mercedes",
            "nationality": "German"
        }
    }
]

MOCK_SCHEDULE = [
    {
        "season": "2024",
        "round": "1",
        "raceName": "Bahrain Grand Prix",
        "Circuit": {
            "circuitId": "bahrain",
            "circuitName": "Bahrain International Circuit",
            "Location": {
                "lat": "26.0325",
                "long": "50.5106",
                "locality": "Sakhir",
                "country": "Bahrain"
            }
        },
        "date": "2024-03-02",
        "time": "15:00:00Z"
    },
    {
        "season": "2024",
        "round": "2",
        "raceName": "Saudi Arabian Grand Prix",
        "Circuit": {
            "circuitId": "jeddah",
            "circuitName": "Jeddah Corniche Circuit",
            "Location": {
                "lat": "21.6319",
                "long": "39.1044",
                "locality": "Jeddah",
                "country": "Saudi Arabia"
            }
        },
        "date": "2024-03-09",
        "time": "17:00:00Z"
    },
    {
        "season": "2024",
        "round": "3",
        "raceName": "Australian Grand Prix",
        "Circuit": {
            "circuitId": "albert_park",
            "circuitName": "Albert Park Circuit",
            "Location": {
                "lat": "-37.8497",
                "long": "144.968",
                "locality": "Melbourne",
                "country": "Australia"
            }
        },
        "date": "2024-03-24",
        "time": "05:00:00Z"
    }
]

MOCK_LAST_RACE = {
    "season": "2024",
    "round": "20",
    "raceName": "São Paulo Grand Prix",
    "Circuit": {
        "circuitId": "interlagos",
        "circuitName": "Autódromo José Carlos Pace",
        "Location": {
            "lat": "-23.7036",
            "long": "-46.6997",
            "locality": "São Paulo",
            "country": "Brazil"
        }
    },
    "date": "2024-11-03",
    "time": "17:00:00Z",
    "Results": [
        {
            "number": "1",
            "position": "1",
            "positionText": "1",
            "points": "25",
            "Driver": MOCK_DRIVER_STANDINGS[0]["Driver"],
            "Constructor": MOCK_CONSTRUCTORS[0],
            "grid": "1",
            "laps": "71",
            "status": "Finished",
            "Time": {
                "millis": "5843567",
                "time": "1:37:23.567"
            }
        },
        {
            "number": "16",
            "position": "2",
            "positionText": "2",
            "points": "18",
            "Driver": MOCK_DRIVER_STANDINGS[3]["Driver"],
            "Constructor": MOCK_CONSTRUCTORS[1],
            "grid": "3",
            "laps": "71",
            "status": "Finished",
            "Time": {
                "millis": "5845234",
                "time": "+1.667"
            }
        }
    ]
}