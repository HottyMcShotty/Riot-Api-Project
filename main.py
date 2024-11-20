import requests
import time
api_key="RGAPI-0a55a7f4-92b0-4792-8b77-456820b5f6aa"
name="The%20Troglodyte"
id="1111"
api_url="https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"+name+"/"+id+"?api_key="+api_key
kda =0
playerList=[None]*10


def obtain():
    totalkda=0
    #getting the json file, then parsing the json file, and then grabbing the puuid
    puuid=requests.get(api_url).json()["puuid"]

    matches_url="https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=5&api_key="+api_key
    lastMatch=requests.get(matches_url).json()[0]
    lastMatchurl="https://americas.api.riotgames.com/lol/match/v5/matches/"+lastMatch+"?api_key="+api_key

    #putting all 10 players from current/lastmatch into a list
    for x in range(10):
        playerList[x]=requests.get(lastMatchurl).json()['metadata']["participants"][x]
        

    #obtaining player stats
    # This doesn't work right now most likely solution is an imbedded for loop to hold the first index of the
    #player list while we iterate through the games then repeat for all players I would note that the best way to
    #store this info will most likely be a dictionary inside of a list.
    for x in range(10):
        ####Iteating through our player list and getting match ids for their last 10 matches
        matches_url="https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+playerList[x]+"/ids?start=0&count=5&api_key="+api_key
        for y in range(5):
            try:
                matches=requests.get(matches_url).json()[y]
                ####
                ####Making a data call for the first player in game and the match that is equal to index x
                temp_match="https://americas.api.riotgames.com/lol/match/v5/matches/"+matches+"?api_key="+api_key
                match_data_call=requests.get(temp_match).json()
                ####Grabbing Data From the Match
                info=match_data_call['metadata']["participants"].index(playerList[x])
                kda =match_data_call["info"]["participants"][info]["challenges"]["kda"]
                temp_name=match_data_call["info"]["participants"][info]["summonerName"]
                time.sleep(1.5)
                print(temp_name,kda)
                totalkda=totalkda+kda
            except:
                print("Well that just happened!")
        print("Average KDA:"+str(totalkda/5))
        ####
obtain()