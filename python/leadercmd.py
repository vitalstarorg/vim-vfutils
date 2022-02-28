import unittest
import re
import os

class LeaderCmd:
  reg1 = r'([a-z]*:\/\/[^ >,;)]*)' 
    # url
    # "https://aa.bb/cc#dd" "file://aa.bb"
  reg2 = r'@*([0-9a-zA-Z-~_/]+\.[^0-9 ]+)' 
    # local file
  reg3 = r'@+ *([^#]*)' 
    # search marker by @
    # "  @@ xx"
  reg4 = r'^[-+\*]+: *([^#]*)' 
    # mindmap multi-line
    #"--: xx" "++: xx" "**: xx"
  reg5 = r'([a-zA-Z-~_/]+\.[^0-9 ]+)' 
    # local file
    # "  xx.xx "
  reg6 = r'[-+\*]+ ([^#]*)' 
    # mindmap right & left
    #" -- xx" " ++ xx" " ** xx"
  hashbang = r'^#! *(.*)' 
  vimbang = r'^#: *(.*)' 

  def extractLCmd(line, debug=False):
    m = re.search(LeaderCmd.hashbang, line)
    if m:
      s = m.group(1)
      #s = re.sub(r'#', '\\#', s)
      #return [":!%s" % s,"",""]
      if not debug:
        ret = os.system(s)
      return ["echo '%s'" % s,"hashbang",""]

    m = re.search(LeaderCmd.vimbang, line)
    if m:
      s = m.group(1)
      return [":%s" % s,"vimbang",""]

    m = re.search(LeaderCmd.reg1, line)
    if m:
      s = m.group(1)
      s = re.sub(r'#', '\\#', s)
      s = re.sub(r'%', '\\%', s)
      return [":!open '%s'" % s,"",""]

    m = re.search(LeaderCmd.reg2, line)
    if m:
      s = m.group(1)
      if s != ".":
        stmux = ":!tmux new-window -an '%s' -c '\\#{pane_current_path}' vim %s" % (s,s)
        return [stmux,s,""]

    m = re.search(LeaderCmd.reg3, line)
    if m:
      s = m.group(1)
      s = re.sub(r'/', '\\\/', s)
      s = s.rstrip()
      return ["/%s" % s,s,"Found @Marker"]

    m = re.search(LeaderCmd.reg4, line)
    if m:
      s = m.group(1)
      s = re.sub(r'/', '\\\/', s)
      s = s.rstrip()
      return ["/%s" % s,s,"Found mindmap header"]

    m = re.search(LeaderCmd.reg5, line)
    if m:
      s = m.group(1)
      if s != ".":
        stmux = ":!tmux new-window -an '%s' -c '\\#{pane_current_path}' vim %s" % (s,s)
        return [stmux,s,""]

    m = re.search(LeaderCmd.reg6, line)
    if m:
      s = m.group(1)
      s = re.sub(r'/', '\\\/', s)
      s = s.rstrip()
      return ["/%s" % s,s,"Found mindmap item"]

    return ['','','']

  runcmd1 = r'^#@+ *(.*)' 
  def _extractRunCmd(line, direction):
    m = re.search(LeaderCmd.runcmd1, line)
    cmd = ""
    if m:
      cmd = m.group(1)
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

    # reg2: local file
    result = LeaderCmd.extractLCmd("**:@~/aa/bb/cc.dd")
    self.assertEqual(":!tmux new-window -an '~/aa/bb/cc.dd' -c '\#{pane_current_path}' vim ~/aa/bb/cc.dd", result[0])
    self.assertEqual("~/aa/bb/cc.dd", result[1])
    self.assertEqual("", result[2])

    # reg3
    result = LeaderCmd.extractLCmd("  @A/B")
    self.assertEqual(":/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found @Marker", result[2])

    result = LeaderCmd.extractLCmd("**:@A/B ")
    self.assertEqual(":/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found @Marker", result[2])

    result = LeaderCmd.extractLCmd("**:@A/B # comment")
    self.assertEqual(":/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found @Marker", result[2])

    # reg4
    result = LeaderCmd.extractLCmd("**:A/B ")
    self.assertEqual(":/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found mindmap header", result[2])

    result = LeaderCmd.extractLCmd("**:A/B # comment")
    self.assertEqual(":/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found mindmap header", result[2])

    # reg5
    result = LeaderCmd.extractLCmd(" - a/b.out ")
    self.assertEqual(":!tmux new-window -an 'a/b.out' -c '\#{pane_current_path}' vim a/b.out", result[0])
    self.assertEqual("a/b.out", result[1])
    self.assertEqual("", result[2])

    # reg6
    result = LeaderCmd.extractLCmd("  - A/B")
    self.assertEqual(":/A\/B", result[0])
    self.assertEqual("A\/B", result[1])
    self.assertEqual("Found mindmap item", result[2])

    result = LeaderCmd.extractLCmd("  - A/B # comment")
    self.assertEqual(":/A\/B", result[0])
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
