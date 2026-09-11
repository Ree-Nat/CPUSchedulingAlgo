import random
import queue
import pandas as pd 
import numpy as np 
from dataclasses import dataclass

class process:
    def __init__(self):
        process_name: str
        process_burst_time : int
        arrival_time : int
        start_time : int
        completion_time : int
        turnaround_time : int 
    


def generate_jobs(job_amount : int, burst_range : tuple[int, int]):
    random_list = []
    for x in range(job_amount):
        burst_value = random.randrange(burst_range[0], burst_range[1])
        random_list.append((f"{x+1}", burst_value))
    return random_list


def createJobFile(file_name : str, job_list: list) -> bool:
    with open("jobs.txt", "w") as file:
        for job_name, job_burst_time in job_list:
            file.write(f"Job {job_name}\n")
            file.write(f"{job_burst_time}\n")
        file.close()
        return True 
    return False 

def firstComeFirstServe(job_file : str):
        jobQueue = queue.Queue()
        with open(job_file, "r") as file:    
            for line in file:
                new_process : process = process()
                new_process.process_name = line.strip()
                new_process.process_burst_time = int(file.readline().strip())
                new_process.arrival_time = 0 #all arrival time is set to 0
                jobQueue.put(new_process)
            file.close()

        jobSize = jobQueue.qsize()
        currentTime : int = 0
        completedList = list()

        while not jobQueue.empty():
            starting_burst_time = currentTime
            current_job = jobQueue.get()
            current_job.start_time = currentTime
            currentTime += current_job.process_burst_time
            current_job.completion_time = currentTime
            current_job.turnaround_time = current_job.completion_time - current_job.arrival_time
            completedList.append(current_job)

        print("Process name|process burst time|arrival time|start time|completion time|turn around time")
        totalTurnaround = 0
        for processItem in completedList:
            print(f"""{processItem.process_name}: {processItem.process_burst_time} {processItem.arrival_time} {processItem.start_time} {processItem.completion_time} {processItem.turnaround_time}""")
            totalTurnaround += processItem.turnaround_time ##adds the total turnaround time  
    
        averageTurnaround = totalTurnaround/jobSize
        print(f"Average turnaround time: {averageTurnaround}")
    
        return completedList





createJobFile("jobs.txt", generate_jobs(10, (1, 30)))

firstComeFirstServe("jobs.txt")