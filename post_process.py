import json
import datetime

DURATION = 5

def load_predict():
    with open("predict_{}s.txt".format(DURATION), "r") as fp:
        data = json.load(fp)
    
    return data


def group_timeslots(timeslots):
    # if current timeslot is only 5 seconds
    # and there have a 30s gap to next timeslots
    # then current timeslot is noise
    # if not, then merge current timeslot to next timeslot
    grouped_timeslots = []
    i = 0
    while i < len(timeslots) - 1:
        current_start, current_end = timeslots[i]
        next_start, next_end = timeslots[i + 1]

        # Check if the current timeslot is only 5 seconds and there is a 30s gap to the next timeslot
        if current_end - current_start == DURATION and next_start - current_end >= 30:
            # The current timeslot is noise, skip it
            i += 1
            continue

        # Merge the current timeslot with the next timeslot
        while i < len(timeslots) - 1 and next_start - current_end < 30:
            i += 1
            current_end = max(current_end, next_end)
            if i < len(timeslots) - 1:
                next_start, next_end = timeslots[i + 1]

        grouped_timeslots.append([current_start, current_end])
        i += 1

    # Handle the last timeslot
    if timeslots and (not grouped_timeslots or timeslots[-1][1] > grouped_timeslots[-1][1]):
        grouped_timeslots.append(timeslots[-1])

    return grouped_timeslots
    

if __name__ == "__main__":
    data = load_predict()
    result = []
    for predict in data:
        timeslots = group_timeslots(predict["periods"])
        timeslots = [[str(datetime.timedelta(seconds=it[0])), str(datetime.timedelta(seconds=it[1]))] for it in timeslots]
        result.append({"stream": predict["stream"], "singing": timeslots})

    with open("result_{}s.json".format(DURATION), "w") as fp:
        json.dump(result, fp, indent=4)