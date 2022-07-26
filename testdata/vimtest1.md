# My Demo
- LCmd Demo # jump to the demo session
- @Open local file # make it clear is a marker
-: RunCmd Demo # --: +: ++: **: -- ++ ** also work too.
** RunCmdUntil Demo # --: +: ++: **: -- ++ ** also work too.

# LCmd Demo
## Open URL on your recently used browser
- https://github.com/vitalstarorg/vim-vfutils # comment
- [vim-vfutils](https://github.com/vitalstarorg/vim-vfutils) # comment

#! tmux split-window -hd
#! tmux split-window -vd
#: reg
#: ls
#: help
#: echo "hello"
#:python3 run_unittest()

## Open local file
- vimtest2.md
- @vimtest2.md # added @ as a reminder it is a redirection
- vimtest2.md@project file # open a file and jump to the marker
- vimtest2.md@new project

# RunCmd Demo1
```
ls # press \<down>, assume there is a pane below.
vim --version | grep python3
```

# RunCmd Demo2
```
#! tmux split-window -vd # press \\
ls # press \<down>
vim --version | grep python3
exit # close tmux pane below
```

# RunCmdUntil Demo
```
#! tmux split-window -vd # press \\ to open tmux pane below
clear # press `<down> to run until empty line or ```
python3
print("hello world!")
exit()
ls

```
