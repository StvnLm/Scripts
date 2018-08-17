
#!/usr/bin/python
"""
This is a script to execute 2 commands:
1) WGET command to retrieve certificate revocation lists from https://pub.ac.carillon.ca/CRL/.
2) Run openSSL on the retrieved files, append to a new "certToConnector.log" file.
3.a) If there is no certToConnector.log in the main directory, it will take the oldest file from the buffer directory.
It will also rename all certToConnectorX.log files in the buffer directory; where X is counter, decrementing it by 1.
Example: file1.log, file2.log -> file0.log, file1.log 
3.b) If there is a certToConnector.log in the main directory, it will simply add the latest log to the buffer directory
with the name certToConnectorX.log, where X is the highest counter.
To execute the script, simply run ./python <script name>
TODO:
-Delete the file when read by smartconnector. This can be done by storing the file creation date in the filename, and
checking the file "atime". However, this has the issue that file can possibly get deleted if a user opens it. Ideally, 
connector will delete a file when it reads the log source. 
"""
__author__ = "Steven Lam"
__version__ = "1.0.0"


import os, subprocess

def WgetCRL(file_name):
    # Using open os.DEVNULL since stdout=subprocess.DEVNULL not in Py2.
    with open(os.devnull, 'w') as FNULL:
        base_url = "https://XXXXXXXXXXXXXXXXXX.ca/CRL/"
        full_link = base_url + file_name
        subprocess.call(["wget", "--no-check-certificate", full_link, "-O", file_name], stdin=FNULL, stdout=FNULL, stderr=FNULL)


def OpenSSL(base_dir, file_list):
    # Clear contents of the certToConnector file.
    with open(base_dir + "certToConnector.log", "w+") as f:
        pass
    # Append the contents of the openSSL output to the certToConnector.log file.
    with open(os.devnull, 'w') as FNULL:
        for file in file_list:
            input = base_dir + file
            with open(base_dir + "certToConnector.log", "a") as log:
                log.flush()
                subprocess.call(["openssl", "crl", "-inform", "DER", "-in", input, "-text", "-noout"], stdin=FNULL, stdout=log,
                                stderr=FNULL)


def OpenSSLBuffer(base_dir, file_list):
    """
    In the event that a connector goes down, and the script is running - a rotating file cache is required.
    OpenSSLBuffer will place the processed files into a directory called buffer, and then move a single log file into the
    main directory if there is no certToConnector*.log file present.
    """
    buffer_dir = base_dir + "buffer/"
    if not os.path.exists(buffer_dir):
        os.makedirs(buffer_dir)
    # Append the contents of the openSSL output to the certToConnector.log file.
    index = 0
    rotating_file = "certToConnector{}.log".format(index)
    # Checks if a log file already exists. If so, check for the next log file index to be used.
    while os.path.exists(buffer_dir + rotating_file):
        index += 1
        rotating_file = "certToConnector{}.log".format(index)
    with open(os.devnull, 'w') as FNULL:
        # Writes content to buffer log file
        with open(buffer_dir + rotating_file, "a+") as log:
            for file in file_list:
                input = base_dir + file
                log.flush()
                subprocess.call(["openssl", "crl", "-inform", "DER", "-in", input, "-text", "-noout"], stdin=FNULL, stdout=log,
                                stderr=FNULL)


def PluckLog(base_dir):
    """
    If base directory does not have a certToConnector.log file, it will take the oldest from the buffer directory.
    First in, first out. This helps ensure events are read sequentially.
    """
    if not os.path.isfile(base_dir + "certToConnector.log"):
        try:
            # Grab oldest file from buffer and place in main directory.
            old_file, new_file = base_dir + "buffer/certToConnector0.log", base_dir + "certToConnector.log"
            subprocess.call("mv {} {}".format(old_file, new_file), shell=True)
            # Re-name files in buffer directory
            numFiles = len([name for name in os.listdir('/home/stelam/buffer/') if "certToConnector" in name])
            for n in range(1, numFiles + 1):
                old_file = base_dir + "buffer/certToConnector{}.log".format(str(n))
                new_file = base_dir + "buffer/certToConnector{}.log".format(str(n-1))
                os.rename(old_file, new_file)
        # FileNotFound not in Py2
        except Exception as e:
            pass


if __name__ == '__main__':
    crl_list = ["AAAAAAA.crl", "BBBBBB.crl", "CCCCCCC.crl"]
    base_dir = "/home/stelam/"

    for file in crl_list:
        WgetCRL(file)
        # Older script that kept 1 log file.
        # OpenSSL(base_dir, crl_list)
    OpenSSLBuffer(base_dir, crl_list)
    PluckLog(base_dir)
