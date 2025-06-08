import network
import requests as re
import time
import gc

nic = network.WIZNET5K()
nic.active(True)
nic.ifconfig()
nic.ifconfig("dhcp")
if (nic.isconnected()):
    print("Connected to the network")
else:
    print("Failed to connect to the network")

r= 0
start =0
gc.disable()


while True:
    login = input()
    password = input()
    print("Trying to login with {}:{}".format(login, password))
    gc.collect()
    start = time.ticks_cpu()
    r = re.get("http://192.168.1.1",auth=(login, password))
    end = time.ticks_cpu()
    print(r.status_code)
    print(time.ticks_diff(end, start))


# for i in range(1,10000000):
#     gc.collect()
#     start = time.ticks_cpu()
#     if i % 2 == 0:
#         r= re.get("http://192.168.1.1",auth=('admin', 'udmin'))
#         end = time.ticks_cpu()
#         short_avg += time.ticks_diff(end, start)

#     else:
#         r= re.get("http://192.168.1.1",auth=('admin', 'admik'))
#         end = time.ticks_cpu()
#         long_avg += time.ticks_diff(end, start)
#     # time it took in nanoseconds
    
#     print("Long AVG: {} us".format(long_avg // (i // 2 + 1)))
#     print("Short AVG: {} us".format(short_avg // ((i + 1) // 2)))
#     print("Response time: {} us".format(time.ticks_diff(end, start)))
#     # time.sleep(1)

    
