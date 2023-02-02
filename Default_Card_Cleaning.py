import requests
import json
import pandas as pd

def keep_core_and_expansion(cards):
       
       # Makes two copies of the dataset where all cards we do not want are nulled
       expansion_cards = cards.where(cards['set_type'] == 'expansion')
       core_cards = cards.where(cards['set_type'] == 'core')

       # Now we drop all the rows that we marked as null from each new dataframe
       expansion_cards = expansion_cards.dropna(how = 'all', subset = ['set_type'])
       core_cards = core_cards.dropna(how = 'all', subset = ['set_type'])

       # The final set of cards that we want is made by combining these two 
       cards = pd.concat([expansion_cards,core_cards], axis = 0, ignore_index=True)

       return cards

def recast_as_number(df,cols):
       #find nulls to replace with 0, otherwise we can't cast them
       nulls = df.isna()
       # do this for each column
       for i in range(len(cols)):
              for j in df.index:
                     #some of the cards have non-numeric symbols, this deals with each 
                     if nulls.loc[j,cols[i]]: 
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
       # I chose to make a new column for each type a card can be, 
       # this was the best way I could think of to easily deal with multi-typed cards
       for type in types:
              cards[type] = type
              for i in cards.index:
                     if type in cards.loc[i, 'type_line']:
                            cards.loc[i,type] = True
                     else:
                            cards.loc[i,type] = False

       #dont need this column anymore
       cards = cards.drop(['type_line'], axis = 1)

       return cards

def add_colors(cards,colors):

       # A card's colors are stored in an array, so if this array is empty the
       # card has no color, and is multicolored if it is longer than 1
       for i in cards.index:
              if len(cards.loc[i, 'color_identity']) > 1:
                     cards.loc[i, 'color_identity'] = 'Multicolor'
              elif len(cards.loc[i, 'color_identity']) < 1:
                     cards.loc[i, 'color_identity'] = 'Colorless'

       # Replaces the color identity array with the color of the card
       for color in colors:
              cards[color] = color
              #have to ge the right letter to look for 
              if (color == 'Blue'):
                     color_letter = 'U'
              else:
                     color_letter = color[0]

              for i in cards.index:
                     if (color_letter in cards.loc[i, 'color_identity']) and (cards.loc[i, 'color_identity'] != 'Blue'):
                            cards.loc[i, 'color_identity'] = color

       return cards
       
def price_range(df):
       # I have not been able to figure out how to apply a function like this more
       # efficiently, so we iterate
       df['price_range'] = ''
       for i in df.index:
              price = df.loc[i,'prices.usd']
              if (price < 1):
                     df.loc[i,'price_range'] = '$0.00 - $0.99'
              elif (price >= 1 and price < 2):
                     df.loc[i,'price_range'] = '$1.00 - $1.99'
              elif (price >= 2 and price < 5):
                     df.loc[i,'price_range'] = '$2.00 - $4.99'
              elif (price >=5 and price < 10):
                     df.loc[i,'price_range'] = '$5.00 - $10.00'
              else:
                     df.loc[i,'price_range'] = '$10.00 +'
       return df

def export_df(data):
       data.to_excel("Default_Cards_Sheet.xlsx",index=False)
       data.to_csv("Default_Cards_CSV.csv",index=False)


# Gets Default cards from Scryfall and puts them in a pandas dataframe
response = requests.get('https://data.scryfall.io/default-cards/default-cards-20230202100501.json')
card_df = pd.json_normalize(response.json())

# Remove columns not needed for analysis/data viz
cols_to_drop = ['multiverse_ids', 'mtgo_id', 'id',
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
       'card_faces', 'tcgplayer_etched_id', 'attraction_lights', 'color_indicator', 
       'life_modifier', 'hand_modifier', 'content_warning', 
       'object','lang','keywords','foil','nonfoil',
       'set_id','collector_number','artist','legalities.future','legalities.penny','prices.usd_foil',
       'prices.usd_etched', 'legalities.gladiator']
card_df = card_df.drop(cols_to_drop, axis = 1)

# We only want cards from Core sets/Epansions, this removes the othes
card_df = keep_core_and_expansion(card_df)

# Re-cast power and toughness as numerical values rather than strings
card_df = recast_as_number(card_df,['power','toughness','prices.usd'])

# Add new column for total P/T
card_df['total_pt'] = card_df['power'] + card_df['toughness']

# Changes color_identity from array to the single color, colorless, or multicolor
colors = ['White','Blue','Black','Red','Green']
card_df = add_colors(card_df,colors)

# Add a new column for each card type using the typeline column, then drops the old one
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

# Adds a price range column I used for data viz/filtering
card_df = price_range(card_df)

# Cleaning for nicety
card_df['rarity'] = card_df['rarity'].str.title()

# Makes exported files of clean data
export_df(card_df)
