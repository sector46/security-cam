#!/bin/bash
#python send_mail.py

if [ -f "security.conf" ]; then
  python motion_detection.py security.conf
else
  echo "run configure.sh first"
fi
