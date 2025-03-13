--This function gets surplus labour rate(=surplus value rate) from the sum of work time and the necessary labour time. The sum of work time minus the sum of necessary labour time is the sum of surplus labour time. this result divided by the sum of necessary labour time is the surplus labour rate. Pay attention to `1`. It represents the sum of necessary labour time.

getSurplusLabourRate work_time_sum worker_num necessary_labour_time = (work_time_sum / (worker_num * necessary_labour_time)) - 1

--It is easy to know that the work time equal to the sum of necessary labour time and surplus labour time. Now that surplus labour time equal to necessary multiplied by surplus labour rate.

getWorkTime necessary_labour_time surplus_labour_rate = necessary_labour_time + surplus_labour_time
    where surplus_labour_time = necessary_labour_time * surplus_labour_rate

-- the most interesting function.
getDerivativeOfSlrToWorkerNum work_time_sum necessary_labour_time worker_num = (-1) * (work_time_sum / necessary_labour_time) * (worker_num ** (-2))

-- edge condition of absolute surplus labour rate.
getEdgeOfSurplusLabourRate necessary_labour_time necessary_non_labour_time = (total_time_everyday / necessary_labour_time) - 1
    where total_time_everyday = 24 - necessary_non_labour_time
