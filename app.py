from flask import Flask, request,jsonify, render_template
import requests
from pandas._libs import json
import datetime
from decimal import Decimal

app = Flask(__name__)

#default route when application firstly started.
@app.route("/")
def index():
    return render_template("app.html")

#function to get rank and points based on teamId
def getRankAndPointsbyTeamId(teamId):

    url_team_rankings = "https://delivery.chalk247.com/team_rankings/NFL.json?api_key=74db8efa2a6db279393b433d97c2bc843f8e32b0"
    resp_team_rankings = requests.get(url=url_team_rankings)
    data_team_rankings = resp_team_rankings.json();

    team_rankings_result_data= data_team_rankings['results']['data'];
    for team in team_rankings_result_data:
        if(team['team_id']==teamId):
            adjusted_points= Decimal(float(team['adjusted_points']))
            return team['rank'], str(round(adjusted_points, 2))

#function to get date and time from datetime.
def getDateAndTime(dateString):

    date_time_obj = datetime.datetime.strptime(dateString, '%Y-%m-%d %H:%M')
    date=date_time_obj.date()
    time=date_time_obj.time()
    return date.strftime("%d-%m-%Y"),time.strftime("%H:%M")

#function to get eventData based on startDate and endDate
@app.route('/getEventJsonData', methods=['GET', 'POST'])
def getEventJsonData():

    start_date = request.args['startDate'];
    end_Date = request.args['endDate'];
    base_url="https://delivery.chalk247.com/scoreboard/";
    league_name="NFL";
    api_key="74db8efa2a6db279393b433d97c2bc843f8e32b0";

    scoreboard_url=base_url+league_name+'/'+start_date+'/'+end_Date+'.json?'+"api_key="+api_key;
    scoreboard_resp = requests.get(url=scoreboard_url);
    scoreboard_data = scoreboard_resp.json();
    results=scoreboard_data['results'];

    event_list=[]
    for i in results:
        results_data=(scoreboard_data['results'][i]);
        if type(results_data) is dict:
            event_data=results_data.get('data');
            for i in event_data:
                event_dict = {}
                event=event_data.get(i);
                event_dict['event_id']=event.get('event_id');
                event_dict['event_date'],event_dict['event_time']=getDateAndTime(event.get('event_date'));
                event_dict['away_team_id'] = event.get('away_team_id');
                event_dict['away_nick_name'] = event.get('away_nick_name');
                event_dict['away_city'] = event.get('away_city');
                event_dict['away_rank'], event_dict['away_rank_points'] = getRankAndPointsbyTeamId(event.get('away_team_id'));
                event_dict['home_team_id'] = event.get('home_team_id');
                event_dict['home_nick_name'] = event.get('home_nick_name');
                event_dict['home_city'] = event.get('home_city');
                event_dict['home_rank'],event_dict['home_rank_points']=getRankAndPointsbyTeamId(event.get('home_team_id'));
                event_list.append(event_dict);

    json_data_response = json.dumps(event_list)
    return json_data_response

if __name__ == "__main__":
    app.run(debug=True)
