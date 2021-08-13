# Album-splitter

An improved version of the script I found [here](https://unix.stackexchange.com/questions/280767/how-do-i-split-an-audio-file-into-multiple)

*Improved means that I think I made it easier to split by youtube-comment-like tracklists, so you do not have to write your own.
--> and now with the new "release" it automatically edits the id3 tags (no support for flac (vorbis tags) yet BIG SAD) *

## How to use?

### Get the script
good old `https://github.com/ShrekhavingabadDay/album-splitter`
`cd album-splitter`
`pip install dependencies.txt`

### 1. Create file with tracklist
* pattern: `*song_name*;*start_minutes:start_seconds*;*end_minutes:end_seconds*`
* these don't have to be in this exact order, 
* separator has to be semicolon
### 2. Run script
* `python album_splitter.py <album_name> <artist_name> <original_track> <track_list_path> <template> [optional:cover_art_path]`
* You should work with relative paths
template has to be the strings *name,end,start* in the order it is specified in the tracklist file. Separator has to be colon.
  
Happy splitting!
