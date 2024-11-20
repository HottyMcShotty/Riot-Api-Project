import tkinter as tk
import requests
api_key="RGAPI-0a55a7f4-92b0-4792-8b77-456820b5f6aa"
text="The%20Troglodyte"
id="1111"
api_url="https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"+text+"/"+id+"?api_key="+api_key

#getting the json file, then parsing the json file, and then grabbing the puuid
account=requests.get(api_url)
account=account.json()
puuid=account["puuid"]
matches_url="https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+puuid+"/ids?start=0&count=10&api_key="+api_key
matches_requests=requests.get(matches_url)
matches=matches_requests.json()


for x in range(10):
    match_id=matches[x]
    temp_match="https://americas.api.riotgames.com/lol/match/v5/matches/"+match_id+"?api_key="+api_key
    match_data_call=requests.get(temp_match)
    match_data=match_data_call.json()
    info=match_data['metadata']["participants"].index(puuid)
    kda=match_data["info"]["participants"][info]['challenges']["kda"]
match_id=matches[6]
kda=match_data["info"]["participants"][info]['challenges']["kda"]
print(kda)


def update_label(x):
    if x[0] % 2 == 0:
        label.config(text="Updated!")
    else:
        label.config(text="Original Text")
    x[0] += 1

root = tk.Tk()
root.title("Tkinter Update Example")
root.geometry("300x300")

x = [0]  # Use a list to hold the mutable value

label = tk.Label(root, text="Original Text")
label.grid(row=0, column=0, padx=10, pady=10)

button = tk.Button(root, text="Update Text!", command=lambda: update_label(x))
button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
