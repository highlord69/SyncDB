from syncdb import SyncDB
from filedb import FileDB
import threading
import logging

FORMAT = '%(asctime)s.%(msecs)03d - %(message)s'
DATEFMT = '%H:%M:%S'


def test_write(db):
    logging.debug("started write test")
    for i in range(1000):
        assert db.set_value(i, "test" + str(i))


def test_read(db):
    logging.debug("started read test")
    for i in range(1000):
        assert "test" + str(i) == db.get_value(i)


def main():
    logging.debug("Starting tests for Multithreading")
    db = SyncDB(FileDB(), True)
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing simple write perms")
    p1 = threading.Thread(target=test_write, args=(db, ))
    p1.start()
    p1.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing simple read perms")
    p1 = threading.Thread(target=test_read, args=(db, ))
    p1.start()
    p1.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing read blocks writing")
    p1 = threading.Thread(target=test_read, args=(db, ))
    p2 = threading.Thread(target=test_write, args=(db, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing write blocks reading")
    p1 = threading.Thread(target=test_write, args=(db, ))
    p2 = threading.Thread(target=test_read, args=(db, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing multi reading perms possible")
    threads = []
    for i in range(5):
        thread = threading.Thread(target=test_read, args=(db, ))
        thread.start()
        threads.append(thread)
    for i in threads:
        i.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing load")
    threads = []
    for i in range(15):
        thread = threading.Thread(target=test_read, args=(db, ))
        thread.start()
        threads.append(thread)
    for i in range(5):
        p1 = threading.Thread(target=test_write, args=(db,))
        p1.start()
        threads.append(p1)
    for i in threads:
        i.join()
    logging.info("test successful")
    logging.debug("\n--------------------------------------------------------\n")
    logging.info("testing values stay correct")
    p1 = threading.Thread(target=test_read, args=(db,))
    p1.start()
    p1.join()
    logging.info("test successful")


if __name__ == '__main__':
    logging.basicConfig(filename="ThreadTest.log", filemode="a", level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
    main()
