#!/bin/bash
# xclip installation: sudo apt-get install -y xclip

str=(`xclip -o -selection clipboard`);echo ${str[2]} | cut -c8-
