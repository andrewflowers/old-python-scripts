# Web scraping example of NFL player data
from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import csv
import time

base_url = 'http://www.pro-football-reference.com/play-index/psl_finder.cgi?request=1&match=single&year_min=1980&year_max=2013&season_start=1&season_end=-1&age_min=0&age_max=99&league_id=&team_id=&is_active=&is_hof=&pos_is_qb=Y&pos_is_rb=Y&pos_is_wr=Y&pos_is_te=Y&pos_is_rec=Y&pos_is_t=Y&pos_is_g=Y&pos_is_c=Y&pos_is_ol=Y&pos_is_dt=Y&pos_is_de=Y&pos_is_dl=Y&pos_is_ilb=Y&pos_is_olb=Y&pos_is_lb=Y&pos_is_cb=Y&pos_is_s=Y&pos_is_db=Y&pos_is_k=Y&pos_is_p=Y&c1stat=g&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by=av&draft=0&draft_year_min=1936&draft_year_max=2013&type=&draft_round_min=0&draft_round_max=99&draft_slot_min=1&draft_slot_max=500&draft_pick_in_round=0&draft_league_id=&draft_team_id=&college_id=all&conference=any&draft_pos_is_qb=Y&draft_pos_is_rb=Y&draft_pos_is_wr=Y&draft_pos_is_te=Y&draft_pos_is_rec=Y&draft_pos_is_t=Y&draft_pos_is_g=Y&draft_pos_is_c=Y&draft_pos_is_ol=Y&draft_pos_is_dt=Y&draft_pos_is_de=Y&draft_pos_is_dl=Y&draft_pos_is_ilb=Y&draft_pos_is_olb=Y&draft_pos_is_lb=Y&draft_pos_is_cb=Y&draft_pos_is_s=Y&draft_pos_is_db=Y&draft_pos_is_k=Y&draft_pos_is_p=Y&offset='

bigDF = pd.DataFrame()

last_offset = 58700

t0 = time.time() # Timing of code for profiling

for offset in range(0,last_offset,100):
    
    new_url = base_url + str(offset)
    
    page=urllib2.urlopen(new_url).read()
    soup = BeautifulSoup(page)
    table_rows=soup.find_all(name='tr', class_='')
    
    # On each page, of 129 rows, the first 21 are not players
    # first_row=21
    player_rows=table_rows[21:]
    
    smallDF = pd.DataFrame()
    
    for player in player_rows:        
        
        player_data = [data for data in player.strings]
        # player_data = []
        #for datapt in player.strings:
        #     player_data.append(datapt)
        
        df = pd.DataFrame(player_data).transpose()
    
        # if len(df.columns) == 27:
        smallDF = smallDF.append(df, ignore_index=True)
    
    bigDF = bigDF.append(smallDF, ignore_index=True)

t1 = time.time()

print('Total time: ' + str(t1-t0)) 

# Write data frame to .csv file
bigDF.to_csv('football.csv')


