import requests
import json
from typing import List, Dict

# This script fetches Pokémon data from the PokeAPI and saves it to a JSON file.

class Pokemon:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.data = self.get_data()

    def get_data(self):
        print("Fetching data from:", self.url)
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data for {self.name}: {response.status_code}")

    def get_name(self):
        return self.data['name']

    def get_height(self):
        return self.data['height'] / 10

    def get_weight(self):
        return self.data['weight'] / 10
    
    def get_height_inches(self):
        return round(self.get_height() * 39.3701, 1)
    
    def get_weight_pounds(self):
        return round(self.get_weight() * 2.20462, 1)
    
    def get_types(self):
        types = [type_info['type']['name'] for type_info in self.data['types']]
        return types
    
    def get_abilities(self):
        abilities = [ability_info['ability']['name'] for ability_info in self.data['abilities']]
        return abilities
    
    def get_image(self):
        return self.data['sprites']['other']['official-artwork']['front_default']
    
    def get_shiny_image(self):
        return self.data['sprites']['other']['official-artwork']['front_shiny']
    
    def get_stats(self):
        stats = {stat_info['stat']['name']: stat_info['base_stat'] for stat_info in self.data['stats']}
        return stats
    
    def get_id(self):
        return self.data['id']
    
    def get_dict(self):
        return {
            "id": self.get_id(),
            "name": self.get_name(),
            "height": {"meters": self.get_height(), "inches": self.get_height_inches()},
            "weight": {"kilograms": self.get_weight(), "pounds": self.get_weight_pounds()},
            "types": self.get_types(),
            "abilities": self.get_abilities(),
            "image": self.get_image(),
            "shiny_image": self.get_shiny_image(),
            "stats": self.get_stats()
        }

ALL_POKEMON_URL = "https://pokeapi.co/api/v2/pokemon?limit=1025&offset=0"


def main():
    response = requests.get(ALL_POKEMON_URL)
    if response.status_code == 200:
        all_pokemon_data = response.json()
        all_pokemon = [Pokemon(pokemon['name'], pokemon['url']) for pokemon in all_pokemon_data['results']]
        
    else:
        print("Error fetching all Pokémon data.")
    
    save_pokemon_data(all_pokemon, 'pokemon_data.json')



def save_pokemon_data(pokemon: List[Pokemon], filename: str):
    data = [poke.get_dict() for poke in pokemon]
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Saved Pokémon data to {filename}")





if __name__ == "__main__":
    main()