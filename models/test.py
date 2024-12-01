import json
from players import Player

qifia = Player('aqif','kapertoni','01-01-2000')
afrimi = Player('afrim','tahipi','11-11-1999')
players = [qifia.serialize_players(),afrimi.serialize_players()]

# create the data in json file
with open('json_data/players.json', 'w') as fp:
    json.dump(players,fp,indent=2)

# reading the json datas
with open("json_data/players.json", "r") as f:
    players = json.load(f)


print(players)
'''
players_dict["player3"] = {
    "first_name": "Afrim",
    "last_nam": "Tahipi",
    "date_of_birth": "12/02/1960"
}


new_player = json.dumps(players_dict)
with open("players.json","w") as nf:
    nf.write(new_player)
'''
