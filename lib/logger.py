from .date import get_current_datetime
import os, time

def write_log(host, msg_type, error_string):
    # Is file already open?
    log_file = "log/" + host + "/" + host + ".log"
    log_dir = "log/" + host
    scans_dir = "log/" + host + "/scans"

    if os.path.exists(log_file):
        try:
            os.rename(log_file, log_file)
            with open(log_file, "a") as log:
                log.write(host + ',' + str(get_current_datetime()) + ',' + msg_type + ',' + str(error_string) +'\n')
                log.close()
        except OSError as e:
            print("[-] Error: File is already open... waiting until available...")
    else:
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
            os.mkdir(scans_dir)
        
        # Wait 5 seconds... then try again
        time.sleep(5)
        with open(log_file, "a") as log:
            log.write(host + ',' + str(get_current_datetime()) + ',' + msg_type + ',' + str(error_string) +'\n')
            log.close()
            

