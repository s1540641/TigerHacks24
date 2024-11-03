# Dictionary containing crop data
backyard_crops_data = {
    'cool_season': {
        'well-drained': [
            {'name': 'lettuce', 'vitamins': ['A', 'C', 'K']},
            {'name': 'spinach', 'vitamins': ['A', 'C', 'K', 'B9']},
            {'name': 'carrots', 'vitamins': ['A', 'C', 'K', 'B6']}
        ],
        'sandy': [
            {'name': 'radishes', 'vitamins': ['C', 'B6', 'K']},
            {'name': 'peas', 'vitamins': ['A', 'C', 'K']},
            {'name': 'beets', 'vitamins': ['C', 'B9', 'K']}
        ],
        'clay': [
            {'name': 'broccoli', 'vitamins': ['C', 'K', 'B9']},
            {'name': 'cabbage', 'vitamins': ['C', 'K', 'B6']},
            {'name': 'cauliflower', 'vitamins': ['C', 'K', 'B9']}
        ]
    },
    'warm_season': {
        'well-drained': [
            {'name': 'okra', 'vitamins': ['A', 'C', 'K']},
            {'name': 'eggplant', 'vitamins': ['B1', 'B6', 'K']},
            {'name': 'peppers', 'vitamins': ['A', 'C', 'E']}
        ],
        'sandy': [
            {'name': 'tomatoes', 'vitamins': ['A', 'C', 'K']},
            {'name': 'sweet potatoes', 'vitamins': ['A', 'C', 'B6']},
            {'name': 'watermelon', 'vitamins': ['A', 'C', 'B6']}
        ],
        'clay': [
            {'name': 'beans', 'vitamins': ['B9', 'B6', 'C']},
            {'name': 'corn', 'vitamins': ['B1', 'B5', 'C']},
            {'name': 'squash', 'vitamins': ['A', 'C', 'B6']}
        ]
    },
    'winter_season': {
        'well-drained': [
            {'name': 'kale', 'vitamins': ['A', 'C', 'K']},
            {'name': 'brussels sprouts', 'vitamins': ['C', 'K', 'B6']},
            {'name': 'leeks', 'vitamins': ['A', 'C', 'K']}
        ],
        'sandy': [
            {'name': 'garlic', 'vitamins': ['B6', 'C', 'B1']},
            {'name': 'onions', 'vitamins': ['C', 'B6', 'B9']},
            {'name': 'turnips', 'vitamins': ['C', 'B6', 'K']}
        ],
        'clay': [
            {'name': 'collards', 'vitamins': ['A', 'C', 'K']},
            {'name': 'swiss chard', 'vitamins': ['A', 'C', 'K']},
            {'name': 'mustard greens', 'vitamins': ['A', 'C', 'K']}
        ]
    }
}

def match_crops(season, soil_type):
    """
    Match crops based on season and soil type.
    
    Parameters:
    season (str): The growing season ('cool_season', 'warm_season', or 'winter_season')
    soil_type (str): The type of soil ('well-drained', 'sandy', or 'clay')
    
    Returns:
    list: A list of matching crops with their vitamin content
    """
    if season not in backyard_crops_data:
        return "Invalid season selected"
    
    if soil_type not in backyard_crops_data[season]:
        # If soil type not found, default to well-drained
        soil_type = 'well-drained'
    
    return backyard_crops_data[season][soil_type]