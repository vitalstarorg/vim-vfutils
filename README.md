# vim-vfutils
`vim-vfutils` has a set helper features for vim with tmux.

# LCmd
In vim normal mode, type `\\` on the line below, it will trigger different function. `\` is used as the leader.
```
# Open any url find in the line on your last used browser
xxx https://github.com/vitalstarorg/vim-vfutils
xxx [vim-vfutils](https://github.com/vitalstarorg/vim-vfutils)

# Open a local file python/leadercmd.py on new tmux window.
# It must be in xxxx.yy format
xxx python/leadercmd.py
xxx @python/leadercmd.py
xxx @@python/leadercmd.py

# Search for the marker on local file
xxx @LCmd
xxx @ LCmd
xxx @ LCmd # jump to LCmd

# Search for the marker on local file e.g. plantuml mindmap multi-line format
-: LCmd
--: LCmd
+: LCmd
++: LCmd
*: LCmd
**: LCmd
**: LCmd # jump to LCmd

# Search for the marker on local file e.g. plantuml mindmap format
xxx - LCmd
xxx -- LCmd
xxx + LCmd
xxx ++ LCmd
xxx * LCmd
xxx ** LCmd
xxx ** LCmd # jump to LCmd
```

# RunCmd
```
Send the line to a neighbouring tmux pane and execute. `\<down>` `\<right>` `\<up>` `\<left>` specifies which pane the line will be executed.
```
```bash
# Open a tmux pane around the main pane, before you try these 4 command
cd python
ls
vi leadercmd.py

```

# RunCmdUntil
```
Similar to RunCmd, but run the line and following lines until an empty line or ```. `<down> `<right> `<up> `<left> specifies which pane the line will be executed.
```

```bash
# Open a tmux pane around the main pane, before you try these 4 command
cd python
ls
vi leadercmd.py

```
