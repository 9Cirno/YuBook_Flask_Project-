from enum import Enum

class PendingStatus(Enum):
    Waiting = 1
    Success = 2
    Reject = 3
    Redraw = 4

    @classmethod
    def pending_str(cls, status, key):
        key_map = {
            cls.Waiting:{
                'requester':'wait opposite shipment',
                'gifter': 'wait your shipment'
            },
            cls.Reject: {
                'requester': 'opposite refused your request',
                'gifter': 'you refused request'
            },
            cls.Redraw: {
                'requester': 'you cancelled',
                'gifter': 'opposite cancelled'
            },
            cls.Success: {
                'requester': 'opposite shipped',
                'gifter': 'you shipped'
            }

        }
        return key_map[status][key]
