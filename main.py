from flask import Flask, request
import json
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
import os 

app = Flask(__name__)

def details(url):
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    team = []
    team_player = []
    player_details = []
    player_information = []
    officer_table = soup.find('table', {"class" : "table"})
    #try clause to skip any companies with missing/empty board member tables

    #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
    for row in officer_table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 13:
            team.append((cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip(), cols[5].text.strip(), cols[6].text.strip(), cols[7].text.strip(), cols[8].text.strip(),cols[9].text.strip(),cols[10].text.strip(),cols[11].text.strip(),cols[12].text.strip()))
        link = soup.find_all('table', {'class' : 'table'})
        for a_href in link:
            links = [item['href'] if item.get('href') is not None else item['src'] for item in a_href.select('[href^="http"], [src^="http"]') ]
        for b in links:
            page = requests.get(b, verify=False)
            soup = BeautifulSoup(page.content, 'html.parser')
            officer_table = soup.find('table', {"class" : "table"})
            #try clause to skip any companies with missing/empty board member tables
            # #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
            try:
                for row in officer_table.find_all('tr'):
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
                    officer_table = soup.find('table', {"class" : "table"})
                    #try clause to skip any companies with missing/empty board member tables
                    # #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
                    try:
                        for row in officer_table.find_all('tr'):
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
                            officer_table = soup3.find('table', {"class" : "table"})
                            #try clause to skip any companies with missing/empty board member tables
                            # #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
                            try:
                                for row in officer_table.find_all('tr'):
                                    cols = row.find_all('td')
                                    if len(cols) == 6:
                                        player_information.append((c, cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip(), cols[5].text.strip()))
                            except:
                                print("error")
    
    board_array = np.asarray(team)
    df = pd.DataFrame(board_array)
    df.columns = ['club', 'matches_played', 'yellow_card','redyellow_card', 'red_card', 'yellowcard_permatch', 'first_half', 'second_half', 'home', 'away', 'match_won', 'match_draw', 'match_loss']
    df['season_number'] = pd.Series(["2021" for x in range(len(df.index))])
    df['competition_name'] = pd.Series(["Major League Rugby" for x in range(len(df.index))])
    cols = df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    df = df[cols] 
    result1 = df.to_json(orient="split")
    parsed1 = json.loads(result1)
    json.dumps(parsed1, indent=4)
    df.to_csv('team.csv')


    board_array1 = np.asarray(team_player)
    df1 = pd.DataFrame(board_array1)
    df1.columns = ['club_URL', 'points', 'player_name', 'tries', 'conversions', 'penalties', 'drop_goals']
    df1['season_number'] = pd.Series(["2021" for x in range(len(df1.index))])
    df1['competition_name'] = pd.Series(["Major League Rugby" for x in range(len(df1.index))])
    df1['club_name'] = ""
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=683','club_name'] = 'New England Free Jacks'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=686','club_name'] = 'Rugby United New York'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=684','club_name'] = 'New Orleans Gold'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=680','club_name'] = 'San Diego Legions'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=677','club_name'] = 'Austin Gilgronis'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=679','club_name'] = 'Houston Sabercats'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=685','club_name'] = 'Old Glory DC'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=728','club_name'] = 'LA Giltinis'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=687','club_name'] = 'Rugby ATL'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=682','club_name'] = 'Utah Warriors'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=681','club_name'] = 'Seattle Seawolves'
    df1.loc[df1['club_URL'] == 'https://rugby.statbunker.com/competitions/LeadingTopScorers?comp_id=652&club_id=688','club_name'] = 'Toronto Arrows'
    df1['club_name'].fillna('Other', inplace=True)
    cols1 = df1.columns.tolist()
    cols1 = cols1[-3:] + cols1[:-3]
    df1 = df1[cols1]
    df1["teamurl_dummy"]=df1["club_URL"]
    df1[['getteamapi','Comp_Id', 'Club_Id']] = df1.teamurl_dummy.apply(
    lambda x: pd.Series(str(x).split("=")))
    df1.drop(["teamurl_dummy"], axis=1, inplace=True)
    df1.drop(["getteamapi"], axis=1, inplace=True)
    df1['Comp_Id'] = df1['Comp_Id'].str.split('&').str[0]
    result2 = df1.to_json(orient="split")
    parsed2 = json.loads(result2)
    json.dumps(parsed2, indent=4)
    df1.to_csv('player.csv')

    board_array2 = np.asarray(player_details)
    df2 = pd.DataFrame(board_array2)
    df2.columns = ['player_URL', 'player_name', 'height', 'nationality', 'dateofbirth', 'birth_country']
    df2["playerurl_dummy"]=df2["player_URL"]
    df2[['getplayerapi','Player_Id']] = df2.playerurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    df2.drop(["playerurl_dummy"], axis=1, inplace=True)
    df2.drop(["getplayerapi"], axis=1, inplace=True)

    board_array3 = np.asarray(player_information)
    df3 = pd.DataFrame(board_array3)
    df3.columns = ['PlayerDetails_URL', 'club', 'country', 'position', 'NO', 'from', 'to']
    df3["playerdetailsurl_dummy"]=df3["PlayerDetails_URL"]
    df3[['getplayerdetailsapi','Player_Id']] = df3.playerdetailsurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    df3.drop(["playerdetailsurl_dummy"], axis=1, inplace=True)
    df3.drop(["getplayerdetailsapi"], axis=1, inplace=True)

    merged_Frame = pd.merge(df2, df3, on = "Player_Id", how='inner')

    result3 = merged_Frame.to_json(orient="split")
    parsed3 = json.loads(result3)
    json.dumps(parsed3, indent=4)
    merged_Frame.to_csv('player_details.csv')

    result = {"data": {"Team_Names": df.to_json(orient="split"), "Team_Player": df1.to_json(orient="split"), "Player_Details": merged_Frame.to_json(orient="split")}}
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

    


