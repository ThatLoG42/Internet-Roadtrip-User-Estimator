import requests
import json
import statistics
# import threading

def main() -> None:
    readableOE()
    # set_interval(readableOE,30)

def onlineEstimate() -> tuple[float,float]:
    info = requests.get("https://roadtrip.pikarocks.dev/queryTime?limit=20")
    estimates: list[float] = []
    stopJson = json.loads(info.text)
    reportedUserCount = stopJson["results"][0]["totalUsers"]
    print(f"Reported User Count: {reportedUserCount} drivers online")
    for stop in stopJson["results"]:
        voteResults: dict = json.loads(stop["voteCounts"])
        voteCount: int = stop["voteCount"]
        if (len(voteResults) > 3):
            turnoutPercents = [3,5,8,10]
            for turnoutPercent in turnoutPercents:
                estimates.append(voteCount*100/turnoutPercent)
        else:
            turnoutPercents = [2,3,5,7,9]
            for turnoutPercent in turnoutPercents:
                estimates.append(voteCount*100/turnoutPercent) 
    return (statistics.mean(estimates),statistics.stdev(estimates))


def readableOE() -> None:
    estimate = onlineEstimate()
    print(f"LoG42's Actual Online Estimate (based on vote counts): {round(estimate[0],5)} ± {round(estimate[1],5)} drivers online\n")


# def set_interval(func, sec):
#     def func_wrapper():
#         set_interval(func, sec) 
#         func()  
#     t = threading.Timer(sec, func_wrapper)
#     t.start()
#     return t

main()