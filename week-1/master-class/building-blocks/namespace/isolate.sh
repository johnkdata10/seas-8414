#!/usr/bin/env bash

unshare --mount --uts --ipc --net --pid --fork --mount-proc $@
