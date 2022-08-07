#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pulp
import numpy as np
import pandas as pd
import requests
import bs4
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pprint import pprint

def select_team(expected_scores, prices, positions, teams, total_budget=100, sub_factor=0.1):
    num_players = len(expected_scores)
    model = pulp.LpProblem("Constrained value maximisation", pulp.LpMaximize)
    decisions = [
        pulp.LpVariable("x{}".format(i), lowBound=0, upBound=1, cat='Integer')
        for i in range(num_players)
    ]
    captain_decisions = [
        pulp.LpVariable("y{}".format(i), lowBound=0, upBound=1, cat='Integer')
        for i in range(num_players)
    ]
    sub_decisions = [
        pulp.LpVariable("z{}".format(i), lowBound=0, upBound=1, cat='Integer')
        for i in range(num_players)
    ]


    # objective function:
    model += sum((captain_decisions[i] + decisions[i] + sub_decisions[i]*sub_factor) * expected_scores[i]
                 for i in range(num_players)), "Objective"

    # cost constraint
    model += sum((decisions[i] + sub_decisions[i]) * prices[i] for i in range(num_players)) <= total_budget  # total cost

    # position constraints
    # 1 starting goalkeeper
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 'GK') == 1
    # 2 total goalkeepers
    model += sum(decisions[i] + sub_decisions[i] for i in range(num_players) if positions[i] == 'GK') == 2

    # 3-5 starting defenders
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 'DEF') >= 3
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 'DEF') <= 5
    # 5 total defenders
    model += sum(decisions[i] + sub_decisions[i] for i in range(num_players) if positions[i] == 'DEF') == 5

    # 3-5 starting midfielders
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 'MID') >= 3
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 'MID') <= 5
    # 5 total midfielders
    model += sum(decisions[i] + sub_decisions[i] for i in range(num_players) if positions[i] == 'MID') == 5

    # 1-3 starting attackers
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 'FWD') >= 1
    model += sum(decisions[i] for i in range(num_players) if positions[i] == 'FWD') <= 3
    # 3 total attackers
    model += sum(decisions[i] + sub_decisions[i] for i in range(num_players) if positions[i] == 'FWD') == 3

    # team constraint
    for team_name in np.unique(teams):
        model += sum(decisions[i] + sub_decisions[i] for i in range(num_players) if teams[i] == team_name) <= 3  # max 3 players

    model += sum(decisions) == 11  # total team size
    model += sum(captain_decisions) == 1  # 1 captain
    
    for i in range(num_players):  
        model += (decisions[i] - captain_decisions[i]) >= 0  # captain must also be on team
        model += (decisions[i] + sub_decisions[i]) <= 1  # subs must not be on team

    model.solve()
    print("Total expected score = {}".format(model.objective.value()))

    return decisions, captain_decisions, sub_decisions


# In[2]:


url = 'https://fplform.com/fpl-predicted-points'
r = requests.get(url)
print(r.status_code) # hopefully it's 200, so we got something
soup = BeautifulSoup(r.text, 'html.parser')


# In[3]:


player_data = pd.read_html(url)
player_data[0]


# In[4]:


players = player_data[0].loc[:,"Player"]
teams = player_data[0].loc[:,"Team"]
positions = player_data[0].loc[:,"PosPosition"]
prices = player_data[0].loc[:,"CostPlayer's current price"]
ppnext6 = player_data[0].loc[:,"PPNext6"]
ppall = player_data[0].loc[:,"PPRest OfSeasonPredicted FPL points for the rest of the season"]


# In[5]:


# The last values of our arrays of data picked up some ugly parts of the site we scraped:


# In[6]:


ppnext6.values
ppall.values
prices.values
positions.values
players.values
teams.values


# In[7]:


chopped_ppnext6 = ppnext6.values[0:-1]
chopped_prices = prices.values[0:-1]
chopped_positions = positions.values[0:-1]
chopped_players = players.values[0:-1]
chopped_teams = teams.values[0:-1]
chopped_ppall = ppall.values[0:-1]

best_ppnext6 = pd.Series(chopped_ppnext6)
best_prices = pd.Series(chopped_prices)
best_positions = pd.Series(chopped_positions)
best_players = pd.Series(chopped_players)
best_teams = pd.Series(chopped_teams)
best_ppall = pd.Series(chopped_ppall)

best_teams


# In[8]:


# Team made for the close future (next 6 gameweeks):

decisions, captain_decisions, sub_decisions = select_team(best_ppnext6, best_prices, best_positions, best_teams)
player_indices = []

print()
print("First Team:")
for i in range(len(decisions)):
    if decisions[i].value() == 1:
        print("{}{}".format(best_players[i], "*" if captain_decisions[i].value() == 1 else ""))
        player_indices.append(i)
print()
print("Subs:")
for i in range(len(sub_decisions)):
    if sub_decisions[i].value() == 1:
        print(best_players[i])
        player_indices.append(i)


# In[9]:


# Team made for the entire season (set and forget, no transfers):

decisions, captain_decisions, sub_decisions = select_team(best_ppall, best_prices, best_positions, best_teams)
player_indices = []

print()
print("First Team:")
for i in range(len(decisions)):
    if decisions[i].value() == 1:
        print("{}{}".format(best_players[i], "*" if captain_decisions[i].value() == 1 else ""))
        player_indices.append(i)
print()
print("Subs:")
for i in range(len(sub_decisions)):
    if sub_decisions[i].value() == 1:
        print(best_players[i])
        player_indices.append(i)


# In[ ]:




