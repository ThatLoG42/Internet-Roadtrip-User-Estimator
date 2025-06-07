import requests
import json
import statistics
import threading

def main():
    readableOE()

def onlineEstimate():
    info = requests.get("https://roadtrip.pikarocks.dev/queryTime?limit=20")
    estimates = []
    stopJson = json.loads(info.text)
    reportedUserCount = stopJson["results"][0]["totalUsers"]
    print(f"Reported User Count: {reportedUserCount} drivers online")
    for stop in stopJson["results"]:
        voteResults = json.loads(stop["voteCounts"])
        voteCount = stop["voteCount"]
        if (len(voteResults) > 3):
            high = voteCount * 100/3
            mid = voteCount * 100/5
            eight = voteCount * 100/8
            low = voteCount * 100/10
            estimates += [high,mid,eight,low]
        else:
            two = voteCount * 100/2
            high = voteCount * 100/3
            mid = voteCount * 100/5
            low = voteCount * 100/7
            ten = voteCount * 100/10
            estimates += [two,low,mid,high,ten]  
    return (statistics.mean(estimates),statistics.stdev(estimates))


def readableOE():
    estimate = onlineEstimate()
    print(f"LoG42's Actual Online Estimate: {round(estimate[0],5)} ± {round(estimate[1],5)} drivers online\n")


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

main()