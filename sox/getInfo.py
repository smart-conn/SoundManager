from subprocess import Popen, PIPE, STDOUT

# get file time
def time(filename):
  p = Popen(["soxi", filename], stdout = PIPE, stderr = STDOUT, close_fds = True)
  out = p.stdout.read().split("\n")[5].split(": ")[1][0:11]
  print convertToSec(out)
  return

# 00:00:06.35 => 6.35
def  convertToSec(str):
  strs = str.split(":")
  return int(strs[0])*3600+int(strs[1])*60+int(strs[2][0:2])+float(strs[2].split(".")[1])*0.01