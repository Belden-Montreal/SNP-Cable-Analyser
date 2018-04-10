import multiprocessing.Pool as ThreadPool
import time

def f(x):
    print x**x

if __name__ == '__main__':
    start_time = time.time()

    pool = multiprocessing.Pool() #use all available cores, otherwise specify the number you want as an argument
    for i in xrange(0, 512):
        pool.apply_async(f, args=(i,))
    pool.close()
    pool.join()

    print("--- %s seconds ---" % (time.time() - start_time))
