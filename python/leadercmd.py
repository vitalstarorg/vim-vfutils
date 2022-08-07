import unittest
import re
import os

class LeaderCmd:
  debugmsg = False
  reg1 = r'([a-z]*:\/\/[^ >,;)]*)' 
    # url
    # "https://aa.bb/cc#dd" "file://aa.bb"
  reg2 = r'([a-zA-Z~_/]+[^ .]+\.[^0-9 @]+)@*([^#]*)' 
    # local file and search marker by @
    # "  file.md@project
  #reg3 = r'@*([0-9a-zA-Z-~_/][^ .]+\.[^0-9 @]+)' 
    # local file
    # "  @@ xx"
  reg4 = r'@+ *([^#]*)' 
    # local file
    # "  xx.xx "
  reg5 = r'^[-+\*]+: *([^#]*)' 
    # mindmap multi-line
    #"--: xx" "++: xx" "**: xx"
  reg6 = r'[-+\*]+ ([^#]*)' 
    # mindmap right & left
    #" -- xx" " ++ xx" " ** xx"
  hashbang = r'^#! *(.*)' 
  vimbang = r'^#: *(.*)' 

  def extractLCmd(line, debug=False):
    m = re.search(LeaderCmd.hashbang, line)
    if m:
      if LeaderCmd.debugmsg: print(">> hashbang")
      s = m.group(1).strip()
      #s = re.sub(r'#', '\\#', s)
      #return [":!%s" % s,"",""]
      if not debug:
        ret = os.system(s)
      return ["echo '%s'" % s,"hashbang","", "skip-cr","hashbang"]

    m = re.search(LeaderCmd.vimbang, line)
    if m:
      if LeaderCmd.debugmsg: print(">> vimbang")
      s = m.group(1).strip()
      return [":%s" % s,"vimbang","", "skip-cr","vimbang"]

    m = re.search(LeaderCmd.reg1, line)
    if m:
      if LeaderCmd.debugmsg: print(">> reg1")
      s = m.group(1).strip()
      s = re.sub(r'#', '\\#', s)
      s = re.sub(r'%', '\\%', s)
      return [":!open '%s'" % s,"","","","reg1"]

    m = re.search(LeaderCmd.reg2, line)
    if m and len(m.groups()) == 2:
      if LeaderCmd.debugmsg: print(">> reg2")
      s = m.group(1).strip()
      t = m.group(2).strip()
      #print("-- %s %s" % (s,t))
      if s != ".":
        win_name = os.path.basename(s)
        if t != "":
          stmux = ":!tmux new-window -an '%s' -c '\\#{pane_current_path}' \"vim %s -c '/%s'\"" % (win_name,s,t)
        else:
          stmux = ":!tmux new-window -an '%s' -c '\\#{pane_current_path}' \"vim %s\"" % (win_name,s)
      return [stmux,s,t,"","reg2"]

#    m = re.search(LeaderCmd.reg3, line)
#    if m:
#      if LeaderCmd.debugmsg: print(">> reg3")
#      s = m.group(1)
#      if s != ".":
#        stmux = ":!tmux new-window -an '%s' -c '\\#{pane_current_path}' vim %s" % (s,s)
#        return [stmux,s,"","","reg3"]

    m = re.search(LeaderCmd.reg4, line)
    if m:
      if LeaderCmd.debugmsg: print(">> reg4")
      s = m.group(1).strip()
      s = re.sub(r'/', '\\\/', s)
      s = s.rstrip()
      return ["/%s" % s,s,"Found @Marker","","reg4"]

    m = re.search(LeaderCmd.reg5, line)
    if m:
      if LeaderCmd.debugmsg: print(">> reg5")
      s = m.group(1).strip()
      s = re.sub(r'/', '\\\/', s)
      s = s.rstrip()
      return ["/%s" % s,s,"Found mindmap header","","reg5"]

    m = re.search(LeaderCmd.reg6, line)
    if m:
      if LeaderCmd.debugmsg: print(">> reg6")
      s = m.group(1).strip()
      s = re.sub(r'/', '\\\/', s)
      s = s.rstrip()
      return ["/%s" % s,s,"Found mindmap item","","reg6"]

    return ['','','','']

  runcmd1 = r'^#@+ *(.*)' 
  def _extractRunCmd(line, direction):
    m = re.search(LeaderCmd.runcmd1, line)
    cmd = ""
    if m:
      cmd = m.group(1).strip()
      #ret = os.system(c)
      #return ret
    else:
      line = re.sub(r'\\', "\\\\\\\\", line)
      line = re.sub(r';$', '\;', line) # only the last semi-colon
      line = re.sub(r'"', '\\"', line)
      line = re.sub(r'\$', '\\\$', line)
      cmd = "tmux send-keys -t {%s-of} \"%s\" C-m" % (direction,line)
    return cmd

  def extractRunCmd(line, direction):
    tmuxcmd = LeaderCmd._extractRunCmd(line,direction)
    ret = os.system(tmuxcmd)
    return tmuxcmd

  def tryout(line):
    return line

class TestLeaderCmd(unittest.TestCase):
  def test_extractLCmd(self):
    # reg1: url
    result = LeaderCmd.extractLCmd("[MindMap](https://plantuml.com/mindmap-diagram")
    self.assertEqual(":!open 'https://plantuml.com/mindmap-diagram'", result[0])
    self.assertEqual("", result[1])
    self.assertEqual("", result[2])

    # reg3: local file
    result = LeaderCmd.extractLCmd("**:@~/aa/bb/cc.dd")
    self.assertEqual(":!tmux new-window -an 'cc.dd' -c '\#{pane_current_path}' \"vim ~/aa/bb/cc.dd\"", result[0])
    self.assertEqual("~/aa/bb/cc.dd", result[1])
    self.assertEqual("", result[2])
    self.assertEqual("reg2", result[4])
      # reg3 is superseded by reg2

    result = LeaderCmd.extractLCmd("- cc.dd")
    self.assertEqual(":!tmux new-window -an 'cc.dd' -c '\#{pane_current_path}' \"vim cc.dd\"", result[0])
    self.assertEqual("cc.dd", result[1])
    self.assertEqual("", result[2])
    self.assertEqual("reg2", result[4])

    # reg4
    result = LeaderCmd.extractLCmd("  @A/B")
    self.assertEqual("/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found @Marker", result[2])

    result = LeaderCmd.extractLCmd("**:@A/B ")
    self.assertEqual("/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found @Marker", result[2])

    result = LeaderCmd.extractLCmd("**:@A/B # comment")
    self.assertEqual("/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found @Marker", result[2])

    # reg5
    result = LeaderCmd.extractLCmd("**:A/B ")
    self.assertEqual("/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found mindmap header", result[2])

    result = LeaderCmd.extractLCmd("**:A/B # comment")
    self.assertEqual("/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found mindmap header", result[2])

    # reg2
    result = LeaderCmd.extractLCmd(" - a/b.out ")
    self.assertEqual(":!tmux new-window -an 'b.out' -c '\#{pane_current_path}' \"vim a/b.out\"", result[0])
    self.assertEqual("a/b.out", result[1])
    self.assertEqual("", result[2])

    result = LeaderCmd.extractLCmd(" - a/b.out@")
    self.assertEqual(":!tmux new-window -an 'b.out' -c '\#{pane_current_path}' \"vim a/b.out\"", result[0])
    self.assertEqual("a/b.out", result[1])
    self.assertEqual("", result[2])

    result = LeaderCmd.extractLCmd(" - a/b.out@a_b")
    self.assertEqual(":!tmux new-window -an 'b.out' -c '\#{pane_current_path}' \"vim a/b.out -c '/a_b'\"", result[0])
    self.assertEqual("a/b.out", result[1])
    self.assertEqual("a_b", result[2])

    result = LeaderCmd.extractLCmd("- cc.dd")
    self.assertEqual(":!tmux new-window -an 'cc.dd' -c '\#{pane_current_path}' \"vim cc.dd\"", result[0])
    self.assertEqual("cc.dd", result[1])
    self.assertEqual("", result[2])
    self.assertEqual("reg2", result[4])

    result = LeaderCmd.extractLCmd("- vimtest2.md@project ")
    self.assertEqual(":!tmux new-window -an 'vimtest2.md' -c '\#{pane_current_path}' \"vim vimtest2.md -c '/project'\"", result[0])
    self.assertEqual("vimtest2.md", result[1])
    self.assertEqual("project", result[2])
    self.assertEqual("reg2", result[4])

    result = LeaderCmd.extractLCmd("- vimtest2.md@project file ")
    self.assertEqual(":!tmux new-window -an 'vimtest2.md' -c '\#{pane_current_path}' \"vim vimtest2.md -c '/project file'\"", result[0])
    self.assertEqual("vimtest2.md", result[1])
    self.assertEqual("project file", result[2])
    self.assertEqual("reg2", result[4])

    # reg6
    result = LeaderCmd.extractLCmd("  - A/B")
    self.assertEqual("/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found mindmap item", result[2])

    result = LeaderCmd.extractLCmd("  - A/B # comment")
    self.assertEqual("/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found mindmap item", result[2])

  def test_extractRunCmd(self):
    s = "a = \"-\\\\-\""
    result = LeaderCmd._extractRunCmd(s,"down")
    self.assertEqual("tmux send-keys -t {down-of} \"a = \\\"-\\\\\\\\-\\\"\" C-m", result)
    s = "a = '-\\\\-'"
    result = LeaderCmd._extractRunCmd(s,"down")
    self.assertEqual("tmux send-keys -t {down-of} \"a = '-\\\\\\\\-'\" C-m", result)
    s = "#@ tmux split-window -hd"
    result = LeaderCmd._extractRunCmd(s,"down")
    self.assertEqual("tmux split-window -hd", result)
    s = "echo \"$WAIT\""
    result = LeaderCmd._extractRunCmd(s,"down")
    self.assertEqual("tmux send-keys -t {down-of} \"echo \\\"\$WAIT\\\"\" C-m", result)

if __name__ == '__main__':
  unittest.main()
