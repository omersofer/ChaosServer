import httplib

httpServ = httplib.HTTPConnection("127.0.0.1", 8000)
httpServ.connect()

http200Count = 0
http401Count = 0
http500Count = 0
n = 100  # number of iterations in each call

for a in range(0,n):
    httpServ.request('GET', "/response/")
    response = httpServ.getresponse()
    if response.status == 200:
        http200Count += 1
    elif response.status == 401:
        http401Count += 1
    elif response.status == 500:
        http500Count += 1

print "Probed the /response endpoint " + str(n) + " times"
print "got: " + str("%.2f" % ((http200Count / (n*1.0))*100)) + "% 200 http responses"
print "     " + str("%.2f" % ((http401Count / (n*1.0))*100)) + "% 401 http responses"
print "     " + str("%.2f" % ((http500Count / (n*1.0))*100)) + "% 500 http responses"

httpServ.close()
