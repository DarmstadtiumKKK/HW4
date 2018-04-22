from abc import ABCMeta, abstractmethod

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

    def poisk_num(self, key, id):
        list_of_task=self._data[key]
        for i in range(len(list_of_task)):
            if str(list_of_task[i].get_id()) == id:
                return i


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


