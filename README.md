# MTG-Data-Analysis
Code for collecting, cleaning, transforming, and exporting data about Magic: The Gathering cards.

Uses Scryfall's API to access bulk card data of two varieties, and outputs a cleaned CSV and Excel file for the corresponding dataset.  The "Oracle" cards contain an single entry for each unique magic card, and as such includes no card duplicates or treatments. The "Default" cards contain an entry for each printing of each card, including different versions or treatments (foil, full art, etc.).

Many columns and cards are removed from each dataset, for my analysis I was interested specifically in cards from Core Sets and regular Expansion printings.  Cards printed in products like Secret Lair, Masters sets, or Commander Pre-Constructed decks are not included, the final outputted dataset is essentially a list of cards printed into Standard.

Scryfall's API documentation can be found at https://scryfall.com/docs/api
