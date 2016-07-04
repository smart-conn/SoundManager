# SoX player

### Package
- `sudo apt install sox`
- `sudo apt install libsox-fmt-mp3`
- `pip install paho-mqtt`
- `pip install redis`

### DB
  - keys
    - play:curr:file
    - play:curr:totalTime
    - play:curr:skip
    - play:curr:start
    - play:curr:stop
    - play:curr:id
    - play:imme:file
    - play:imme:id
  - list playList
    - id
    - file

### Topic
- soundManager/play
- soundManager/break
- soundManager/clearList
- soundManager/push
- soundManager/stopAndClear

### Notic
Sometimes subprocess will hang on due to child process generates enough output to a pipe such that it blocks waiting for the OS pipe buffer to accept more data. Use communicate() to avoid that.