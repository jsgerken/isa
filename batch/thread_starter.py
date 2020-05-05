#!/usr/bin/python
import threading
import time
import batch
import count_logs
import logger


def main():
    all_threads = []
    # Making threads
    batch_thread = threading.Thread(target=batch.main)
    logger_thread = threading.Thread(target=logger.main)
    count_logs_thread = threading.Thread(target=count_logs.main)

    # starting threads
    batch_thread.start()
    logger_thread.start()
    count_logs_thread.start()

    # appending to array
    all_threads.append(batch_thread)
    all_threads.append(logger_thread)
    all_threads.append(count_logs_thread)

    # wait for all threads to complete which they will never do
    for t in all_threads:
        t.join()


if __name__ == "__main__":
    main()
