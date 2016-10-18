#!/bin/sh

dir_executable=executables
dir_objects=objects

assemblyFile="$1"
fileRoot=${assemblyFile%.*}
objectFile=${fileRoot}.o
executable=${fileRoot}

mkdir -p ${dir_executable}
mkdir -p ${dir_objects}

as "${assemblyFile}" -o "${dir_objects}"/"${objectFile}"
ld "${dir_objects}"/"${objectFile}" -o "${dir_executable}"/"$executable"
./"${dir_executable}"/"${executable}"
echo $?
