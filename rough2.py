from flask import Flask, request
import json
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
import os 

app = Flask(__name__)

def one(url):
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    
    linkkk = soup.find_all('table', {'class' : 'table'})
    for a_href in linkkk:
      linksss = [item['href'] if item.get('href') is not None else item['src'] for item in a_href.select('[href^="http"], [src^="http"]')]
      return linksss
    #try clause to skip any companies with missing/empty board member tables

    #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
def details(url):
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    team = []
    team_player = []
    player_details = []
    player_information = []
    team_table = soup.find('table', {"class" : "table"})
    #try clause to skip any companies with missing/empty board member tables

    #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
    for row in team_table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 13:
            team.append((cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip(), cols[5].text.strip(), cols[6].text.strip(), cols[7].text.strip(), cols[8].text.strip(),cols[9].text.strip(),cols[10].text.strip(),cols[11].text.strip(),cols[12].text.strip()))
        link = soup.find_all('table', {'class' : 'table'})
        for a_href in link:
            links = [item['href'] if item.get('href') is not None else item['src'] for item in a_href.select('[href^="http"], [src^="http"]') ]
        for b in links:
            page = requests.get(b, verify=False)
            soup = BeautifulSoup(page.content, 'html.parser')
            teamplayer_table = soup.find('table', {"class" : "table"})
            #try clause to skip any companies with missing/empty board member tables
            # #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
            try:
                for row in teamplayer_table.find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) == 6:
                        team_player.append((b, cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip(), cols[5].text.strip()))
            except:
                print("error")
            link1 = soup.find_all('table', {'class' : 'table'})
            for a_href in link1:
                links1 = [item['href'] if item.get('href') is not None else item['src'] for item in a_href.select('[href^="http"], [src^="http"]') ]
                print(links1)
                for i in links1:
                    page = requests.get(i, verify=False)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    playerdetail_table = soup.find('table', {"class" : "table"})
                    #try clause to skip any companies with missing/empty board member tables
                    # #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
                    try:
                        for row in playerdetail_table.find_all('tr'):
                            cols = row.find_all('td')
                            if len(cols) == 5:
                                player_details.append((i, cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip()))
                    except:
                        print("error")
                    link2 = soup.find_all('ul', {'class' : 'navMain'})
                    for a in link2:
                        links2 = [item['href'] if item.get('href') is not None else item['src'] for item in a.select('[href^="https://rugby.statbunker.com/players/getPlayerHistory?player_id="], [src^="http"]') ]
                        print(links2)
                        for c in links2:
                            page3 = requests.get(c, verify=False)
                            soup3 = BeautifulSoup(page3.content, 'html.parser')
                            playerinformation_table = soup3.find('table', {"class" : "table"})
                            #try clause to skip any companies with missing/empty board member tables
                            # #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
                            try:
                                for row in playerinformation_table.find_all('tr'):
                                    cols = row.find_all('td')
                                    if len(cols) == 6:
                                        player_information.append((c, cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip(), cols[5].text.strip()))
                            except:
                                print("error")
    
    
    team_array = np.asarray(team)
    team_df = pd.DataFrame(team_array)
    team_df.columns = ['club_name', 'matches_played', 'yellow_card','redyellow_card', 'red_card', 'yellowcard_permatch', 'first_half', 'second_half', 'home', 'away', 'match_won', 'match_draw', 'match_loss']
    for ss in team_table.find_all('caption'):
        season = ss.findAll('h1')[0].text.strip()
    team_df['Season'] = pd.Series([season for x in range(len(team_df.index))])
    team_df['club_URL']=one(url)
    cols = team_df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    team_df = team_df[cols] 
    team_result = team_df.to_json(orient="split")
    parsed1 = json.loads(team_result)
    json.dumps(parsed1, indent=4)
    team_df.to_csv('team1.csv')


    tempdf = team_df[['Season', 'club_name', 'club_URL']]

    teamplayer_array = np.asarray(team_player)
    teamplayer_df = pd.DataFrame(teamplayer_array)
    teamplayer_df.columns = ['club_URL', 'points', 'player_name', 'tries', 'conversions', 'penalties', 'drop_goals']
    teamplayer_df["teamurl_dummy"]=teamplayer_df["club_URL"]
    teamplayer_df[['getteamapi','Comp_Id', 'Club_Id']] = teamplayer_df.teamurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    teamplayer_df.drop(["teamurl_dummy"], axis=1, inplace=True)
    teamplayer_df.drop(["getteamapi"], axis=1, inplace=True)
    teamplayer_df['Comp_Id'] = teamplayer_df['Comp_Id'].str.split('&').str[0]
    teamplayerfinal_df = pd.merge(tempdf, teamplayer_df, on = "club_URL", how='inner')
    teamplayer_result = teamplayerfinal_df.to_json(orient="split")
    parsed2 = json.loads(teamplayer_result)
    json.dumps(parsed2, indent=4)
    teamplayerfinal_df.to_csv('player1.csv')

    playerdetails_array = np.asarray(player_details)
    playerdetails_df = pd.DataFrame(playerdetails_array)
    print(playerdetails_df)
    playerdetails_df.columns = ['player_URL', 'player_name', 'height', 'nationality', 'dateofbirth', 'birth_country']
    playerdetails_df["playerurl_dummy"]=playerdetails_df["player_URL"]
    playerdetails_df[['getplayerapi','Player_Id']] = playerdetails_df.playerurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    playerdetails_df.drop(["playerurl_dummy"], axis=1, inplace=True)
    playerdetails_df.drop(["getplayerapi"], axis=1, inplace=True)

    playerinformation_array = np.asarray(player_information)
    playerinformation_df = pd.DataFrame(playerinformation_array)
    playerinformation_df.columns = ['PlayerDetails_URL', 'club', 'country', 'position', 'NO', 'from', 'to']
    playerinformation_df["playerdetailsurl_dummy"]=playerinformation_df["PlayerDetails_URL"]
    playerinformation_df[['getplayerdetailsapi','Player_Id']] = playerinformation_df.playerdetailsurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    playerinformation_df.drop(["playerdetailsurl_dummy"], axis=1, inplace=True)
    playerinformation_df.drop(["getplayerdetailsapi"], axis=1, inplace=True)

    playerdetailsfinal_df = pd.merge(playerdetails_df, playerinformation_df, on = "Player_Id", how='inner')

    pdetails_result = playerdetailsfinal_df.to_json(orient="split")
    parsed3 = json.loads(pdetails_result)
    json.dumps(parsed3, indent=4)
    playerdetailsfinal_df.to_csv('player_details1.csv')

    result = {"data": {"Team_Names": team_df.to_json(orient="split"), "Team_Player": teamplayerfinal_df.to_json(orient="split"), "Player_Details": playerdetailsfinal_df.to_json(orient="split")}}
    #result = str(df.to_json(orient="split"), df1.to_json(orient="split"), merged_Frame.to_json(orient="split"))

    if (len(result) > 0):
            return True, result
    else:
        return False, None

@app.route('/', methods=['GET'])
def index():
    """
    Base path to check if the service is running
    """
    return (str('Service is running')), 200



@app.route('/scraper', methods=['GET'])
def run_scraper():
    url=request.args['url']
    #base_url = request.args['base_url']
    #comp_id = request.args['comp_id']
    #match_id = request.args['match_id']
    #date = request.args['date']
    #url = base_url+"?comp_id="+comp_id+"&match_id="+match_id+"&date="+date

    print(url)
    
    status, output = details(url)
    
    if status:
        return (output), 200
    else:
        return ("ERROR"), 500

@app.errorhandler(500)
def server_error(e):
    """
    Handling errors with 500 error. 
    If more specific error handling is required, 
    it should be custom handles with each endpoint
    """
    
    #logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    """
    Running the Flask application in local.
    Set debug=True for local testing and False for deployments
    """
    app.run(host='0.0.0.0', port=5000, debug = True)  #PORT should 5000 as our cluster by default listen on 5000