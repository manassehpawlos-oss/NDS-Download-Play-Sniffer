#!/bin/bash

sudo airmon-ng | tail -n +3 | cut -f 1,2
exit 0;
