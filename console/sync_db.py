#!/usr/bin/env python
import os
import sys
import datetime
import django
import logging

sys.path.append(os.path.abspath(__file__))

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "console.settings")

    django.setup()

    from _domain.core import Paths
    from _domain.utils import JsonDumper, FileWriter
    from traffic.generator import Generator

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info("Syncing monitoring settings from /opt/websafety/var/db/config.sqlite to /opt/websafety/etc/traffic/monitor.json...")

    f = os.path.join(Paths.etc_dir(), "traffic")

    logging.info("Generating monitor.json in folder %s" % f)
    
    g = Generator(f)
    w = FileWriter(f)
    d = JsonDumper()
    g.generate_monitor(w, d)

    logging.info("Success!!!")

    