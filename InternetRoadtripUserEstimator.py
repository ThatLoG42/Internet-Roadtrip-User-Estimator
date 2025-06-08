import requests
import json
import statistics
from scipy import stats
from typing import Literal

def main() -> None:
    info: requests.Response = requests.get("https://roadtrip.pikarocks.dev/queryTime?limit=100")
    reportedUserCount = json.loads(info.text)["results"][0]["totalUsers"]
    print(f"Reported User Count: {reportedUserCount} drivers online")
    readableOE(info)

def onlineEstimate(info: requests.Response, typeStat: Literal["mean","median"]) -> tuple[float,float]:
    estimates: list[float] = []
    stopJson = json.loads(info.text)
    stops: list = stopJson["results"]
    fwdStreak = 0
    turnStreak = 0
    for idx, stop in enumerate(reversed(stops)):
        voteResults: dict = json.loads(stop["voteCounts"])
        voteCount: int = stop["voteCount"]
        ## pre-check for boredom level based on first n-20 of last n stops (n = 100 rn)
        if (idx < len(stops) - 20):
            if (len(voteResults) > 3):
                turnStreak += 1
            else:
                fwdStreak += 1
            continue
        if (len(voteResults) > 3):
            turnStreak += 1
            # checks for boredom level
            if (fwdStreak >= 8):
                turnoutPercents = (3,5,8,10)
            elif (fwdStreak >= 6):
                turnoutPercents = (3,5,8,10,11)
            elif (fwdStreak >= 4):
                turnoutPercents = (3,5,8,10,12)
            else:
                turnoutPercents = (3,5,8,10,12,14)
            fwdStreak = 0
            #checks for locked-in level
            if (turnStreak >= 5):
                turnoutPercents = (3,5,8,10,12,15,16)
            elif (turnStreak >= 3):
                turnoutPercents = (3,5,8,10,12,15)
            for turnoutPercent in turnoutPercents:
                estimates.append(voteCount*100/turnoutPercent)
        else:
            fwdStreak += 1
            #checks bordeom level
            if fwdStreak >= 6:
                turnoutPercents = (2,3,5,7,9)
            elif fwdStreak == 5:
                turnoutPercents = (2,3,5,7,9,10)
            elif fwdStreak == 4:
                turnoutPercents = (2,3,5,7,9,11)
            else:
                turnoutPercents = (2,3,5,7,9,12)
            
            for turnoutPercent in turnoutPercents:
                estimates.append(voteCount*100/turnoutPercent) 
    if typeStat == "median":
        return (statistics.median(estimates),stats.median_abs_deviation(estimates))
    elif typeStat == "mean":
        return (statistics.mean(estimates),statistics.stdev(estimates))
    else:
        raise TypeError("Input must be either 'mean' or 'median'")


def readableOE(info: requests.Response) -> None:
    estimates = {"Mean": onlineEstimate(info, "mean"), "Median": onlineEstimate(info, "median")}
    for label, estimate in estimates.items():
        print(f"LoG42's {label}-based Actual Online Estimate (based on vote counts): {round(estimate[0],5)} ± {round(estimate[1],5)} drivers online")

main()