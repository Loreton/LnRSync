#!/bin/bash


UUID_LN1TB_A="0EBE144A0EBE144A"
UUID_Lacie232GB_A="1448564A48562AAE"
UUID_Lacie232GB_B="B222175022171945"

# python3 /home/pi/Loreto/pyProc/LnMount.py $UUID_Lacie232GB_A
python3 /home/pi/Loreto/pyProc/LnMount.py $UUID_Lacie232GB_A
[[ ! "$?" == "0" ]] && exit
python3 /home/pi/Loreto/pyProc/LnMount.py $UUID_Lacie232GB_B
[[ ! "$?" == "0" ]] && exit
python3 /home/pi/Loreto/pyProc/LnMount.py $UUID_LN1TB_A
[[ ! "$?" == "0" ]] && exit

Project="PI_DiskToDisk"
Caption="Esecuzione: $Project"
echo $Caption

MAIN=../SOURCE/__main__.py
MAIN=../bin/LnRSync.zip

CMD="python3 $MAIN ../conf/LnRsync.ini $Project --go"
echo $CMD
$CMD
