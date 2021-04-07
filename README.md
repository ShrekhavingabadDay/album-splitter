# Album-splitter

An improved version of the script I found [here](https://unix.stackexchange.com/questions/280767/how-do-i-split-an-audio-file-into-multiple)

*Improved means that I think I made it easier to split by youtube-comment-like tracklists, so you do not have to write your own.*

## How to use?

### 1. Create file with tracklist
* pattern: `*song_name* *start_minutes:start_seconds* *end_minutes:end_seconds*`
* these don't have to be in this exact order, 
* separator has to be space
### 2. Run script
* `python <nameofscript> <path_to_album> <path_to_file> <pattern>`
pattern has to be the strings *name,end,start* in the order it is specified in the file separated by a single colon
  
Happy splitting!
