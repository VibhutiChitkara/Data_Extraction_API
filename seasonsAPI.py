from cgitb import html
from flask import Flask, request
import json
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
import os 
import lxml
from lxml import html

app = Flask(__name__)

def one(url):
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    
    link= soup.find_all('table', {'class' : 'table'})
    for a_href in link:
      club_link = [item['href'] if item.get('href') is not None else item['src'] for item in a_href.select('[href^="http"], [src^="http"]')]
      return club_link
    #try clause to skip any companies with missing/empty board member tables

    #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)

def stats(url):
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    team = []
    Club = []
    stats_df = pd.DataFrame()
    stats_dict={}
    temp = ""
    team_table = soup.find('table', {"class" : "table"})
    #try clause to skip any companies with missing/empty board member tables

    #loop through table, grab each of the 4 columns shown (try one of the links yourself to see the layout)
    for row in team_table.find_all('tr'):
        link = soup.find_all('table', {'class' : 'table'})
        for a_href in link:
            links = [item['href'] if item.get('href') is not None else item['src'] for item in a_href.select('[href^="http"], [src^="http"]') ]
        for b in links:
            page = requests.get(b, verify=False)
            soup = BeautifulSoup(page.content, 'html.parser')
            link1 = soup.find_all('table', {'class' : 'table'})
            for a_href in link1:
                links1 = [item['href'] if item.get('href') is not None else item['src'] for item in a_href.select('[href^="http"], [src^="http"]') ]
                print(links1)
                for i in links1:
                    page = requests.get(i, verify=False)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    link2 = soup.find_all('ul', {'class' : 'navMain'})
                    for a in link2:
                        links2 = [item['href'] if item.get('href') is not None else item['src'] for item in a.select('[href^="https://rugby.statbunker.com/players/getPlayerStats?player_id="], [src^="http"]') ]
                        print(links2)
                        for d in links2:
                            page4 = requests.get(d, verify=False)
                            soup4 = BeautifulSoup(page4.content, 'html.parser')
                            html = requests.get(d, verify=False).content
                            df_list1 = pd.read_html(html)
                            stats_dict["PlayerStats_URL"]=d
                            products = soup4.findAll('caption', {'class':'genericTitle'})
                            clubs = soup4.findAll('ul', {'class':'breadcrumb'})
                            for product in products:
                                name = product.findAll('h1')[0].text.strip()
                                stats_dict["player_name"]=name
                            clubs = soup4.findAll('ul', {'class':'breadcrumb'})
                            for club in clubs:
                                team = club.findAll('li')
                                for value in team:
                                    clubname = value.get_text()
                                    Club.append(clubname)
                                    print(Club)
                                for aa in df_list1:
                                    for i,row in aa.iterrows():
                                        if i==0 or i ==6 or i==11:
                                            temp=row[0]
                                        else:
                                            if not (pd.isna(row[0]) and pd.isna(row[1])):
                                                stats_dict[temp+"_"+row[0]]=row[1] if not pd.isna(row[1]) else "NaN"
                                            if not (pd.isna(row[2]) and pd.isna(row[3])):
                                                stats_dict[temp+"_"+row[2]]=row[3] if not pd.isna(row[3]) else "NaN"
                                    print(stats_dict)
                                    stats_df = stats_df.append(stats_dict, ignore_index=True)
                                    print(stats_df) 
            
    
    stats_df['Club_Name']=Club
    last_column = stats_df.pop('Club_Name')
    stats_df.insert(2, 'Club_Name', last_column)
    stats_df["playerstatsurl_dummy"]=stats_df["PlayerStats_URL"]
    stats_df[['getplayerstatsapi','Player_Id']] = stats_df.playerstatsurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    stats_df.drop(["playerstatsurl_dummy"], axis=1, inplace=True)
    stats_df.drop(["getplayerstatsapi"], axis=1, inplace=True)

    stats_result = stats_df.to_json(orient="split")
    parsed3 = json.loads(stats_result)
    json.dumps(parsed3, indent=4)
    stats_df.to_csv('stats2.csv')
    return stats_result

def details(url):
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    team = []
    team_player = []
    player_details = []
    player_information = []
    player_international = []
    PlayerLink = []
    stats_df = pd.DataFrame()
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
                    playerlinks = [item['href'] if item.get('href') is not None else item['src'] for item in row.select('[href^="http"], [src^="http"]') ]
                    cols = row.find_all('td')
                    if len(cols) == 6:
                        team_player.append((b, playerlinks, cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip(), cols[5].text.strip()))
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
                            playerinformation_table = soup3.find_all('table', {"class" : "table"})
                            for obj in playerinformation_table:
                                for row in obj.find_all('tr'):
                                    clublinks = [item['href'] if item.get('href') is not None else item['src'] for item in row.select('[href^="http"], [src^="http"]') ]
                                    #print("links", links22)
                                    cols = row.find_all('td')
                                    #print(len(cols))
                                    if len(cols) == 6:
                                        player_information.append((c, clublinks, cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip(), cols[4].text.strip(), cols[5].text.strip()))
                                    if len(cols) == 4:
                                        player_international.append((c, clublinks, cols[0].text.strip(), cols[1].text.strip(), cols[2].text.strip(), cols[3].text.strip()))

    team_array = np.asarray(team)
    team_df = pd.DataFrame(team_array)
    team_df.columns = ['club_name', 'matches_played', 'yellow_card','redyellow_card', 'red_card', 'yellowcard_permatch', 'first_half', 'second_half', 'home', 'away', 'match_won', 'match_draw', 'match_loss']
    for ss in team_table.find_all('caption'):
        season = ss.findAll('h1')[0].text.strip()
    team_df['Season'] = pd.Series([season for x in range(len(team_df.index))])
    team_df[['season_number', 'major', 'league', 'rugby', 'clubs', 'discipline']] = team_df['Season'].str.split(' ', expand=True)
    team_df['competition_name'] = team_df[['major', 'league', 'rugby']].apply(lambda x: ' '.join(x), axis=1)
    team_df.drop(['Season', 'major', 'league', 'rugby', 'clubs', 'discipline'], axis = 1, inplace = True)
    team_df['club_URL']=one(url)
    cols = team_df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    team_df = team_df[cols] 
    team_df["teamurl_dummy"]=team_df["club_URL"]
    team_df[['getteamapi','Comp_Id', 'Club_Id']] = team_df.teamurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    team_df.drop(["teamurl_dummy"], axis=1, inplace=True)
    team_df.drop(["getteamapi"], axis=1, inplace=True)
    team_df['Comp_Id'] = team_df['Comp_Id'].str.split('&').str[0]
    team_result = team_df.to_json(orient="split")
    parsed1 = json.loads(team_result)
    json.dumps(parsed1, indent=4)
    team_df.to_csv('team2.csv')


    tempdf = team_df[['season_number', 'competition_name', 'club_name', 'club_URL']]

    teamplayer_array = np.asarray(team_player)
    teamplayer_df = pd.DataFrame(teamplayer_array)
    teamplayer_df.columns = ['club_URL', 'playerurl' ,'points', 'player_name', 'tries', 'conversions', 'penalties', 'drop_goals']
    teamplayer_df["teamurl_dummy"]=teamplayer_df["club_URL"]
    teamplayer_df[['getteamapi','Comp_Id', 'Club_Id']] = teamplayer_df.teamurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    teamplayer_df.drop(["teamurl_dummy"], axis=1, inplace=True)
    teamplayer_df.drop(["getteamapi"], axis=1, inplace=True)
    teamplayer_df['Comp_Id'] = teamplayer_df['Comp_Id'].str.split('&').str[0]
    #teamplayer_df["playerurl"]=PlayerLink
    teamplayer_df["playerurl_dummy"]=teamplayer_df["playerurl"]
    teamplayer_df[['getplayerapi','Player_Id']] = teamplayer_df.playerurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    teamplayer_df.drop(["playerurl_dummy"], axis=1, inplace=True)
    teamplayer_df.drop(["getplayerapi"], axis=1, inplace=True)
    teamplayerfinal_df = pd.merge(tempdf, teamplayer_df, on = "club_URL", how='inner')
    teamplayer_result = teamplayerfinal_df.to_json(orient="split")
    parsed2 = json.loads(teamplayer_result)
    json.dumps(parsed2, indent=4)
    teamplayerfinal_df.to_csv('player2.csv')

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
    playerinformation_df.columns = ['PlayerDetails_URL', 'ClubDetails_URL', 'Club_Name', 'country', 'position', 'NO', 'from', 'to']
    playerinformation_df["playerdetailsurl_dummy"]=playerinformation_df["PlayerDetails_URL"]
    playerinformation_df[['getplayerdetailsapi','Player_Id']] = playerinformation_df.playerdetailsurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    playerinformation_df.drop(["playerdetailsurl_dummy"], axis=1, inplace=True)
    playerinformation_df.drop(["getplayerdetailsapi"], axis=1, inplace=True)
    playerinformation_df["clubdetailsurl_dummy"]=playerinformation_df["ClubDetails_URL"]
    playerinformation_df[['getclubdetailsapi','Club_Id']] = playerinformation_df.clubdetailsurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    playerinformation_df.drop(["clubdetailsurl_dummy"], axis=1, inplace=True)
    playerinformation_df.drop(["getclubdetailsapi"], axis=1, inplace=True)

    playerinternational_array = np.asarray(player_international)
    playerinternational_df = pd.DataFrame(playerinternational_array)
    playerinternational_df.columns = ['PlayerDetails_URL', 'ClubDetails_URL', 'Club_Name', 'position', 'from', 'to']
    playerinternational_df["playerdetailsurl_dummy"]=playerinternational_df["PlayerDetails_URL"]
    playerinternational_df[['getplayerdetailsapi','Player_Id']] = playerinternational_df.playerdetailsurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    playerinternational_df.drop(["playerdetailsurl_dummy"], axis=1, inplace=True)
    playerinternational_df.drop(["getplayerdetailsapi"], axis=1, inplace=True)
    playerinternational_df["clubdetailsurl_dummy"]=playerinternational_df["ClubDetails_URL"]
    playerinternational_df[['getclubdetailsapi','Club_Id']] = playerinternational_df.clubdetailsurl_dummy.apply(
        lambda x: pd.Series(str(x).split("=")))
    playerinternational_df.drop(["clubdetailsurl_dummy"], axis=1, inplace=True)
    playerinternational_df.drop(["getclubdetailsapi"], axis=1, inplace=True)

    playerhistory_df = pd.DataFrame()
    playerhistory_df = playerhistory_df.append(playerinformation_df)
    playerhistory_df = playerhistory_df.append(playerinternational_df)


    playerdetailsfinal_df = pd.merge(playerdetails_df, playerhistory_df, on = "Player_Id", how='inner')

    pdetails_result = playerdetailsfinal_df.to_json(orient="split")
    parsed3 = json.loads(pdetails_result)
    json.dumps(parsed3, indent=4)
    playerdetailsfinal_df.to_csv('player_details2.csv')


    result = {"data": {"Team_Names": team_df.to_json(orient="split"), "Team_Player": teamplayerfinal_df.to_json(orient="split"), "Player_Details": playerdetailsfinal_df.to_json(orient="split"), "Player_Stats": stats(url)}}
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
    #url=request.args['url']
    base_url = "https://rugby.statbunker.com/competitions/ClubBookings"
    comp_id = request.args['comp_id']
    #match_id = request.args['match_id']
    #date = request.args['date']
    url = base_url+"?comp_id="+comp_id

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
    app.run(host='0.0.0.0', port=5002, debug = True)  #PORT should 5000 as our cluster by default listen on 5000