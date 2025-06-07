import requests
import json
import statistics
from scipy import stats
from typing import Literal
# import threading

def main() -> None:
    info: requests.Response = requests.get("https://roadtrip.pikarocks.dev/queryTime?limit=20")
    reportedUserCount = json.loads(info.text)["results"][0]["totalUsers"]
    print(f"Reported User Count: {reportedUserCount} drivers online")
    readableOE(info)
    # set_interval(readableOE,30)

def onlineEstimate(info: requests.Response, type: Literal["mean","median"]) -> tuple[float,float]:
    estimates: list[float] = []
    stopJson = json.loads(info.text)
    for stop in stopJson["results"]:
        voteResults: dict = json.loads(stop["voteCounts"])
        voteCount: int = stop["voteCount"]
        if (len(voteResults) > 3):
            turnoutPercents = (3,5,8,10,12,15)
            for turnoutPercent in turnoutPercents:
                estimates.append(voteCount*100/turnoutPercent)
        else:
            turnoutPercents = (2,3,5,7,9,12)
            for turnoutPercent in turnoutPercents:
                estimates.append(voteCount*100/turnoutPercent) 
    if type == "median":
        return (statistics.median(estimates),stats.median_abs_deviation(estimates))
    elif type == "mean":
        return (statistics.mean(estimates),statistics.stdev(estimates))
    else:
        raise TypeError("Input must be either 'mean' or 'median'")


def readableOE(info: requests.Response) -> None:
    estimates = {"Mean": onlineEstimate(info, "mean"), "Median": onlineEstimate(info, "median")}
    for label, estimate in estimates.items():
        print(f"LoG42's {label}-based Actual Online Estimate (based on vote counts): {round(estimate[0],5)} ± {round(estimate[1],5)} drivers online")
    print("\n")


# def set_interval(func, sec):
#     def func_wrapper():
#         set_interval(func, sec) 
#         func()  
#     t = threading.Timer(sec, func_wrapper)
#     t.start()
#     return t

main()