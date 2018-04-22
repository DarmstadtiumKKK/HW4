import socket
import os
from datetime import datetime, date, time
from classes import Struckt_of_Queue, Task

class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('127.0.0.1', 5555))
        self.sock.listen(1)
        self.data_of_queue = Struckt_of_Queue('1', 0, {})
        self.sock.setblocking(0)

    def run(self):
        self._restore()
        try:
            while True:
                while True:
                    try: conn, addr = self.sock.accept()
                    except socket.error:
                        break
                    else:
                        data = conn.recv(10000000)
                        arguments = data.decode('utf-8').split(' ')
                        result=eval('self._'+arguments[0].lower())(arguments)
                        conn.send(bytes(result, 'utf-8'))
                        conn.close()
                        self._archive()
                self._check_timeout()
        except KeyboardInterrupt:
            return None

    def _add(self, ars):
        if not self.data_of_queue.exsist(ars[1]):
            # создание новой очереди если нужная отсутствует
            self.data_of_queue.creating(ars[1])
        # добавление данных в нужную очередь
        id = self.data_of_queue.adding(ars)
        return str(id)

    def _in(self, ars):
        data=self.data_of_queue.get_data()
        list_of_task=data[ars[1]]
        for i in range(len(list_of_task)):
            if str(list_of_task[i].get_id()) == ars[2]:
                return 'YES'
        return  'NO'

    def _get(self, ars):
        list_of_task = self.data_of_queue.get_data()[ars[1]]
        for i in range(len(list_of_task)):
            if not list_of_task[i].get_status():
                self.data_of_queue._data[ars[1]][i]._status=True
                self.data_of_queue._data[ars[1]][i]._date_of_take=datetime.now()
                return str(list_of_task[i].get_id())+' '+list_of_task[i].get_length()+' '+list_of_task[i].get_data()
        return 'NONE'

    def _ack(self, ars):
        check=self._in(ars)
        if check == 'YES':
            data=self.data_of_queue.get_data()
            data[ars[1]].pop(self.data_of_queue.poisk_num(ars[1], ars[2]))
        return check

    def _restore(self):
        if not os.path.exists("restore_file.txt"):
            return None
        data_dict={}
        restore_file = open('restore_file.txt', 'r')
        for line in restore_file:
            arguments = line.split(' ')
            if arguments[0]=='queue':
                key = arguments[1][: len(arguments[1]) - 1]
                data_dict[key]=[]
            else:
                if arguments[0]=='task':
                    key = arguments[1]
                    current_task = Task(int(arguments[2]), arguments[3], arguments[4],key)
                    current_task._status=arguments[5]
                    current_task._date_of_take = datetime.strptime(arguments[6])
                    data_dict[key].append(current_task)
                else:
                    self.data_of_queue._current_id=int(arguments[0])
        self.data_of_queue._data=data_dict
        restore_file.close()
        return None

    def _archive(self):
        archive_file = open('restore_file.txt', 'w')
        data_dict=self.data_of_queue.get_data()
        keys=list(data_dict.keys())
        values=list(data_dict.values())
        for i in range(len(values)):
            line='queue '+keys[i]+'\n'
            archive_file.write(line)
            for item in values:
                for j in range(len(item)):
                    line='task '+keys[i]+' '+str(item[j].get_id())+' '+item[j].get_length()+' '+item[j].get_data()+' '+str(item[j].get_status())+' '+str(item[j]._date_of_take)+'\n'
                    archive_file.write(line)
        archive_file.write(str(self.data_of_queue._current_id))
        archive_file.close()
        return None

    def _check_timeout(self):
        now_time=datetime.now()
        current_data=self.data_of_queue.get_data()
        data_values=list(current_data.values())
        for current_list in data_values:
            for task in current_list:
                if task._date_of_take is not None:
                    delta = now_time - task._date_of_take
                    if delta.seconds>300:
                        self._remove_from_queue(self,task)

    def _remove_from_queue(self,task):
        self.data_of_queue._data[task._num_of_queue].remove(task)
        task._status=False
        task._date_of_take = None
        self.data_of_queue._data[task._num_of_queue].append(task)


if __name__ == '__main__':
    serv = Server()
    serv.run()
