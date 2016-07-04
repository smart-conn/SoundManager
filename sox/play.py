import redis
import time, os, json
from subprocess import Popen, PIPE, STDOUT
import threading
from processCtrl import *
import paho.mqtt.publish as publish

DB = 0
DB_KEY_PREFIX = "play:curr:"
DB_KEY_ID = DB_KEY_PREFIX + "id"
DB_KEY_FILE = DB_KEY_PREFIX + "file"
DB_KEY_START = DB_KEY_PREFIX + "start"
DB_KEY_STOP = DB_KEY_PREFIX + "stop"
DB_KEY_SKIP = DB_KEY_PREFIX + "skip"
DB_PLAYLIST = "playList"
TOPIC_PREFIX = "sound_manager"

r = redis.StrictRedis(host='localhost', port=6379, db=DB)

def pubMsg(topic, payload):
  publish.single(topic, payload, hostname = "127.0.0.1", port = 1883)

def masterPlayOnExit():
  r.delete(DB_KEY_STOP)
  r.delete(DB_KEY_SKIP)
  lastSoundId = r.get(DB_KEY_ID)
  pubMsg(TOPIC_PREFIX + "/" + lastSoundId + "/complete", "payload")
  res = r.lpop(DB_PLAYLIST)
  if(res is None):
    return
  else:
    soundInfo = json.loads(res)
  soundId = soundInfo.get("id")
  filename = soundInfo.get("file")
  r.set(DB_KEY_START, time.time())
  r.set(DB_KEY_ID, soundId)
  r.set(DB_KEY_FILE, filename)
  popenAndCall(masterPlayOnExit, filename, 0)
  return

def push(filename, id):
  if(processCtrl.isPlay()):
    r.lpush(DB_PLAYLIST, json.dumps({"id": id, "file": filename}))
  else:
    if(r.get(DB_KEY_STOP) is not None):
      r.lpush(DB_PLAYLIST, json.dumps({"id": id, "file": filename}))
      resume()
    else:
      popenAndCall(masterPlayOnExit, filename, 0)
      r.set(DB_KEY_START, time.time())
      r.set(DB_KEY_ID, id)
      r.set(DB_KEY_FILE, filename)
  return

def clearPlayList():
  r.delete("playList")
  return

def backPlayNull():
  return

def clearCurr():
  r.delete(DB_KEY_START)
  r.delete(DB_KEY_FILE)
  r.delete(DB_KEY_STOP)
  r.delete(DB_KEY_ID)
  r.delete(DB_KEY_SKIP)
  return

def immePlayAndClear(filename):
  clearPlayList()
  clearCurr()
  popenAndCall(backPlayNull, filename, 0)
  return

def pause():
  processCtrl.kill()
  soundId = r.get(DB_KEY_ID)
  start = float(r.get(DB_KEY_START))
  stop = r.get(DB_KEY_STOP)
  if(stop is None):
    stop = time.time()
  else:
    stop = float(stop)
  skip = r.get(DB_KEY_SKIP)
  if(skip is not None):
    skip = stop - start + float(skip)
  else:
    skip = stop - start
  r.set(DB_KEY_SKIP, skip)
  r.set(DB_KEY_STOP, stop)
  pubMsg(TOPIC_PREFIX + "/" + soundId + "/terminate", json.dumps({"progress":str(skip)}))
  return

def resume():
  if(processCtrl.isPlay()):
    return
  start = float(r.get("play:curr:start"))
  stop = r.get(DB_KEY_STOP)
  if(stop is None):
    return
  else:
    stop = float(stop)
  filename = r.get(DB_KEY_FILE)
  skip = r.get(DB_KEY_SKIP)
  if(skip is None):
    skip = 0
  else:
    skip = float(skip)
  skip = stop - start + skip
  r.set(DB_KEY_START, time.time())
  r.delete(DB_KEY_STOP)
  popenAndCall(masterPlayOnExit, filename, skip)
  return

def stopAndClear():
  clearCurr()
  clearPlayList()
  processCtrl.kill()
  return

def immePlay(filename, id):
  if(processCtrl.isPlay()):
    pause()
    popenAndCall(resume, filename, 0)
  else:
    popenAndCall(backPlayNull, filename, 0)
  return

def popenAndCall(onExit, filename, skip):
    def runInThread(onExit, filename):
        proc = Popen(["play", filename, "trim", str(skip)], stdout = PIPE, stderr = STDOUT)
        for line in proc.stdout:
          if(line.find("Done") != -1):
            onExit()
          else:
            # print line
            pass
        proc.wait()
        return
    thread = threading.Thread(target=runInThread, args=(onExit, filename))
    thread.setDaemon(True)
    thread.start()
    return thread
