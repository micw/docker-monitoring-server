#!/usr/bin/python3 -u

import os
import jinja2

def filter_bool(value,true_value=True,false_value=False):
    if type(value) is not bool:
        value=str(value).lower() in ("true","on","1")
    
    if value:
        return true_value
    else:
        return false_value

def render_config(src):
    src=os.path.abspath(src)
    try:
        j2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('/'),
            trim_blocks=True,
            undefined=jinja2.StrictUndefined)
        j2_env.filters['bool']=filter_bool
        return j2_env.get_template(src).render(os.environ)
    except jinja2.exceptions.UndefinedError as e:
        print("Error creating config:",e)
        quit(1)

def process_config(src,dest):
    print("Creating config %s"%dest)
    rendered_template=render_config(src)
    with open(dest,'w') as out:
        out.write(rendered_template)

def exit_gracefully(signum, frame):
    print("Got stop signal, exiting")
    quit(0)

if __name__ == "__main__":

    import signal
    import subprocess

    process_config("/opt/thruk/etc/thruk_local.template.conf","/opt/thruk/etc/thruk_local.conf")
    process_config("/opt/thruk/etc/apache_thruk.template.conf","/etc/apache2/conf.d/zzz-thruk.conf")
    process_config("/opt/thruk/etc/log4perl.template.conf","/opt/thruk/etc/log4perl.conf")

    # create and pipe the thruk logfile
    thruk_logfile="/opt/thruk/var/log/thruk/thruk.log"
    subprocess.check_call(["touch",thruk_logfile])
    subprocess.check_call(["chown","apache.apache",thruk_logfile])
    subprocess.Popen(["tail","-f","-n","0",thruk_logfile])

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    result=subprocess.call(["httpd","-DFOREGROUND"])
    quit(result.returncode)
