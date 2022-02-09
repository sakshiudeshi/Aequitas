import multiprocessing as mp
import numpy as np
from scipy.optimize import basinhopping
import errno



def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def my_queue_get(queue, block=True, timeout=None):
    while True:
        try:
            return queue.get(block, timeout)
        except IOError as e:
            if e.errno != errno.EINTR:
                raise

def worker(fully_direct, local_inputs, minimizer, local_iteration_limit, out_q):
    for inp in local_inputs:
        basinhopping(fully_direct.evaluate_local, inp, stepsize=1.0, take_step=fully_direct.local_perturbation, 
                        minimizer_kwargs=minimizer, niter=local_iteration_limit)
    out_q.put([[fully_direct.local_disc_inputs, fully_direct.local_disc_inputs_list]])
    
def mp_basinhopping(fully_direct, minimizer, local_iteration_limit):
    out_q = mp.Queue()

    divided_lists = chunks(fully_direct.global_disc_inputs_list, 4)

    args = [(fully_direct, inputs, minimizer, local_iteration_limit, out_q) for inputs in divided_lists]

    nprocs = 4
    procs = []

    for i in range(nprocs):
        p = mp.Process(
                target=worker,
                args=args[i])
        procs.append(p)
        p.start()

    res = []
    for i in range(nprocs):
        res += my_queue_get(out_q)

    for p in procs:
        p.join()

    local_inputs = set()
    local_inputs_list  = []

    for pair in res:
        set_inputs = pair[0]
        list_inputs = pair[1]
        for item in set_inputs:
            if item not in local_inputs:
                local_inputs.add(item)
        for item in list_inputs:
            if item not in local_inputs_list:
                local_inputs_list.append(item)
    
    fully_direct.local_disc_inputs = local_inputs
    fully_direct.local_disc_inputs_list = local_inputs_list

    return fully_direct







