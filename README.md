# MTG Data Analysis
Code for collecting, cleaning, transforming, and exporting data about Magic: The Gathering cards.

Uses Scryfall's API to access bulk card data of two varieties, and outputs a cleaned CSV and Excel file for the corresponding dataset.  The "Oracle" cards contain an single entry for each unique magic card, and as such includes no card duplicates or treatments. The "Default" cards contain an entry for each printing of each card, including different versions or treatments (foil, full art, etc.).

Many columns and cards are removed from each dataset, for my analysis I was interested specifically in cards from Core Sets and regular Expansion printings.  Cards printed in products like Secret Lair, Masters sets, or Commander Pre-Constructed decks are not included, the final outputted dataset is essentially a list of cards printed into Standard.

The interactive visualization I developed to explore which Core and Expansion sets printed the most valuable cards can be found at on [Tableau Public](https://public.tableau.com/app/profile/jack.garn/viz/MTGCardCosts/Dashboard2).

I am currently developing a second visualization that outlines how the various card treatments an Oracle ID might receive impacts a card's price using a modified version of this dataset that should be updated here soon.

Scryfall's API documentation can be found at https://scryfall.com/docs/api
