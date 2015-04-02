#!/bin/bash

    thisDir="$(dirname  "$(test -L "$0" && readlink "$0" || echo "$0")")"     # risolve anche eventuali LINK presenti sullo script
    thisDir=$(cd $(dirname "$thisDir"); pwd -P)/$(basename "$thisDir")        # GET AbsolutePath
    baseDir=${thisDir%/.*}                                                      # Remove /. finale (se esiste)
    parentDir=${baseDir%/bin}                                               # Remove /bin finale (se esiste)
    parentDir="$(dirname $baseDir)"
    sourceDir="${parentDir}/SOURCE"
    binDir="${parentDir}/bin"
    confDir="${parentDir}/conf"


    mainProgram="$binDir/LnRSync.zip"
    if [[ ! -f "$mainProgram" ]]; then
        mainProgram="$sourceDir/__main__.py"
    fi

    [[ ! -f "$mainProgram"  ]] && echo "$mainProgram non esiste!" && exit 1


    Project="save2Git"
    Caption="Esecuzione: $Project"
    echo $Caption

    CMD="python3 $mainProgram $confDir/LnRSync.ini $Project --go"
    echo $CMD

    $CMD

    # Project="PI_LacieA_1TB"
    # Caption="Esecuzione: $Project"
    # echo $Caption

    # CMD="python3 $mainProgram $confDir/PI_DiskToDisk.ini $Project --go"
    # echo $CMD

    # $CMD
