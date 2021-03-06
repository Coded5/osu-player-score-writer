from beatmap_reader import get_beatmaps_id
from score_request import get_player_score
from parse_scores import pack_scores
from score import Score

beatmap_dir = 'directory here'
player_list = ['username']
osu_version = osu_version_here

def main():
    beatmaps_data = get_beatmaps_id(beatmap_dir)
    unsupported_set = beatmaps_data['unsupported_beatmap_sets'] #I'll deal with this later :/
    supported_beatmaps = beatmaps_data['supported_beatmaps']

    requests_count = (len(supported_beatmaps) * len(player_list)) + (len(unsupported_set) * len(player_list))
    scores = get_player_score(supported_beatmaps, player_list)

    print('[Main] Packing score...')
    pack_scores(scores, osu_version, 'scores.db')
    for i in scores:
        scores[i][0].toJSON()

if __name__ == '__main__':
    main()