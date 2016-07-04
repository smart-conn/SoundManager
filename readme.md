# SoX player

### Package
- `sudo apt install sox`
- `sudo apt install libsox-fmt-mp3`
- `pip install paho-mqtt`
- `pip install redis`

### DB
  - keys
    - play:curr:file
    - play:curr:skip
    - play:curr:start
    - play:curr:stop
    - play:curr:id
  - list playList
    - id
    - file

### Topic
- soundManager/play
- soundManager/break
- soundManager/pause
- soundManager/resume
- soundManager/stop_all
- soundManager/stop_all_break


### Notic
Sometimes subprocess will hang on due to child process generates enough output to a pipe such that it blocks waiting for the OS pipe buffer to accept more data. Use communicate() to avoid that.
