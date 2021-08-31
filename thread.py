import threading
import time
import concurrent.futures

lock = threading.Lock()
print(lock)
lock.acquire()
print(lock)
lock.release()
print(lock)
print(threading.current_thread())
def init():
    return True


def f(name):
    print(f'func1 started with {name}')
    time.sleep(5)
    print(f'func1 {name} ended')

def f2(name):
    print(f'func2 started with {name}')
    time.sleep(5)
    print(f'func2 {name} ended')

"""
Use rlock to not deadlock
"""
class Account:
    def __init__(self):
        self.balance = 100
        self.lock = threading.Lock()
    def update(self, transaction, amount):
        print(f'{transaction} thread updating')
        with self.lock:
            local_copy = self.balance
            local_copy += amount
            time.sleep(1)
            self.balance = local_copy
        print(f'{transaction} thread ending')

"""
daemon=True allows to terminate threads that have not finished
"""
if __name__ == "__main__":
    print('main started')
    account = Account()
    print(f'starting with balance of {account.balance}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
        #e.map(f, ['foo', 'bar', 'baz'])[]
        #e.map(f2, ['second map'])
        for transaction, amount in [('deposit', 50), ('withdrawal', -150)]:
            e.submit(account.update, transaction, amount)
    print(f'ending balance of {account.balance}')

    print('main ended')
