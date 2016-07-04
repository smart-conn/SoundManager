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

### Subscribe
- soundManager/play
  - payload
  ```
    {
      file: String, // Required 要播放的文件位置
      soundId: String,  // 声音 ID如果不填则自动生成
      args: String[] // 传入 sox 的参数
    }
  ```
- soundManager/break
  - payload
  ```
    {
      file: String, // Required 要播放的文件位置
      soundId: String,  // 声音 ID如果不填则自动生成
      args: String[] // 传入 sox 的参数
    }
  ```
- soundManager/pause
- soundManager/resume
- soundManager/stop_all
- soundManager/stop_all_break
  - payload
  ```
    {
      file: String, // Required 要播放的文件位置
      soundId: String,  // 声音 ID如果不填则自动生成
      args: String[] // 传入 sox 的参数
    }
  ```

### publish
- sound_manager/{soundId}/complete
- sound_manager/{soundId}/terminate

### Notic
Sometimes subprocess will hang on due to child process generates enough output to a pipe such that it blocks waiting for the OS pipe buffer to accept more data. Use communicate() to avoid that.
