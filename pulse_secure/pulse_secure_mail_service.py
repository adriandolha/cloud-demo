import base64
import datetime
import logging
import servicemanager
import socket
import win32event
import win32service
from logging.handlers import RotatingFileHandler
from threading import Thread

import psutil
import pythoncom
import win32com.client
import win32serviceutil

log_path = "c:/apps/cloud_demo/pulse_secure/output.log"
logging.basicConfig(level=logging.DEBUG)

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().addHandler(RotatingFileHandler(filename=log_path, maxBytes=500, backupCount=2))


def encode(key):
    return base64.b64encode(key)


def decode(key):
    return base64.b64decode(key)


def disconnect_pulse_secure():
    process = get_pulse_secure_service()
    if not process:
        logging.info('No Pulse Secure Service Found.')
    logging.info(f'Killing za process {process}')
    process.kill()
    process.terminate()
    logging.info(f'Killed za process {process}')


def get_all_processes():
    return [psutil.Process(pid) for pid in psutil.pids()]


def get_pulse_secure_service():
    services = [process for process in get_all_processes() if 'PulseVpn'.lower() in process.name().lower()]
    if len(services) == 0:
        return None
    return services[0]


class Handler_Class(object):
    def OnNewMailEx(self, receivedItemsIDs):
        logging.debug(f'New mail received {datetime.datetime.now()}')
        # RecrivedItemIDs is a collection of mail IDs separated by a ",".
        # You know, sometimes more than 1 mail is received at the same moment.
        try:
            for ID in receivedItemsIDs.split(","):
                mail = outlook.Session.GetItemFromID(ID)
                subject = mail.Subject
                if str(subject).lower() == 'pssd':
                    logging.debug(f'Received Pulse Secure Disconnect mail with subject {subject}')
                    disconnect_pulse_secure()
        except Exception as e:
            logging.error(e)


class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "PulseSecureDisconnectService"
    _svc_display_name_ = "Pulse Secure Disconnect Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        rc = None
        mail_thread = Thread(target=MailHandler().process)
        logging.info(f'Started service at {datetime.datetime.now()}')
        while rc != win32event.WAIT_OBJECT_0:
            # block for 24*60*60 seconds and wait for a stop event
            # it is used for a one-day loop
            mail_thread.start()
            rc = win32event.WaitForSingleObject(self.hWaitStop, 24 * 60 * 60 * 1000)
        logging.info(f'Stopped service at {datetime.datetime.now()}')


if __name__ == '__main__':
    # win32serviceutil.HandleCommandLine(AppServerSvc)
    logging.info('Connecting Outlook...')
    outlook = win32com.client.DispatchWithEvents("Outlook.Application", Handler_Class)
    logging.info('Waiting from pulse secure messages...')
    pythoncom.PumpMessages()
