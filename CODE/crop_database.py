# Logic for matching crops with user input

#this is all the possible crop options that the user can get
backyard_crops_data = {
    'cool_season': {
        'well-drained': [
            {'name':'lettuce', 'vitamins': ['A', 'C', 'K']},
            {'name': 'Spinach', 'vitamins': ['A', 'C', 'K', 'B9']},
            {'name': 'Carrots', 'vitamins': ['A', 'C', 'K', 'B6']},
        ]
    },
   'warm_season': {
        'well-drained': [
            {'name': 'okra', 'vitamins': ['A', 'C', 'K']},
            {'name': 'eggplant', 'vitamins': ['B1', 'B6', 'K']},
            {'name': 'peppers', 'vitamins': ['A', 'C', 'E']}
        ]
   },
    'winter_season':{
        'well-drained':[
        {'name': 'kale', 'vitamins': ['A', 'C', 'K']},
        {'name': 'brussels sprouts', 'vitamins': ['C', 'K', 'B6']},
        {'name': 'leeks', 'vitamins': ['A', 'C', 'K']}
        ]
    },
}
#
def match_crops(season, soil_condition):
    try:
        crops = backyard_crops_data[season][soil_condition]
        return crops
    except KeyError:
        return "No crops available for the specified season and soil condition."
