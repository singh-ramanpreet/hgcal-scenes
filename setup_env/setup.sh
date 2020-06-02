#!/bin/bash

DIR=$( dirname "${BASH_SOURCE[0]}" )
cd $DIR
source /cvmfs/sft.cern.ch/lcg/views/LCG_97python3/x86_64-centos7-gcc8-opt/setup.sh

export PYTHONUSERBASE=`pwd`
PY_VER=`python -c "import sys; print('python{0}.{1}'.format(*sys.version_info))"`
export PYTHONPATH=$PYTHONUSERBASE/lib/$PY_VER/site-packages:$PYTHONPATH
PATH=$PYTHONUSERBASE/bin:$PATH

if [[ ${1} == "with-install" ]]; then
    pip install --user -r requirements.txt
fi

cd -
