#!/usr/bin/env python3

import sys
import docker_entrypoint

if len(sys.argv)!=2:
    print ("USAGE: %s TEMPLATE"%__file__)
    quit(1)

print(docker_entrypoint.render_config(sys.argv[1]))