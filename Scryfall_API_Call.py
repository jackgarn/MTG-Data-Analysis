import requests
import json

# Gets the JSON for ALL MTG Cards
response = requests.get('https://data.scryfall.io/default-cards/default-cards-20230120100454.json')
# stores the call in a json file
with open("Cards.json","w") as file:
    json.dump(response.json(),file,indent = 4)