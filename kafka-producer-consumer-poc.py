import asyncio
import json
from random import randint
from kafka import KafkaProducer, KafkaConsumer


async def producer():
    producer = KafkaProducer(
                    bootstrap_servers='localhost:9092',
                    value_serializer=lambda x: json.dumps(x).encode('utf-8')
                )
    for i in range(5):
        cnt = randint(1, 10)
        print("Start sending...")
        for j in range(cnt):
            msg = {"_id": i, "text": "hello world {}-{}".format(i, j)}
            producer.send('test_new', msg)
            producer.flush()
            print("produce [test_new]:  {}".format(json.dumps(msg)))
        await asyncio.sleep(2)
    producer.close()


async def consumer():
    consumer = KafkaConsumer(
                    bootstrap_servers='localhost:9092',
                    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                    # auto_offset_reset='earliest',
                    consumer_timeout_ms=1000)
    consumer.subscribe(['test_new'])
    while True:
        print("Start reading...")
        for msg in consumer:
            print("  consume [test_new]:  {}".format(msg.value))
        await asyncio.sleep(1)


if __name__ == '__main__':
    producer_coro = producer()
    consumer_coro = consumer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
    loop.close()
