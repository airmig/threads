import random
import time
import concurrent.futures
import threading
import logging
import queue

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s')

class Pipeline(queue.Queue):
    def __init__(self):
        self.capacity = super().__init__(maxsize=20)

    def set_message(self, message):
        print(f'processing {message}')
        producer_pipeline.append(message)
        self.put(message)

    def get_message(self):
        message = self.get()
        print(f'consuming {message}')
        consumer_pipeline.append(message)
        return message

def producer(pipeline, event):
    logging.info("producing")
    while not event.is_set():
        message = random.randint(1, 100)
        pipeline.set_message(message)

def consumer(pipeline, event):
    logging.info("consuming")
    while not pipeline.empty() or not event.is_set():
        logging.info(f"processing message queue. queue size: {pipeline.qsize()}")
        message = pipeline.get_message()
        time.sleep(random.random())

producer_pipeline = []
consumer_pipeline = []

if __name__ == '__main__':
    pipeline= Pipeline()
    event = threading.Event() # True or False .set(), .reset() .clear() initially false
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as worker:
        worker.submit(producer, pipeline, event)
        worker.submit(consumer, pipeline,event)
        time.sleep(0.5)
        event.set()
    print(f'producer: {producer_pipeline}')
    print(f'consumer: {consumer_pipeline}')
