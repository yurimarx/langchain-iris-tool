#!/bin/bash

set -m

iris session iris -U%SYS '##class(Security.Users).UnExpireUserPasswords("*")'

# streamlit run /home/irisowner/dev/src/python/rag/main.py --server.port=8501 --server.address=0.0.0.0 --global.developmentMode=false

fg %1