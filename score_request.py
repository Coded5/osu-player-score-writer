import requests
import time
from typing import Dict
from score import Score
from parse_scores import pack_scores

test_beatmap_id = 1071754
test_player_name = 'Coded5'
osu_version = 202005191

API_KEY = 'c53979a6645be9d759d0bfee2184a37e8d72a901'
API_URL = 'https://osu.ppy.sh/api/{}'
REQ_SCORE_LIST = 'C:/Users/phoen/AppData/Local/osu!/Songs'

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
    score.replay_md5      = '098f6bcd4621d373cade4e832627b4f6'
    return score

def get_player_score(beatmap_ids: list, name: str):
    scores = {}
    for id in beatmap_ids:
        p = {'b' : id, 'u' : name}
        h = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        } 

        score_data = requests.get(API_URL.format('get_scores?k={}'.format(API_KEY)), headers=h, params=p)
        time.sleep(0.5)
        if len(score_data.json()) == 0:
            continue
        beatmap_data = requests.get(API_URL.format('get_beatmaps?k={}&{}'.format(API_KEY, 'b={}'.format(id)), headers=h))
        time.sleep(0.5)
        scores[beatmap_data.json()[0]['file_md5']] = [parseScore(score_data.json()[0])]
    pack_scores(scores, osu_version, "test_02.db")


def requestScore():
    beatmap_id = 764517
    p = {
        'b' : beatmap_id,
        'u' : test_player_name
    }

    h = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    } 

    score_data = requests.get(API_URL.format('get_scores?k={}'.format(API_KEY)), headers=h, params=p)
    beatmap_data = requests.get(API_URL.format('get_beatmaps?k={}&{}'.format(API_KEY, 'b={}'.format(beatmap_id)), headers=h))
    print(beatmap_data.json()[0])
    print(parseScore(score_data.json()[0]).toJSON())
    scores = {beatmap_data.json()[0]['file_md5'] : [parseScore(score_data.json()[0])]}
    pack_scores(scores, osu_version, "test_02.db")

requestScore()