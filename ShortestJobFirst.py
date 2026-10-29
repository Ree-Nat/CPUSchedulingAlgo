import random
import heapq

class process:
    def __init__(self):
        process_name: str
        process_burst_time : int
        arrival_time : int
        start_time : int
        completion_time : int
        turnaround_time : int 

    #For heap implementation

    def val(self):
        return self.process_burst_time

    def __it__(self, other):
        return self.process_burst_time <= other.process_burst_time

    def __eq__(self, other):
        return self.val() == other.val()

    def __lt__(self, other):
        return self.val() < other.val()

    

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

#Runs the shortest job first algorithm by processing nonpreemitiely the process with the shortest burst time by using a heap 
#to organize the processes
#job_amount -> the amount of jobs you want to process in the file
#job_file ->the name of the file
def shortestJobFirst(job_file : str, job_amount : int):
        jobHeap = []
        lines = []

        try:
            with open(job_file, "r") as file:
                lines = [l.strip() for l in file if l.strip()]
                file.close()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found{job_file}")

        if int(len(lines)) //2 < job_amount:
            raise ValueError(f"job amount cant exceed the amount of jobs in: {job_file}")    
        for i in range(job_amount):
            new_process : process = process()
            new_process.process_name = lines[2*i]
            new_process.process_burst_time = int(lines[2*i + 1])
            if new_process.process_burst_time < 0:
                            raise ValueError("No negative burst values")
            new_process.arrival_time = 0 #all arrival time is set to 0
            heapq.heappush(jobHeap, new_process)
        file.close()

        jobSize = len(jobHeap)
        currentTime : int = 0
        completedList = list()

        while not len(jobHeap) == 0:
            starting_burst_time = currentTime
            current_job = heapq.heappop(jobHeap)
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
    
        return averageTurnaround

#shortestJobFirst("jobs.txt", 5)
#shortestJobFirst("jobs.txt", 10)
#shortestJobFirst("jobs.txt", 15)


#gets the avergae of average for part 3 of project by regenerating jobs, getting its turnaround time and adding it up
#the number of trials to run the algorithm
#function the name of the scheduler algorithm
#*args arguments to the scheduler algorithm
def getAverageOfAverage(trials, func , *args):
    sum = 0
    for x in range(0, trials):
        sum+= func(*args)
    return sum/trials

#createJobFile("jobs.txt", generate_jobs(15, (1, 30)))#createJobFile() Note: This is the job, no trails for part 1c table
#createJobFile("generatedJobs.txt", generate_jobs(15, (1, 30))) #for part 3

#for part 1, 2
#using jobs 5, 2, 7, 4, 3, 8, 3, 6, 9, 29, 3, 3, 15, 5, 12
turnaroundtimes = []
turnaroundtimes.append(shortestJobFirst("jobs.txt", 5))
turnaroundtimes.append(shortestJobFirst("jobs.txt", 10))
turnaroundtimes.append(shortestJobFirst("jobs.txt", 15))

#for part 3
averageOfAverageList = []
averageOfAverageList.append(getAverageOfAverage(20, shortestJobFirst, "generatedJobs.txt", 5))
averageOfAverageList.append(getAverageOfAverage(20, shortestJobFirst, "generatedJobs.txt", 10))
averageOfAverageList.append(getAverageOfAverage(20, shortestJobFirst, "generatedJobs.txt", 15))
print(f"SJF Turnaround times for 5 10 15 jobs in jobs.txt: {turnaroundtimes}")
print(f"SJF averages with 20 trials of 5 10 15 jobs in generatedJobs : {averageOfAverageList}")
