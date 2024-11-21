import requests
import time
import tkinter as tk
API_KEY="RGAPI-21e631a4-0df4-479b-8636-db9b18f324cb"
name="The%20Troglodyte"
id="1111"
api_url="https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"+name+"/"+id+"?api_key="+API_KEY
kda =0
playerList=[None]*10


def obtain():
    totalkda=0
    global playerInfo
    playerInfo=[]
    #getting the json file, then parsing the json file, and then grabbing the puuid
    puuid=requests.get(api_url).json()["puuid"]

    matches_url="https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=5&api_key="+API_KEY
    lastMatch=requests.get(matches_url).json()[0]
    lastMatchurl="https://americas.api.riotgames.com/lol/match/v5/matches/"+lastMatch+"?api_key="+API_KEY

    #putting all 10 players from current/lastmatch into a list
    for x in range(10):
        playerList[x]=requests.get(lastMatchurl).json()['metadata']["participants"][x]
        

    #obtaining player stats
    # This doesn't work right now most likely solution is an imbedded for loop to hold the first index of the
    #player list while we iterate through the games then repeat for all players I would note that the best way to
    #store this info will most likely be a dictionary inside of a list.
    for x in range(10):
        
        ####Iteating through our player list and getting match ids for their last 10 matches
        matches_url="https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+playerList[x]+"/ids?start=0&count=5&api_key="+API_KEY
        for y in range(1):
            try:
                matches=requests.get(matches_url).json()[y]
                ####
                ####Making a data call for the first player in game and the match that is equal to index x
                temp_match="https://americas.api.riotgames.com/lol/match/v5/matches/"+matches+"?api_key="+API_KEY
                match_data_call=requests.get(temp_match).json()
                ####Grabbing Data From the Match
                info=match_data_call['metadata']["participants"].index(playerList[x])
                kda =match_data_call["info"]["participants"][info]["challenges"]["kda"]
                time.sleep(1.5)
                totalkda=totalkda+kda
                
            except Exception as e:
                print(f"An error occurred: {e}")
        print(str((1+x)*10)+"% Done!")
        temp_name=match_data_call["info"]["participants"][info]["summonerName"]
        playerInfo.append({"Name":temp_name,"KDA":round((totalkda/5),2)})
        totalkda=0
        ####


def gui():
    obtain()
    root = tk.Tk()
    root.title("Player Stats")
    root.attributes("-topmost", True)

    # Create a header for the table
    header_name = tk.Label(root, text="Name", font=("Arial", 12, "bold"))
    header_name.grid(row=0, column=0, padx=10, pady=5)

    header_kda = tk.Label(root, text="KDA", font=("Arial", 12, "bold"))
    header_kda.grid(row=0, column=1, padx=10, pady=5)

    # Populate the table with data
    for i in range(10):
        name_label = tk.Label(root, text=playerInfo[i]["Name"],fg=("red"), font=("Arial", 10))
        name_label.grid(row=i + 1, column=0, padx=10, pady=5)

        kda_label = tk.Label(root, text=str(playerInfo[i]["KDA"]), font=("Arial", 10))
        kda_label.grid(row=i + 1, column=1, padx=10, pady=5)

    # Run the application
    root.mainloop()
gui()