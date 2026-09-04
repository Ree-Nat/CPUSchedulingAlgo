import random


def generate_jobs(job_amount : int, burst_range : tuple[int, int]):
    random_list = []
    for x in range(job_amount):
        burst_value = random.randrange(burst_range[0], burst_range[1])
        random_list.append(burst_value)
    return random_list


print(generate_jobs(5, (0,20)))

