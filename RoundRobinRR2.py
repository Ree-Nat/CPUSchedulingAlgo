import random
import queue

class process:
    def __init__(self):
        process_name: str
        process_burst_time : int
        burst_progress : int
        arrival_time : int
        start_time : int
        completion_time : int
        turnaround_time : int
        processed : bool 
    

#Generates list of jobs -> jobs.txt
def generate_jobs(job_amount : int, burst_range : tuple[int, int]):
    random_list = []
    for x in range(job_amount):
        burst_value = random.randrange(burst_range[0], burst_range[1])
        random_list.append((f"{x+1}", burst_value))
    return random_list

#Creates jobs file to be parsed into a list if true, job list ran successfully
def createJobFile(file_name : str, job_list: list) -> bool:
    with open(file_name, "w") as file:
        for job_name, job_burst_time in job_list:
            file.write(f"Job {job_name}\n")
            file.write(f"{job_burst_time}\n")
        file.close()
        return True 
    return False 

#The Round Robin algorithm that takes in a job file, the amount of jobs you want to process, and time slice or known
#as the quantum of the round robin algorithm that switches once time runs out or the quantum is less than the burst time
#Takes in file: job_file -> the file that contains the jobs
#Takes in job_amount -> integer: the amount of jobs you want to process
#time_slice -> integer: the time each process gets per clock interrupt
def RoundRobin(job_file : str, job_amount : int, time_slice):
        jobQueue = queue.Queue()
        with open(job_file, "r") as file:
            if int(len(file.readlines()))/2 < job_amount:
                raise ValueError(f"job amount cant exceed the amount of jobss in: {job_file}")    
            file.seek(0)
            for index, line in enumerate(file,start=0):
                if(index < job_amount):
                    new_process : process = process()
                    new_process.process_name = line.strip()
                    new_process.process_burst_time = int(file.readline().strip())
                    new_process.process_burst_progress = new_process.process_burst_time
                    new_process.arrival_time = 0 #all arrival time is set to 0
                    new_process.completion_time = new_process.arrival_time #all arrival time is set to 0
                    new_process.processed = False #all arrival time is set to 0
                    jobQueue.put(new_process)
            file.close()

        jobSize = jobQueue.qsize()
        currentTime : int = 0
        completedList = list()

        while not jobQueue.empty():
            current_job : process = jobQueue.get()
            if not current_job.processed: 
                current_job.start_time = currentTime
                current_job.processed = True 


            if current_job.process_burst_progress <= time_slice:
                current_job.completion_time = current_job.process_burst_progress + currentTime
                currentTime += current_job.process_burst_progress
                current_job.process_burst_progress =- time_slice
                current_job.turnaround_time = current_job.completion_time - current_job.arrival_time
                completedList.append(current_job)
            else:
                current_job.process_burst_progress -= time_slice
                currentTime += time_slice
                current_job.completion_time += currentTime
                jobQueue.put(current_job)


        print("Process name|process burst time|arrival time|start time|completion time|turn around time")
        totalTurnaround = 0
        for processItem in completedList:
            print(f"""{processItem.process_name}: {processItem.process_burst_time} {processItem.arrival_time} {processItem.start_time} {processItem.completion_time} {processItem.turnaround_time}""")
            totalTurnaround += processItem.turnaround_time ##adds the total turnaround time  
    
        averageTurnaround = totalTurnaround/jobSize
        print(f"Average turnaround time: {averageTurnaround}")
    
        return averageTurnaround


#RoundRobin("jobs.txt", 5, 2)
#RoundRobin("jobs.txt", 10, 2)
#RoundRobin("jobs.txt", 15, 2)


#gets the avergae of average for part 3 of project
#the number of trials to run the algorithm
#function the name of the scheduler algorithm
#*args arguments to the scheduler algorithm
def getAverageOfAverage(trials, func , *args):
    sum = 0
    for x in range(0, trials):
        createJobFile("part3jobs.txt", generate_jobs(15, (1, 30))) #Reset generator
        sum+= func(*args)
    return sum/trials

#createJobFile("Jobs.txt", generate_jobs(15, (1, 30)))#createJobFile() Note: This is the job, no trails for part 1c table
createJobFile("part3jobs.txt", generate_jobs(15, (1, 30))) #for part 3


averageOfAverageList = []
averageOfAverageList.append(getAverageOfAverage(5, RoundRobin, "part3jobs.txt", 5, 2))
averageOfAverageList.append(getAverageOfAverage(10, RoundRobin, "part3jobs.txt", 10, 2))
averageOfAverageList.append(getAverageOfAverage(15, RoundRobin, "part3jobs.txt", 15, 2))
print(f"averages with trials: 5 10 15: {averageOfAverageList}")

