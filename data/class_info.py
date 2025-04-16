CLASS_INFO = {
    'fabric': {
        'display_name': 'Fabric / Textiles', 'icon': '👕', 'description': 'Includes clothes, shoes, towels, bedding etc.',
        'recyclable': 'Sometimes', 'handling': 'Donate usable items. Check for textile recycling programs for unusable items. Otherwise, general waste.', 'color': '#FFA726'
    },
    'glass': {
        'display_name': 'Glass', 'icon': '🍾', 'description': 'Includes bottles and jars.',
        'recyclable': 'Yes', 'handling': 'Rinse clean. Check local guidelines for color separation (brown, green, clear). Remove lids if required.', 'color': '#29B6F6'
    },
    'non-recyclable': {
        'display_name': 'Non-Recyclable / General Waste', 'icon': '🗑️', 'description': 'Items not easily recyclable. Includes general trash, some plastics, potentially contaminated items, batteries (special disposal!), biological waste (check local compost/waste rules).',
        'recyclable': 'No', 'handling': 'Dispose of in general waste bin. **Check local regulations for hazardous items like batteries.**', 'color': '#EF5350'
    },
    'paper': {
        'display_name': 'Paper & Cardboard', 'icon': '📰', 'description': 'Includes newspaper, magazines, office paper, cardboard boxes.',
        'recyclable': 'Yes', 'handling': 'Keep clean and dry. Flatten cardboard boxes. Check local rules for shredded paper or coated paper.', 'color': '#FFEE58'
    },
    'recyclable-inorganic': {
        'display_name': 'Recyclable Inorganic (Metal/Plastic)', 'icon': '🥫', 'description': 'Includes metal cans (aluminum/steel) and certain types of plastic containers.',
        'recyclable': 'Yes (Varies by type)', 'handling': 'Rinse clean. Check local guidelines for accepted plastic numbers (♻️ symbols) and metal types. Remove lids if required.', 'color': '#66BB6A'
    },
    'unknown': {
        'display_name': 'Unknown / Below Threshold', 'icon': '❓', 'description': 'Could not classify with high confidence or item not recognized.',
        'recyclable': 'Unknown', 'handling': 'Please check local waste disposal guidelines or try a clearer image.', 'color': '#BDBDBD'
    }
}

EXPECTED_CLASS_NAMES = sorted(list(CLASS_INFO.keys() - {'unknown'}))