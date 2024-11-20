import requests
api_key="RGAPI-0a55a7f4-92b0-4792-8b77-456820b5f6aa"
name="The%20Troglodyte"
id="1111"
api_url="https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"+name+"/"+id+"?api_key="+api_key

#getting the json file, then parsing the json file, and then grabbing the puuid
puuid=requests.get(api_url).json()["puuid"]

matches_url="https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=10&api_key="+api_key
matches=requests.get(matches_url).json()[0]



temp_match="https://americas.api.riotgames.com/lol/match/v5/matches/"+matches+"?api_key="+api_key
match_data_call=requests.get(temp_match).json()
info=match_data_call['metadata']["participants"]
print(matches)