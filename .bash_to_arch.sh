#!/bin/bash

F=$1

# out curr path
cur_folder=$(pwd)
cur_lesson=$(git branch --show-current)
arch_name="${cur_lesson}_${F}.zip"
cd ..

# arh
echo $arch_name 

zip -r $arch_name $cur_folder
