"""Romanian counties (județe) and the municipality of Bucharest."""

import unicodedata

COUNTIES = [
    "Alba", "Arad", "Argeș", "Bacău", "Bihor", "Bistrița-Năsăud",
    "Botoșani", "Brăila", "Brașov", "Buzău", "Călărași", "Caraș-Severin",
    "Cluj", "Constanța", "Covasna", "Dâmbovița", "Dolj", "Galați",
    "Giurgiu", "Gorj", "Harghita", "Hunedoara", "Ialomița", "Iași",
    "Ilfov", "Maramureș", "Mehedinți", "Mureș", "Neamț", "Olt",
    "Prahova", "Sălaj", "Satu Mare", "Sibiu", "Suceava", "Teleorman",
    "Timiș", "Tulcea", "Vâlcea", "Vaslui", "Vrancea",
    "București",
]

# English Wikipedia article for each county
WIKIPEDIA = {name: f"{name} County" for name in COUNTIES}
WIKIPEDIA["București"] = "Bucharest"

# Wikimedia Commons file with the county highlighted on a map of Romania.
# The files are named without diacritics: "Arges in Romania.svg".
MAP_FILES = {
    name: unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode() + " in Romania.svg"
    for name in COUNTIES
}
MAP_FILES["București"] = "Bucharest in Romania.svg"
