#!/bin/bash
#
    # echo $len - $baseDir
    # echo ${baseDir:$len-1:1}
    # echo ${baseDir#*.}
    # baseDir=$(cd $(dirname "$0"); pwd -P)/$(basename "$0")
    len=$(expr length "$baseDir")


    baseDir="$(dirname  "$(test -L "$0" && readlink "$0" || echo "$0")")"     # risolve anche eventuali LINK presenti sullo script
    baseDir=$(cd $(dirname "$baseDir"); pwd -P)/$(basename "$baseDir")        # GET AbsolutePath

    baseDir=${baseDir%/.*}                                                    # Remove /. finale (se esiste)
    # baseDir=${baseDir%/bin*}                                                  # Remove /bin finale (se esiste)

    sourceDir="${baseDir}/SOURCE"

    if [ -d "$sourceDir"  ]; then
        echo python "$sourceDir/__main__.py" $*

    else
        echo python "$baseDir/LnRSync.zip" $*

    fi

    exit 0
