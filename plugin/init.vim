let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
from vftest import *
EOF

function! EscapeLine(...)
    if a:0 == 0
      let line = getline(".")
    else
      let line = a:1
    endif
    let line = substitute(line, "\\", "\\\\\\\\", 'g')
    let line = substitute(line, "\"", "\\\\\"", 'g')
    return line
endfunction

function! LCmd(...)
    let line = EscapeLine()
    let pycmd = "LeaderCmd.extractLCmd(\"".line."\")"
    let results = py3eval(pycmd)
    if a:0 != 0
      echo results
      return ""
    endif
    if results[0] != ""
      execute results[0]
      normal! <cr>
      if results[1] != ""
        let @/ = results[1]
        "normal! k
      endif
    else
      echo "Nothing to execute"
      "normal! k
    endif
    if results[2] != ""
      "skip echo as that will wait for ENTER.
      echo results[2]
    endif
endfunction

function! LCmdTest(...)
    let line = EscapeLine()
    let pycmd = "LeaderCmd.extractLCmd(\"".line."\", True)"
    let results = py3eval(pycmd)
    echo results
endfunction

function! RunCmd(...)
    if a:0 == 1
      let line = getline('.')
      let direction = a:1
    else
      let line = a:1
      let direction = a:2
    endif
    let line = EscapeLine(line)
    let pycmd = "LeaderCmd.extractRunCmd(\"".line."\",\"".direction."\")"
    let ret = py3eval(pycmd)
    sleep 100m
    return ret
endfunction

function! RunCmdUntil(...)
    let direction = a:1
    let lnum = line('.')
    let line = trim(getline(lnum))
    let ret = ""
    while line != "" && line[0:2] != "```"
      let ret = RunCmd(line,direction)
      normal! j
      let lnum += 1
      let line = trim(getline(lnum))
    endwhile
    return ret
endfunction

function! Tryout()
    let a = RunCmdUntil("down")
"    let direction = "down"
"    let line = EscapeLine()
"    let pycmd = "LeaderCmd._extractRunCmd(\"".line."\",\"".direction."\")"
"    let ret = py3eval(pycmd)
"    echo ret
"    return ret
endfunction

nnoremap <leader>\ :call LCmd()<cr>
nnoremap <leader>T :call LCmdTest()<cr>
nnoremap <Leader><Right> :call RunCmd("right")<CR><Down>
nnoremap <Leader><Down> :call RunCmd("down")<CR><Down>
nnoremap <Leader><Up> :call RunCmd("up")<CR><Down>
nnoremap <Leader><Left> :call RunCmd("left")<CR><Down>

nnoremap `<Right> :call RunCmdUntil("right")<CR><CR>
nnoremap `<Down> :call RunCmdUntil("down")<CR><CR>
nnoremap `<Up> :call RunCmdUntil("up")<CR><CR>
nnoremap `<Left> :call RunCmdUntil("left")<CR><CR>

":map <Leader>z :call Tryout()<CR>
":map <Leader>z :call LCmd()<CR><CR>
" Used to debug RunCmd()
"function! LCTryout()
"    let direction = "down"
"    let line = getline(".")
"    let line = substitute(line, "\\", "\\\\\\\\", 'g')
"    let line = substitute(line, "\"", "\\\\\"", 'g')
"      " a = "\\" => a = \"-\\\\-\"
"      " a = '\\' => a = '-\\\\-'
"    "echo line
"    "return
"    "let pycmd = "LeaderCmd.tryout(\"".line."\")"
"    "let ret = py3eval(pycmd)
"    "  " a = "\\" => a = "-\\-"
"    "  " a = '\\' => a = '-\\-'
"    "echo ret
"    "return
"    let pycmd = "LeaderCmd.extractRunCmd(\"".line."\",\"".direction."\")"
"    let ret = py3eval(pycmd)
"    echo ret
"    "echo pycmd
"endfunction

