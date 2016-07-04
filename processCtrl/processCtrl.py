import subprocess, time, os

# Need real ENV have 'pidof' command
def isPlay():
  for str in os.popen("ps -e | grep play").read().split("\n"):
    if(str.find("play <defunct>") != -1):
      continue
    else:
      if(str.find("play") != -1 and str != ""):
        return True
      else:
        continue
  return False

def kill():
  try:
    res = os.popen("pidof play")
    pids = res.read().split("\n")[0]
    if(pids != ""):
      os.system("kill -9 " + pids)
  except:
    print "stop error"
  finally:
    return True
