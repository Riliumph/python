#!/bin/bash

bash_completion=$HOME/.config/bash_completion
mkdir -p ${bash_completion}

if type docker &> /dev/null; then
  docker completion bash > ${bash_completion}/docker
  echo 'source $HOME/.config/bash_completion/docker' >> $HOME/.bashrc
fi
if type pip  &> /dev/null; then
  pip completion --bash > ${bash_completion}/pip
  echo 'source $HOME/.config/bash_completion/pip' >> $HOME/.bashrc
fi
