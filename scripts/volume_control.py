#!/usr/bin/env python3
import subprocess
import sys

import executor


def get_volume():
  return executor.run('pulseaudio-ctl current | grep -o "[0-9]*" | head -n1')[0]

def set_volume(percentage):
  executor.run('pulseaudio-ctl set ' + str(percentage))
  emit_signal()

def toggle_volume():
  executor.run('pulseaudio-ctl mute')
  emit_signal()

def is_muted():
  return not executor.run('amixer get Master | grep -o "\[on\]" | head -n1')[0]

def write(message):
  sys.stdout.write(message)
  sys.stdout.flush()

def trim_to_range(volume):
  volume = int(volume)
  if volume < 0:
    volume = 0
  elif volume > 95:
    volume = 100
  return volume

def status():
  if int(get_volume()) == 0 or is_muted():
    return 'muted'
  else:
    return 'on'

def emit_signal():
  executor.run('pkill -RTMIN+1 i3blocks')

if __name__ == '__main__':
  command = sys.argv[1]

  if command == 'set':
    set_volume(trim_to_range(sys.argv[2]))
  elif command == 'up':
      executor.run('pulseaudio-ctl up')
      emit_signal()
  elif command == 'down':
      executor.run('pulseaudio-ctl down')
      emit_signal()
  elif command == 'toggle':
    toggle_volume()
  elif command == 'read':
    write(get_volume())
  elif command == 'status':
    write(status())
  elif command == 'i3blocks':
    output = 'VOL ' + get_volume()
    if is_muted():
      output = '<s>' + output + '</s>'
      output += '\n\n#bb7473'
    write(output)
  elif command == 'signal':
    emit_signal()
  else:
    write('Usage: ' + sys.argv[0] + ' [set|up|down|toggle|read|status] [value]\n')
