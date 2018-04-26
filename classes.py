from abc import ABCMeta, abstractmethod
from datetime import datetime, date, time

# class StandData(metaclass=ABCMeta):

class StandStruckt(metaclass=ABCMeta):

    def __init__(self, id, length, data):
        self._id = id
        self._length = length
        self._data = data

    def get_id(self):
        return self._id

    def get_length(self):
        return self._length

    def get_data(self):
        return self._data


    '''@abstractmethod
    def _processing(self, result):
        pass'''

class Struckt_of_Queue(StandStruckt):
    _current_id=0

    def exsist(self, key):
            if self._data.get(key) is None:
                return False
            else:
                return True

    def adding(self, arguments):
        current_task=Task(self._current_id,arguments[2],arguments[3],arguments[1])
        self._data[arguments[1]].append(current_task)
        self._current_id += 1
        return current_task._id

    def creating(self, key):
        self._data[key] = []

    def is_consisting(self, ars):
        data=self.get_data()
        list_of_task = data[ars[1]]
        for i in range(len(list_of_task)):
            if str(list_of_task[i].get_id()) == ars[2]:
                return 'YES'
        return 'NO'

    def get_task(self, queue_name):
        list_of_task = self.get_data()[queue_name]
        for i in range(len(list_of_task)):
            if not list_of_task[i].get_status():
                self._data[queue_name][i]._status = True
                list_of_task[i]._date_of_take = datetime.strftime(datetime.now(), "%H:%M:%S")
                return str(list_of_task[i].get_id()) + ' ' + list_of_task[i].get_length() + ' ' + list_of_task[
                    i].get_data()
        return 'NONE'

    def poisk_num(self, key, id):
        list_of_task=self._data[key]
        for i in range(len(list_of_task)):
            if str(list_of_task[i].get_id()) == id:
                return i

    def remove(self, queue_name, task_id):
        data = self.get_data()
        data[queue_name].pop(self.poisk_num(queue_name, task_id))

    def _check_timeout(self, timeout=0):
        current_data = self.get_data()
        data_values = list(current_data.values())
        for current_list in data_values:
            for task in current_list:
                task.check_timeout(timeout)


class Task(StandStruckt):

    def __init__(self, id, length, data, numb):
        super().__init__(id, length, data,)
        self._status=False # False - не выполняется, True - выполняется
        self._num_of_queue=numb
        self._date_of_take=None

    def get_status(self):
        return self._status

    def get_num(self):
        return self._num_of_queue

    def check_timeout(self, timeout=0):
        now_time=datetime.now()
        if self._date_of_take is not None:
            past_time = datetime.strptime(self._date_of_take, "%H:%M:%S")
            delta = now_time - past_time
            if delta.seconds > timeout:
                self._status = False
                self._date_of_take = None



