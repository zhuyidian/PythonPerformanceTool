#!/bin/bash


# 需要占用的 CPU 核心数，这里设置为 2
CPU_CORES=8


# 判断参数个数
if [ $# -ne 1 ]
then
  echo "Usage: $0 [start|stop]"
  exit 1
fi


if [ $1 == "start" ]
then
  # 在后台占用指定核心数的 CPU 资源
#  for (( i=1; i<=$CPU_CORES; i++ ))
  for i in $CPU_CORES
  do
    while true; do :; done &
  done
  echo "CPU stress test started."
elif [ $1 == "stop" ]
then
  # 停止占用 CPU 资源并清理进程
  for job in `jobs -p`
  do
    kill $job
  done
  echo "CPU stress test stopped."
else
  echo "Usage: $0 [start|stop]"
fi


#在终端中运行该脚本时，可以使用 ./script.sh start 启动 CPU 占用进程，并使用 ./script.sh stop 停止 CPU 占用进程。使用 ./script.sh start & 可以将脚本在后台运行。
#注意，在停止占用 CPU 资源时，使用 jobs + kill命令杀死了所有后台进程，因此如果系统中有其他&后台进程，可能会导致误杀其他进程。如果需要更精细的控制，请使用其他方式