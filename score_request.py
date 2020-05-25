import requests
import time
import sys
import hashlib

from typing import Dict
from score import Score
from parse_scores import pack_scores

delay = 0.3
osu_version = 202005191

API_KEY = 'c53979a6645be9d759d0bfee2184a37e8d72a901'
API_URL = 'https://osu.ppy.sh/api/{}'
REQ_SCORE_LIST = 'C:/Users/<uwu>/AppData/Local/osu!/Songs'

def parseScore(s : Dict[str, str]):
    score = Score()
    score.mode = 0
    score.version = osu_version
    score.player_name     = s['username']
    score.num_300s        = int(s['count300'])
    score.num_100s        = int(s['count100'])
    score.num_50s         = int(s['count50'])
    score.num_gekis       = int(s['countgeki'])
    score.num_katus       = int(s['countkatu'])
    score.num_misses      = int(s['countmiss'])
    score.replay_score    = int(s['score'])
    score.max_combo       = int(s['maxcombo'])
    score.perfect_combo   = s['perfect'] == '1'
    score.mods            = int(s['enabled_mods'])
    score.online_score_id = int(s['score_id'])
    score.replay_md5      = ''
    return score

def get_player_score(beatmap_ids: Dict[int, str], players: list):
    print("[ScoreRequest] Preparing requests parameters")
    scores = {}
    h = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    } 

    print("[ScoreRequest] Player count : {}".format(len(players)))
    print("[ScoreRequest] Beatmap count : {}".format(len(beatmap_ids)))

    request_count = len(players) * len(beatmap_ids)
    print("[ScoreRequest] Request count : {}".format(request_count))
    print("[ScoreRequest] Starting requests...")
    progress = 0
    found_score = 0
    req = 0
    for player in players:
        for i in beatmap_ids:
            p = {'b' : i, 'u' : player}

            score_data = requests.get(API_URL.format('get_scores?k={}'.format(API_KEY)), headers=h, params=p)
            time.sleep(delay)
            req += 1

            progress = (req / request_count) * 100
            sys.stdout.write("Requesting progress: %d%% [%d/%d, Found(%s) : %d]  \r" % (progress, req, request_count, player, found_score) )
            sys.stdout.flush()
            if len(score_data.json()) == 0:
                continue
            found_score += 1
            scores[beatmap_ids[i]] = [parseScore(score_data.json()[0])]
            
    return scores
