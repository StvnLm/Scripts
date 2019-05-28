import os
import json
import socket
import requests
import logging
import datetime

class Proofpoint():
    """
    __author__ = "Steven Lam"
    __Version__ = "1.0"

    Proofpoint.py is to be used to pull events from the Proofpoint REST API using the configuration parameters specified
    within the Proofpoint_config.json file. The class will perform the following steps:
    1. Ensure folder structure is available
    2. Attempt to pull logs via the Proofpoint REST API
    3. Record the events in a flat log file
    4. Attempt to send events to the smartconnector on a listener port
    """

    def __init__(self, config):
        """
        :param config: Configuration file for the script
        """
        with open(config) as f:
            self.config = json.load(f)


    def make_files(self):
        """
        Ensures the necessary directories & files exist on the OS, otherwise create.
        :param path: takes the full path of the log file
        :return: None
        """
        logs = [self.config["log"]["test_path"], self.config["log"]["filename"]]
        err_logs = [self.config["error_logging"]["log_file"], self.config["error_logging"]["filename"]]
        log_list = [logs, err_logs]
        for log in log_list:
            try:
                os.makedirs(log[0])
                logging.warning(f"Making directory - {log[0]}")
            except FileExistsError:
                pass
            # Creates log files in the directories if they do not exist
            file_path = f"{log[0]}/{log[1]}"
            if not os.path.isfile(file_path):
                with open(file_path, "a+") as f:
                    logging.warning(f"Making file - {log[0]}{log[1]}")
                    f.close()


    def get_proofpoint_logs(self, api_endpoint, params):
        """
        Gets the proofpoint logs from the REST API
        :param api_endpoint: URL Endpoint of the REST API
        :param params: Parameters attached to the REST API request; takes interval in seconds and log format
        :return: Response from REST API, otherwise log to error log file
        """
        session = requests.Session()
        session.auth = (self.config["auth"]["client_id"],self.config["auth"]["client_secret"])
        response = session.get(url=api_endpoint, params=params)
        try:
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.warning(f"Error getting logs - {e}")


    def send_logs_from_resp(self, resp, host, port):
        """
        Sends logs to the smartconnector; writes to a log file if there is no active TCP session available (SC is down)
        :param resp: Text output of the REST API output
        :param host: Address of the startconnector
        :param port: TCP listener port of the smartconnector
        :return: None
        """
        resp = resp.split('\n')
        try:
            for line in resp:
                if len(line) <= 1:
                    continue
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, int(port)))
                s.sendall(line.encode())
                s.close()
                return True
        except Exception as e:
            logging.error(f"Error sending logs to connector - {e}")
            filepath = self.config["log"]["test_path"] + self.config["log"]["filename"]
            # Writes logs retrieved from REST API and writes to logs to a cache file
            with open(filepath, "a+") as fr:
                [fr.write(f"{line}\n") for line in resp if len(line) > 1]
                return False


    def send_logs_from_file(self, host, port):
        """
        Reads cache log file to send logs from and attempts to send to a TCP listener.
        :param host: Address of smartconnector
        :param port: Port used to communicate with smartconnector
        :return: None
        """
        logfile_path = self.config["log"]["test_path"] + self.config["log"]["filename"]
        try:
            # Send logs from flat file to smartconnector
            if os.stat(logfile_path).st_size > 0:
                with open(logfile_path, "r") as fr:
                    lines = fr.readlines()
                    for line in lines:
                        if len(line) <= 1:
                            continue
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((host, int(port)))
                        s.sendall(line.encode())
                        s.close()
                # Clear logfile once all logs are sent
                with open(logfile_path, "w+") as fw:
                    fw.close()
                    return True
        except Exception:
            logging.error(f"Error while sending logs from file - {Exception}")
            return False


    def cache_time(self):
        last_run_dt = datetime.datetime(
                day = _.config["timetracker"]["day"],
                month = _.config["timetracker"]["month"],
                year = _.config["timetracker"]["year"],
                hour = _.config["timetracker"]["hour"],
                minute = _.config["timetracker"]["minute"]
                )
        if (datetime.datetime.now() - last_run_dt).seconds / 3600 > 1:
            return True, last_run_dt


    def increment_time(self):

        pass


if __name__ == '__main__':

    # Logging setup
    logging.basicConfig(
    filename="testlogger.log",
    # filename = f"{self.config['error_logging']['log_file']}/{self.config['error_logging']['filename']}",
    level = logging.INFO,
    format = "%(asctime)s - Function %(funcName)s | Message: %(message)s",
    datefmt= "%Y-%m-%d %H:%M:%S"
    )

    _ = Proofpoint("Proofpoint_config.json")
    _.make_files() # Create directories as needed
    host = _.config["arcsight_connection"]["connector_ip"]
    port = _.config["arcsight_connection"]["port"]
    catch_up = _.cache_time()

    # Send HTTP request until interval is caught up to current datetime
    while catch_up[0] is True:
        # Parameters for HTTP request
        params = {
                "logformat": "syslog",
                "interval": f"2019-05-23T12:00:00Z/2019-05-23T13:00:00Z"
                }

        logs = _.get_proofpoint_logs("https://tap-api-v2.proofpoint.com/v2/siem/all/", params=params)
        _.increment_time()
        _.send_logs_from_file(host=host, port=port)
        _.send_logs_from_resp(logs, host=host, port=port)
