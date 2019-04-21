from threading import Thread
from .scanner import monitor


def threader(system_config, overseer_config):
    threads = []

    for each_section in overseer_config.config.sections():
        t = Thread(target=monitor, args=(system_config,
                                         overseer_config,
                                         each_section))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
