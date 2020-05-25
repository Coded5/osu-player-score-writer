#Find beatmap ID in osu! beatmap's directory
#If not found beatmap ID of a beatmap set will be unsupported beatmapset
#And will required to use API request to retrieve the indvidual beatmap ID
import os
import sys
import hashlib

def get_beatmaps_id(song_dir: str):
    print('[BeatmapReader] Getting beatmaps...')
    beatmapset = [os.path.join(song_dir, o) for o in os.listdir(song_dir) if os.path.isdir(os.path.join(song_dir, o))]
    beatmap_count = 0
    supported_beatmap = 0
    unsupported_beatmap = 0
    supported_beatmap_id = {}
    unsupported_beatmapset_id = []

    print('[BeatmapReader] Found {} beatmapsets'.format(len(beatmapset)))
    count = 0
    ex_count = len(beatmapset)
    for i in beatmapset:
        for j in os.listdir(i):
            if j[len(j)-4:len(j)] == '.osu':
                beatmap_count += 1
                f = open("{}/{}".format(i,j))
                if 'BeatmapID:' in f.read():
                    supported_beatmap += 1
                    for k in open("{}/{}".format(i,j)):
                        if 'BeatmapID:' in k:
                            md5 = hashlib.md5(open('{}/{}'.format(i,j), 'rb').read()).hexdigest()
                            supported_beatmap_id[int(k.split(':')[1])] = md5
                else:
                    bid = int(i.replace(song_dir, '').split(' ')[0].replace('/', ''))
                    unsupported_beatmapset_id.append(bid)
                    unsupported_beatmap += 1
        count += 1
        progress = (count / ex_count) * 100
        sys.stdout.write("Reading progress: %d%% [%d/%d]  \r" % (progress, count, ex_count) )
        sys.stdout.flush()

    unsupported_beatmapset_id.sort()
    print("[BeatmapReader] Highest unsupported beatmapset ID : {}".format(unsupported_beatmapset_id[-1]))
    print("[BeatmapReader] Found {} beatmaps".format(beatmap_count))
    print("[BeatmapReader] Supported beatmaps {} found".format(supported_beatmap))
    print("[BeatmapReader] Unsupported beatmaps {} found".format(unsupported_beatmap))
    return_data = {
        'beatmap_count' : beatmap_count,
        'supported_beatmap_count' : supported_beatmap,
        'unsupported_beatmap_count' : unsupported_beatmap,
        'supported_beatmaps' : supported_beatmap_id,
        'unsupported_beatmap_sets' : unsupported_beatmapset_id
    }

    return return_data