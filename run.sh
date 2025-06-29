#!/bin/bash

if [ $BUILD_TYPE = "Release" ]; then
flask run --host=0.0.0.0
elif [ $BUILD_TYPE = "Debug" ]; then 
python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 ./task_manager.py
fi