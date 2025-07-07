#!/bin/bash
cd /home/f/disks/c_os_staff/FarraHella_Bot/
git reset --hard
git pull
source /home/f/disks/c_os_staff/FarraHella_Bot/.venv/bin/activate
/home/f/disks/c_os_staff/FarraHella_Bot/.venv/bin/python3.8 /home/f/disks/c_os_staff/FarraHella_Bot/FarraHella_main.py
