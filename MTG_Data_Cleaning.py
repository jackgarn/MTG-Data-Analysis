import json
import pandas as pd


def load_and_normalize(filename):
       print("Reading",filename,"...")
       # Gets json object type from the json file, then normalizes from there!
       with open(filename,"r") as file:
              cards_json = json.load(file)
       print("Normalizing Dataset...")
       return pd.json_normalize(cards_json)

def recast_as_number(df,cols):
       #find nulls
       nulls = df.isna()
       # do this for each column
       for i in range(len(cols)):
              for j in df.index:
                     if nulls.loc[j,cols[i]]:  # this is super janky but obnoxious to clean 
                            df.loc[j,cols[i]] = 0
                     if df.loc[j,cols[i]] == '*':
                            df.loc[j,cols[i]] = 0
                     if df.loc[j,cols[i]] == '1+*':
                            df.loc[j,cols[i]] = 1
                     if df.loc[j,cols[i]] == '*+1':
                            df.loc[j,cols[i]] = 1
                     if df.loc[j,cols[i]] == '7-*':
                            df.loc[j,cols[i]] = 0
                     if df.loc[j,cols[i]] == '2+*':
                            df.loc[j,cols[i]] = 2
              df[cols[i]] = df[cols[i]].astype(float)
       return df

def add_types(cards,types):
       for type in types:
              cards[type] = type
              for i in cards.index:
                     if type in cards.loc[i, 'type_line']:
                            cards.loc[i,type] = True
                     else:
                            cards.loc[i,type] = False
       return cards

def add_colors(cards,colors):
       for color in colors:
              cards[color] = color
              #have to ge the right letter to look for 
              if (color == 'Blue'):
                     color_letter = 'U'
              else:
                     color_letter = color[0]

              for i in cards.index:
                     if color_letter in cards.loc[i, 'color_identity']:
                            cards.loc[i,color] = True
                     else:
                            cards.loc[i,color] = False
       return cards
       
def export_df(data):
       print("Exporting to Excel...")
       data.to_excel("Cards_Sheet.xlsx")
       print("Exporting to CSV...")
       data.to_csv("Cards_CSV.csv")
       print("Done!")



card_df = load_and_normalize("Cards.json")

# Remove columns not needed for analysis/data viz
cols_to_drop = ['multiverse_ids', 'mtgo_id', 
       'mtgo_foil_id', 'tcgplayer_id', 'cardmarket_id', 'uri', 'scryfall_uri', 'layout', 'highres_image', 
       'image_status', 'colors', 'oracle_text','mana_cost',
       'games', 'reserved', 'finishes', 
       'oversized', 'promo', 'variation','set_uri', 'set_search_uri', 
       'scryfall_set_uri', 'rulings_uri', 'prints_search_uri', 'digital', 
       'flavor_text', 'card_back_id', 'artist_ids', 
       'illustration_id', 'border_color', 'frame', 'full_art', 'textless', 
       'booster', 'story_spotlight', 'edhrec_rank', 'penny_rank', 'image_uris.small', 
       'image_uris.normal', 'image_uris.large', 'image_uris.png', 'image_uris.art_crop', 'image_uris.border_crop', 
       'legalities.brawl', 'legalities.historicbrawl', 'legalities.alchemy', 
       'legalities.paupercommander', 'legalities.duel', 'legalities.oldschool', 'legalities.premodern','prices.eur', 'prices.eur_foil', 'prices.tix', 
       'related_uris.gatherer', 'related_uris.tcgplayer_infinite_articles', 'related_uris.tcgplayer_infinite_decks', 'related_uris.edhrec', 'all_parts', 
       'promo_types', 'arena_id', 'preview.source', 'preview.source_uri', 'preview.previewed_at', 
       'security_stamp', 'produced_mana', 'watermark', 'frame_effects', 
       'printed_name', 'card_faces', 'tcgplayer_etched_id', 'attraction_lights', 'color_indicator', 
       'life_modifier', 'hand_modifier', 'printed_type_line', 'printed_text', 'content_warning', 
       'flavor_name', 'variation_of','object','oracle_id','lang','keywords','foil','nonfoil',
       'set_id','collector_number','artist','legalities.future','legalities.penny','prices.usd_foil',
       'prices.usd_etched', 'legalities.gladiator']
card_df = card_df.drop(cols_to_drop, axis = 1)

# Cleaning for nicety
card_df['rarity'] = card_df['rarity'].str.title()


# We only want cards from Core sets/Epansions, this removes the othes
print("Retaining only Core Sets and Expansions...")
# Makes two copies of the dataset where all cards we do not want are nulled
expansion_cards = card_df.where(card_df['set_type'] == 'expansion')
core_cards = card_df.where(card_df['set_type'] == 'core')

# Now we drop all the rows that we marked as null from each new dataframe
expansion_cards = expansion_cards.dropna(how = 'all', subset = ['set_type'])
core_cards = core_cards.dropna(how = 'all', subset = ['set_type'])
# The final set of cards that we want is made by combining these two 
card_df = pd.concat([expansion_cards,core_cards], axis = 0, ignore_index=True)

# Re-cast power and toughness as numerical values rather than strings
card_df = recast_as_number(card_df,['power','toughness','prices.usd'])

# Add new column for total P/T
card_df['total_pt'] = 0
for i in card_df.index:
       card_df.loc[i,'total_pt'] = card_df.loc[i,'power'] + card_df.loc[i,'toughness']

# Add a new column for each card type using the typeline column, then dops the old one
print("Adding Types...")
types = ['Legendary',
       'Creature',
       'Planeswalker',
       'Artifact',
       'Enchantment',
       'Instant',
       'Sorcery',
       'Land',
       'Snow']
card_df = add_types(card_df,types)

# Similar to above, but for colors
print("Adding Colors...")
colors = ['White','Blue','Black','Red','Green']
card_df = add_colors(card_df,colors)

# Get rid of the last now-unneeded columns
card_df = card_df.drop(['color_identity','type_line'], axis = 1)

# Makes exported files of clean data
export_df(card_df)