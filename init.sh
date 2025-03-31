#!/bin/bash

set -m

iris session iris -U%SYS '##class(Security.Users).UnExpireUserPasswords("*")'

fg %1