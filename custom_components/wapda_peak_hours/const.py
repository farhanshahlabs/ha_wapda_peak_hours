"""Constants for WAPDA Peak Hours integration."""

DOMAIN = "wapda_peak_hours"
CONF_DISCO = "disco"
TIMEZONE = "Asia/Karachi"

# Each DISCO maps to a list of (months, start_hour, start_minute, end_hour, end_minute)
# months is a list of month numbers (1-12)
DISCO_SCHEDULES = {
    "IESCO": [
        ([12, 1, 2], 17, 0, 21, 0),
        ([3, 4, 5, 9, 10, 11], 18, 0, 22, 0),
        ([6, 7, 8], 19, 0, 23, 0),
    ],
    "GEPCO": [
        ([12, 1, 2], 17, 0, 21, 0),
        ([3, 4, 5, 9, 10, 11], 18, 0, 22, 0),
        ([6, 7, 8], 19, 0, 23, 0),
    ],
    "LESCO": [
        ([12, 1, 2], 17, 0, 21, 0),
        ([3, 4, 5, 9, 10, 11], 18, 0, 22, 0),
        ([6, 7, 8], 19, 0, 23, 0),
    ],
    "MEPCO": [
        ([11, 12, 1, 2, 3], 18, 0, 22, 0),
        ([4, 5, 6, 7, 8, 9, 10], 18, 30, 22, 30),
    ],
    "PESCO": [
        ([11, 12, 1, 2, 3], 18, 0, 22, 0),
        ([4, 5, 6, 7, 8, 9, 10], 18, 30, 22, 30),
    ],
    "HESCO": [
        ([11, 12, 1, 2, 3], 18, 0, 22, 0),
        ([4, 5, 6, 7, 8, 9, 10], 18, 30, 22, 30),
    ],
    "QESCO": [
        ([11, 12, 1, 2, 3], 18, 0, 22, 0),
        ([4, 5, 6, 7, 8, 9, 10], 18, 30, 22, 30),
    ],
    "SEPCO": [
        ([11, 12, 1, 2, 3], 18, 0, 22, 0),
        ([4, 5, 6, 7, 8, 9, 10], 18, 30, 22, 30),
    ],
    "KE": [
        ([11, 12, 1, 2, 3], 18, 0, 22, 0),
        ([4, 5, 6, 7, 8, 9, 10], 18, 30, 22, 30),
    ],
    "TESCO": [
        (list(range(1, 13)), 18, 0, 22, 0),
    ],
}

DISCO_NAMES = {
    "IESCO": "IESCO - Islamabad Electric Supply Company",
    "GEPCO": "GEPCO - Gujranwala Electric Power Company",
    "LESCO": "LESCO - Lahore Electric Supply Company",
    "MEPCO": "MEPCO - Multan Electric Power Company",
    "PESCO": "PESCO - Peshawar Electric Supply Company",
    "HESCO": "HESCO - Hyderabad Electric Supply Company",
    "QESCO": "QESCO - Quetta Electric Supply Company",
    "SEPCO": "SEPCO - Sukkur Electric Power Company",
    "KE": "KE - Karachi Electric",
    "TESCO": "TESCO - Tribal Electric Supply Company",
}
