import subprocess
import sys

def main():

    # check command line for original file and track list file
    if len(sys.argv) != 4:
        print ('usage: <original_track> <track_list> <template>')
        exit(1)

    onlytwo = False

    # record command line args
    original_track = sys.argv[1]
    track_list = sys.argv[2]
    template = sys.argv[3].split(',')

    extension = original_track.split('.')[-1]
    
    # if you do not know how to specify a template, you get a very helpful error
    if len(template) <= 1 or len(template) >= 4:
        print('Error: Template length has to be within the range of 2-3')
        return

    # assign an index to all the parameters in the template
    elif len(template) == 2:
        sindex = template.index('start')
        nindex = template.index('name')
        if sindex == -1 or nindex == -1:
            print('Error: Invalid template')
            return
        onlytwo = True

    else:
        sindex = template.index('start')
        nindex = template.index('name')
        eindex = template.index('end')
        if sindex == -1 or nindex == -1 or eindex == -1:
            print('Error: Invalid template')
            return

    # create a template of the ffmpeg call in advance
    cmd_string = 'ffmpeg -i {tr} -acodec copy -ss {st} -to {en} {nm}.'+extension

    # read each line of the track list and split into start, end, name
    with open(track_list, 'r') as f:

        if onlytwo:

            # get length of original file
            length = subprocess.check_output('ffmpeg -i '+original_track+' 2>&1 | grep Duration | awk \'{print$2}\'', shell=True)[:-2]

            # damn, this line is nasty!
            length = ':'.join((length.decode("ascii").split('.')[0]).split(':')[1:])

            starts = []
            ends   = []
            names  = []

            for line in f:
                
                # skip comment and empty lines
                if line.startswith('#') or len(line) <= 1:
                    continue
                
                # extract data from file and store it in a way we like it
                split_line = line.strip().split(' ')
                start = split_line[sindex]
                name  = split_line[nindex]

                starts.append(start)
                ends.append(start)
                names.append(name)
            
            # we need the length of the file at the end of this array so we don't get f*cked by ffmpeg
            ends.append(length)

            for i,n in enumerate(names):
                command = cmd_string.format(tr=original_track, st=starts[i], en=ends[i+1], nm=n)

                # use subprocess to execute the command in the shell
                subprocess.call(command, shell=True)
                
                # print(command) => this is for debugging but I am gonna leave it in. Hope you don't mind <3
                 
            return None

        for line in f:
            
            # skip comment and empty lines
            if line.startswith('#') or len(line) <= 1:
                continue

            # create command string for a given track
            split_line = line.strip().split()
            
            start = split_line[sindex]
            name  = split_line[nindex]
            end   = split_line[eindex]
            
            command = cmd_string.format(tr=original_track, st=start, en=end, nm=name)

            # use subprocess to execute the command in the shell
            subprocess.call(command, shell=True)


        return None


if __name__ == '__main__':
    main()
