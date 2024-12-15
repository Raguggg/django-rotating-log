import logging

k = 0
while True:
    k += 1
    logging.info("This is a test log message %s", k)
    import time

    time.sleep(1)
