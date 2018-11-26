from app.libs.enums import PendingStatus
from datetime import date

class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data = []
        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)



class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.data = {}
        self.data = self.__prase(drift, current_user_id)


    def requester_or_gifter(self, drift, current_user_id):
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are


    def __prase(self, drift, current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': date.fromtimestamp(drift.create_time),
            'message': drift.message,
            'address': drift.address,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending,
            'status_str':pending_status,
            'operator': drift.requester_nickname if you_are != 'requester' else drift.gifter_nickname
        }
        return r
