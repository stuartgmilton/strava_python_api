
from pandas.io.json import json_normalize
import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

import numpy as np

from datetime import datetime

from stravaio import strava_oauth2
from stravaio import StravaIO

import json


myvars = {}
with open('/home/ec2-user/environment/local_settings') as myfile:
    for line in myfile:
        name, var = line.partition("=")[::2]
        myvars[name.strip()] = var.rstrip().replace('"','')

CLIENT_ID = myvars['strava_client_id']
CLIENT_SECRET_ID = myvars['strava_client_secret']
ACCESS_TOKEN = myvars['strava_access_token']


def get_client(access_token=ACCESS_TOKEN):
    client = StravaIO(access_token=access_token)
    return client

def get_athlete(ourclient):
    athlete = ourclient.get_logged_in_athlete()

    if athlete is None:
        oauth2 = strava_oauth2(client_id=CLIENT_ID, client_secret=CLIENT_SECRET_ID)
        ourclient = StravaIO(access_token=oauth2['access_token'])
        athlete = ourclient.get_logged_in_athlete()
    return athlete

def get_all_activities(ourclient):
    activities = ourclient.get_logged_in_athlete_activities(after='2020-10-26')
    return activities


def main():

    client = get_client(ACCESS_TOKEN)
    athlete = get_athlete(client)
    activities = get_all_activities(client)

    lejog  = pd.DataFrame(columns=['Date','Distance'])

    for a in activities:
        if a.type in ['Run', 'Walk', 'Hike'] :
            miles = a.distance / 1000 / 8 * 5
            lejog = lejog.append({'Date': a.start_date_local.date(), 'Distance': miles}, ignore_index=True)

    summed_lejog = lejog.groupby(['Date']).sum()

    print(summed_lejog.to_markdown())

if __name__=="__main__":
    main()