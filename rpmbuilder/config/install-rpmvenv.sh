#!/bin/bash

pip install rpmvenv
cd /mnt
QA_SKIP_BUILD_ROOT=1 rpmvenv rpm-config.json