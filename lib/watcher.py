from threading import Thread
from .scanner import monitor

def threader(overseer_config):
    threads = []

    for each_section in overseer_config.config.sections():
        t = Thread(target=monitor, args=(overseer_config, each_section))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
