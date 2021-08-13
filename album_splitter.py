import subprocess
import sys
import eyed3
from mutagen.easyid3 import EasyID3


def set_tags(filename, title, album_name, artist_name, index, cover):        
    audio = eyed3.load(filename)

    if (audio.tag == None):
        audio.initTag()

    audio.tag.title=title

    audio.tag.album=album_name

    audio.tag.artist=artist_name

    if cover:
        audio.tag.images.set(3, open(cover,'rb').read(), 'image/jpeg')

    audio.tag.save()

    audio =EasyID3(filename)

    audio["tracknumber"] = str(index)

    audio.save()


def main():

    # check command line for original file and track list file
    if len(sys.argv) != 6:
        print ('usage: <album_name> <artist_name> <original_track> <track_list_path> <template> [optional:cover_art_path]')
        exit(1)

    onlytwo = False

    # record command line args
    album_name = sys.argv[1]
    artist_name = sys.argv[2]
    original_track = sys.argv[3]
    track_list = sys.argv[4]
    template = sys.argv[5].split(',')
    try:
        cover_art = sys.argv[6]
    except IndexError:
        cover_art = None

    extension = original_track.split('.')[-1]
    
    if len(template) <= 1 or len(template) >= 4:
        print('Error: Invalid template')
        return

    elif len(template) == 2:
        sindex = template.index('start')
        nindex   = template.index('name')
        if sindex == -1 or nindex == -1:
            print('Error: Invalid template')
            return
        onlytwo = True

    else:
        sindex = template.index('start')
        nindex   = template.index('name')
        eindex    = template.index('end')
        if sindex == -1 or nindex == -1 or eindex == -1:
            print('Error: Invalid template')
            return

    # create a template of the ffmpeg call in advance
    cmd_string = 'ffmpeg -i {tr} -acodec copy -ss {st} -to {en} {nm}.'+extension

    # read each line of the track list and split into start, end, name
    with open(track_list, 'r') as f:

        if onlytwo:

            length = (subprocess.check_output('ffmpeg -i '+original_track+' 2>&1 | grep Duration | awk \'{print$2}\'', shell=True)[:-2]).decode("ascii")

            starts = []
            ends   = []
            names  = []

            for line in f:
                # skip comment and empty lines
                if line.startswith('#') or len(line) <= 1:
                    continue

                # create command string for a given track
                split_line = line.strip().split(';')
                start = split_line[sindex]
                name  = split_line[nindex]

                starts.append(start)
                ends.append(start)
                names.append(name)
            ends.append(length)

            for i,name in enumerate(names):
                command = cmd_string.format(tr=original_track, st=starts[i], en=ends[i+1], nm=(str(i)) )

                # use subprocess to execute the command in the shell
                subprocess.call(command, shell=True)

                set_tags(str(i)+".mp3", name, album_name, artist_name, i+1 , cover_art)
                # print(command)
            return None

        for i,line in enumerate(f):
            # skip comment and empty lines
            if line.startswith('#') or len(line) <= 1:
                continue

            # create command string for a given track
            split_line = line.strip().split(";")
            start = split_line[sindex]
            name  = split_line[nindex]
            end   = split_line[eindex]
            command = cmd_string.format(tr=original_track, st=start, en=end, nm=str(i))

            # use subprocess to execute the command in the shell
            subprocess.call(command, shell=True)


        return None



if __name__ == '__main__':
    main()
