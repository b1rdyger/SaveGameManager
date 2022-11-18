import re

from PyQt6.QtCore import QObject, pyqtSlot, pyqtBoundSignal

from app.SGMSignals.FCHSignals import FCHSignals
from app.SGMSignals.MFSSignals import MFSSignals


class SignalMemory(QObject):
    def __init__(self, func, method, param_tpes, message_box, message):
        super().__init__()
        self.func = func
        self.method = method
        self.slot = param_tpes
        self.message_box = message_box
        self.message = message

    def get_slot(self):
        match self.slot:
            case ['QString']:
                return self.parse_str
            case ['']:
                return self.parse
            case _:
                raise NotImplementedError('No pyqtSlot for signature ' + str(self.slot))

    @pyqtSlot()
    def parse(self):
        self.message_box.write(self.message)
        print(self.message)

    @pyqtSlot(str)
    def parse_str(self, q_str: str):
        self.message_box.write(self.message.replace('{str}', q_str))


class MessageByEvent(QObject):
    bind_list = []  # prevent cleanup

    def __init__(self, msg_box):
        super().__init__()
        self.msg_box = msg_box

        self.mfs_signals = MFSSignals()
        self.fch_signals = FCHSignals()

    def prepare(self):
        self.universal_bind(self.mfs_signals.symlinkCreated, 'Symlink created')
        self.universal_bind(self.mfs_signals.driveCreated, 'Drive [info:{str}:] created')
        self.universal_bind(self.fch_signals.restored, 'Savegame file restored')

    def universal_bind(self, fn, msg):
        f, m, p = self.extract_emitter(fn)
        sm = SignalMemory(f, m, p, self.msg_box, msg)
        self.bind_list.append(sm)
        fn.connect(sm.get_slot())

    @staticmethod
    def extract_emitter(fn) -> (str, str, str):
        sig_clazz = re.search('^<bound PYQT_SIGNAL (.*?)\\sof\\s(.*?)\\sobject at 0x.*', str(fn))
        params = re.search('.*\\((.*)\\)$', fn.signal)
        param_list = [parameter.strip() for parameter in params[1].split(',')]
        return sig_clazz[1], sig_clazz[2], param_list
