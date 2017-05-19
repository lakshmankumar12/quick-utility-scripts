#!/usr/bin/python

from __future__ import print_function
import subprocess
import sys
import argparse
import os

temp_file_name="/tmp/lk_tmux_compact.sh"

def get_current_windows_list(sessionName):
  '''
     Returns list-of (win-no,win-name,pane-no,pane-title,pane-tty)
             dict-of (win-name -> list-of(win-no,pane-no))

             Note that its (win-no,pane-no) that is uniq
  '''
  cmd=['tmux','list-panes','-s','-t',sessionName,'-F','#I|#W|#P|#T|#{pane_tty}']
  a=subprocess.Popen(cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output,err=a.communicate('')
  errcode = a.wait()
  lines=output.split('\n')
  list_of_panes = []
  dict_of_win_names = {}
  for l in lines:
    a = l.strip().split('|')
    if len(a) == 5:
      list_of_panes.append(a)
      u = (a[0],a[2])
      if a[1] in dict_of_win_names:
        dict_of_win_names[a[1]].append(u)
      else:
        dict_of_win_names[a[1]] = [u]
  return (list_of_panes,dict_of_win_names)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-t","--title", help="win-title to mean nothing useful", default="bash")
  parser.add_argument("sessionName",  help="Name of session", nargs="?", default="0")
  parsed_args = parser.parse_args()

  list_of_panes,dict_of_win_names = get_current_windows_list(parsed_args.sessionName)

  #lets check if there are only 1 pane in a window.
  win_no_dict = {}
  duplicates = False
  for i in list_of_panes:
    if i[0] in win_no_dict:
      print("Extra pane in window:%s, extra:%s"%(win_no_dict[i[0]],i))
      duplicates = True
  if duplicates:
    print("Fix the panes first")
    sys.exit(1)

  fd = open(temp_file_name,"w")

  print ("#delete this line to ok", file=fd)

  dict_of_orig = {}

  #collect gaps
  last_num = int(list_of_panes[-1][0])
  free_id_to_use = last_num + 1
  index = 0
  for i in range(last_num+1):
    l = list_of_panes[index]
    n = int(l[0])
    if i == n:
      index+=1
      line = "%-3s | %-25s | %-3s | %s"%(l[0],l[1],l[2],l[3])
      dict_of_orig[l[0]] = line
      print (line,file=fd)
    else:
      print ("#%-3s | Gap"%i,file=fd)

  fd.close()

  os.system("vim %s"%temp_file_name)

  with open(temp_file_name,"r") as fd:
    lines = fd.readlines()

  if lines[0][0] == '#':
    print ("Not doing anything, as comment line is retained")
    return

  picked_windows = {}
  picked_windows_as_list = []
  index = 0
  for l in lines:
    if l[0] == '#':
      continue
    elems = map(lambda i: i.strip(), l.split('|'))
    if elems[0] not in dict_of_orig:
      print ("win-no %s, not in original list!"%elems[0])
      sys.exit(1)
    l = l.strip()
    if dict_of_orig[elems[0]] != l:
      if len(dict_of_orig[elems[0]]) != len(l):
        print ("Lens are diff:%d,%d"%(len(dict_of_orig[elems[0]]),len(l)))
      print ("win-no %s, was originally:\n%s\nbut now:\n%s\n!"%(elems[0],dict_of_orig[elems[0]],l))
      sys.exit(1)
    orig_id = int(elems[0])
    picked_windows[orig_id] = (index, l)
    picked_windows_as_list.append(orig_id)
    index += 1
    del dict_of_orig[elems[0]]

  if dict_of_orig:
    print ("You have left out some windows!")
    for i in dict_of_orig:
      print ("%s"%dict_of_orig[i])
    sys.exit(1)

  #orig-id -> original id, before we started
  #tgt-id  -> desired id,
  #curr-id -> its curr-id (might be either orig or one of the free_id_to_use+N..)

  for tgt_id,orig_id in enumerate(picked_windows_as_list):
    if tgt_id == orig_id:
      print("%d is already okay"%tgt_id)
    else:
      if tgt_id not in picked_windows:
        print ("moving %d to a free spot - %d"%(orig_id,tgt_id))
        cmd = "tmux move-window -s %d -t %d"%(orig_id,tgt_id)
        print (cmd)
        os.system(cmd)
      else:
        print ("swapping spots")
        cmd = "tmux move-window -s %d -t %d"%(tgt_id,free_id_to_use)
        print (cmd)
        os.system(cmd)
        (index,l) = picked_windows[tgt_id]
        del picked_windows[tgt_id]
        picked_windows_as_list[index] = free_id_to_use
        picked_windows[free_id_to_use] = (index,l)
        free_id_to_use += 1
        cmd = "tmux move-window -s %d -t %d"%(orig_id,tgt_id)
        print (cmd)
        os.system(cmd)
      (index,l) = picked_windows[orig_id]
      del picked_windows[orig_id]
      picked_windows[tgt_id] = (index,l)


if __name__ == '__main__':
  main()

