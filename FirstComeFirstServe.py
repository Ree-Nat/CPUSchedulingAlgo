import random
import queue
import pandas as pd
import matplotlib.pyplot as plt

class process:
    def __init__(self):
        process_name: str
        process_burst_time : int
        arrival_time : int
        start_time : int
        completion_time : int
        turnaround_time : int 
    

#Generates list of jobs -> jobs.txt
def generate_jobs(job_amount : int, burst_range : tuple[int, int]):
    random_list = []
    for x in range(job_amount):
        burst_value = random.randint(burst_range[0], burst_range[1])
        random_list.append((f"{x+1}", burst_value))
    return random_list

#Creates jobs file to be parsed into a list if true, job list ran successfully
def createJobFile(file_name : str, job_list: list) -> bool:
    try:
        with open(file_name, "w") as file:
            for job_name, job_burst_time in job_list:
                file.write(f"Job {job_name}\n")
                file.write(f"{job_burst_time}\n")
            file.close()
            return True 
    except FileNotFoundError:
        raise FileNotFoundError(f"Job file not found {file_name}")
    return False 

#Runs first come first serve algorithm processing process by queue arrival time one by one 
#Takes in file: job_file -> the file that contains the jobs
#Takes in job_amount -> integer: the amount of jobs you want to process
def firstComeFirstServe(job_file : str, job_amount : int):
        if job_amount<0:
            raise(ValueError("job amount must be greater than 0"))
        
        jobQueue = queue.Queue()
        #Opens file and parse jobs from list
        lines = []
        try:
            with open(job_file, "r") as file:
                lines = [l.strip() for l in file if l.strip()]
                file.close()
        except FileNotFoundError:
            raise FileNotFoundError(f"Job file not found {job_file}")
        if int(len(lines) // 2 < job_amount):
            raise ValueError(f"job amount cant exceed the amount of jobs in: {job_file}")    
        for i in range(job_amount):
            new_process : process = process()
            new_process.process_name = lines[2*i]
            new_process.process_burst_time = int(lines[2*i + 1])
            if new_process.process_burst_time < 0:
                raise ValueError("No negative burst values")
            new_process.arrival_time = 0 #all arrival time is set to 0
            jobQueue.put(new_process)
        jobSize = jobQueue.qsize()
        currentTime : int = 0
        completedList = list()
        while not jobQueue.empty():
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
        averageTurnaround = totalTurnaround/job_amount
        print(f"Average turnaround time: {averageTurnaround}")
    
        return averageTurnaround

#gets the avergae of average for part 3 of project by regenerating jobs, getting its turnaround time and adding it up
#the number of trials to run the algorithm
#function the name of the scheduler algorithm
#*args arguments to the scheduler algorithm
def getAverageOfAverage(trials, func , *args):
    sum = 0
    for x in range(0, trials):
        sum+= func(*args)
    return sum/trials

#createJobFile("Jobs.txt", generate_jobs(15, (1, 30)))#createJobFile() Note: This is the job, no trails for part 1c table
#createJobFile("generatedJobs.txt", generate_jobs(15, (1, 30))) #for part 3

#for part 1, 2
#using jobs 5, 2, 7, 4, 3, 8, 3, 6, 9, 29, 3, 3, 15, 5, 12
turnaroundtimes = []
turnaroundtimes.append(firstComeFirstServe("jobs.txt", 5))
turnaroundtimes.append(firstComeFirstServe("jobs.txt", 10))
turnaroundtimes.append(firstComeFirstServe("jobs.txt", 15))

#for part 3
averageOfAverageList = []
averageOfAverageList.append(getAverageOfAverage(20, firstComeFirstServe, "generatedJobs.txt", 5))
averageOfAverageList.append(getAverageOfAverage(20, firstComeFirstServe, "generatedJobs.txt", 10))
averageOfAverageList.append(getAverageOfAverage(20, firstComeFirstServe, "generatedJobs.txt", 15))
print(f"FCFS Turnaround times for 5 10 15 jobs in jobs.txt: {turnaroundtimes}")
print(f"FCFS averages with 20 trials of 5 10 15 jobs in generatedJobs : {averageOfAverageList}")

job_counts = [5,10,15]

df = pd.DataFrame({
    "Job Count": job_counts,
    "Average Turnaround Time": turnaroundtimes
})
ax = df.plot(x="Job Count", y="Average Turnaround Time", marker = "o")
ax.set_title("FCFS Average Turnaround Time over Time ")
ax.set_ylabel("Average Turnaround Time")
plt.show()

print(df)
