import os

def get_beatmaps_id(song_dir: str):
    beatmapset = [os.path.join(song_dir, o) for o in os.listdir(song_dir) if os.path.isdir(os.path.join(song_dir, o))]
    beatmap_count = 0
    supported_beatmap = 0
    unsupported_beatmap = 0
    supported_beatmap_id = []
    unsupported_beatmapset_id = []

    for i in beatmapset:
        for j in os.listdir(i):
            if j[len(j)-4:len(j)] == '.osu':
                beatmap_count += 1
                f = open("{}/{}".format(i,j))
                if 'BeatmapID:' in f.read():
                    supported_beatmap += 1
                    for k in open("{}/{}".format(i,j)):
                        if 'BeatmapID:' in k:
                            supported_beatmap_id.append(int(k.split(':')[1]))
                else:
                    bid = int(i.replace(directory, '').split(' ')[0].replace('/', ''))
                    unsupported_beatmapset_id.append(bid)
                    unsupported_beatmap += 1

    unsupported_beatmapset_id.sort()
    print("[BeatmapReader] Highest unsupported beatmapset ID : {}".format(unsupported_beatmapset_id[-1]))
    print("[BeatmapReader] Found {} beatmaps".format(beatmap_count))
    print("[BeatmapReader] Supported beatmaps {} found".format(supported_beatmap))
    print("[BeatmapReader] Unsupported beatmaps {} found".format(unsupported_beatmap))
    return_data = {
        'beatmap_count' : beatmap_count,
        'supported_beatmap_count' : support_beatmap_count,
        'unsupported_beatmap_count' : unsupport_beatmap_count,
        'supported_beatmaps' : supported_beatmap_id,
        'unsupported_beatmap_sets' : unsupported_beatmapset_id
    }

    return return_data

if __name__ == '__main__':
    get_beatmaps_id('../../../mnt/c/Users/phoen/AppData/Local/osu!/Songs')