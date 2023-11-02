#stage 1

#import json

#a = json.loads(input())

#def not_int(whatever_id):
#    return len([i[whatever_id] for i in a if type(i[whatever_id]) is not int])


#all_errors = {"bus_id": not_int("bus_id"),
#              "stop_id": not_int("stop_id"),
#              "stop_name": len([i["stop_name"] for i in a if type(i["stop_name"]) is not str or i["stop_name"] == ""]), 
#              "next_stop": not_int("next_stop"),
#              "stop_type": len([i["stop_type"] for i in a if type(i["stop_type"]) is not str or type(i["stop_type"]) is str and len(i["stop_type"]) > 1]),
#              "a_time": len([i["a_time"] for i in a if type(i["a_time"]) is not str or i["a_time"] == ""])
#              }

#print(f"Type and required field validation: {sum(all_errors.values())}")
#[print(f"{i}: {all_errors[i]}") for i in all_errors]

######################################

#stage 2

#import re
#import json

#datas = json.loads(input())

#all_errors = {"stop_name": len([1 for i in datas if not re.match(r"([A-Z]\w+ ?)+(Road|Avenue|Boulevard|Street)$", i["stop_name"])]), 
#              "stop_type": len([1 for i in datas if i["stop_type"] != "" and i["stop_type"] not in ["S", "O", "F"]]),
#              "a_time": len([1 for i in datas if not re.match(r"^(2[0-3]|1[0-9]|0[0-9]):([0-5][0-9])$", i["a_time"])])
#              }

#print(f"Type and required field validation: {sum(all_errors.values())}")
#[print(f"{i}: {all_errors[i]}") for i in all_errors]

#######################################

#stage 3

#import json

#datas = json.loads(input())

#all_errors = {i["bus_id"]:[] for i in datas}
#for i in datas:
#    all_errors[i["bus_id"]] += [i["stop_name"]]


#print("Line names and number of stops:")
#[print(f"bus_id: {i}, stops: {len(all_errors[i])}") for i in all_errors]

########################################

#stage 4

#import json

#datas = json.loads(input())

#def check_buslines():
#    all_errors = {i["bus_id"]:[] for i in datas}
#    for i in datas:
#        all_errors[i["bus_id"]].append(i["stop_type"]) 
#    for i in all_errors:
#        if "S" not in all_errors[i] or "F" not in all_errors[i]:
#            return i
        
#def stops(x):
#    stop_names = set(i["stop_name"] for i in datas if i["stop_type"] == x)
#    return f"{len(stop_names)} {sorted(stop_names)}"
    
#if check_buslines():
#    print("There is no start or end stop for the line:", check_buslines())
#else:
#    transfer = {i["stop_name"]:[] for i in datas}
#    for i in datas:
#        transfer[i["stop_name"]] += [i["bus_id"]]
#    transfer = [i for i in transfer if len(transfer[i]) > 1]
#    print("Start stops:", stops("S"))
#    print("Transfer stops:", len(transfer), sorted(transfer))
#    print("Finish stops:", stops("F"))

#########################################

#stage 5

#import json

#datas = json.loads(input())

#a = {i["bus_id"]:[] for i in datas}
#for i in datas:
#    hour, minute = i["a_time"].split(":")
#    what_to_add = [(i["stop_name"], i["stop_id"], int(hour)*3600 + int(minute)*60)]
#    a[i["bus_id"]] += sorted(what_to_add, key=lambda x: x[1])

#print("Arrival time test:")

#ri_no = 0
#for i in a:
#    for ii in range(len(a[i]) - 1):
#        if not a[i][ii][2] <= a[i][ii + 1][2]:
#           ri_no += 1
#           print(f"bus_id line {i}: wrong time on station {a[i][ii + 1][0]}") 
#            break   
#if not ri_no:
#    print("OK")

######################################

#stage 6

import json

datas = json.loads(input())

a = set(i["stop_name"] for i in datas if i["stop_type"] == "O")
transfer = {i["stop_name"]:[] for i in datas}
for i in datas:
    transfer[i["stop_name"]] += [i["bus_id"]]
transfer = [i for i in transfer if len(transfer[i]) > 1]
needed_stops = list(set.intersection(a, transfer))

print("On demand stops test:")
print("OK" if not needed_stops else f"Wrong stop type: {sorted(needed_stops)}")