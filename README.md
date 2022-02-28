# vim-vfutils
`vim-vfutils` has a set helper features for vim with tmux on macos to help with creating a devops runbook. Below features are helping to manage multiple project files and run documented commands to avoid copy & paste.

1. Navigate within a file, preferably a markdown file.
2. Navigate to different project file.
3. Open URL on the browser, helpful to manage & document multiple URLs
4. Multiple way to run a single or multiple commands to adjacent tmux pane or on vim itself.t

Make sure your vim supports python3.
```
$ vim --version | grep +python3
+python3
```

![demo](testdata/vfutils.gif)

# Install
Add the following line to `~/.vimrc`
```
call plug#begin('~/.vim/plugged')
Plug 'vitalstarorg/vim-vfutils'
call plug#end()
```

# Default Config
```
let mapleader = '\'

" LCmd
nnoremap <leader>\ :call LCmd()<cr><cr>

" RunCmd
nnoremap <Leader><Right> :call RunCmd("right")<CR><Down>
nnoremap <Leader><Down> :call RunCmd("down")<CR><Down>
nnoremap <Leader><Up> :call RunCmd("up")<CR><Down>
nnoremap <Leader><Left> :call RunCmd("left")<CR><Down>

" RunUntil
nnoremap `<Right> :call RunCmdUntil("right")<CR><CR>
nnoremap `<Down> :call RunCmdUntil("down")<CR><CR>
nnoremap `<Up> :call RunCmdUntil("up")<CR><CR>
nnoremap `<Left> :call RunCmdUntil("left")<CR><CR>
```

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

# Execute hashbang #!command as shell command
#! tmux split-window -hd
#! tmux split-window -vd

# Execute vimbang #:command as vim command
#:reg
#:help
```

# RunCmd
Send the line to a neighbouring tmux pane and execute. `\<down>` `\<right>` `\<up>` `\<left>` specifies which pane the line will be executed.

```
# Open a tmux pane around the main pane, before you try these 4 commands
cd python
ls
vi leadercmd.py
```

# RunCmdUntil
```
Similar to RunCmd, but run the line and following lines until an empty line or ```. `<down> `<right> `<up> `<left> specifies which pane the line will be executed.
```

```bash
# Open a tmux pane around the main pane, before you try these 4 commands
cd python
ls
vi leadercmd.py

```
