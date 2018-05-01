import socket
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
        self.timeout = 300
        self.dict_of_action={'ADD':[4, self._add],'GET':[2,self._get],'ACK':[3,self._ack],'IN':[3,self._in]}

    def _check_correct(self,args):
        if self.dict_of_action.get(args[0]) is not None:
            if len(args)==self.dict_of_action[args[0]][0]:
                return self.dict_of_action[args[0]][1]
        return TypeError

    def run(self):
        self.data_of_queue.restore()
        try:
            while True:
                self.data_of_queue._check_timeout(self.timeout)
                while True:
                    try: conn, addr = self.sock.accept()
                    except socket.error:
                        break
                    else:
                        data = conn.recv(10000000)
                        arguments = data.decode('utf-8').split(' ')
                        fun=self._check_correct(arguments)
                        result=fun(arguments)
                        conn.send(bytes(result, 'utf-8'))
                        conn.close()
                        self.data_of_queue.archive()
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
        return self.data_of_queue.is_consisting(ars)

    def _get(self, ars):
        return self.data_of_queue.get_task(ars[1])

    def _ack(self, ars):
        check=self._in(ars)
        if check == 'YES':
            self.data_of_queue.remove(ars[1],ars[2])
        return check





if __name__ == '__main__':
    serv = Server()
    serv.run()
