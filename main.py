import sys


class Video:
    def __init__(self, id, size):
        self.size = size
        self.id = id


class Server:
    def __init__(self, id,capacity, nep):
        self.id = id
        self.cap = capacity
        self.nep = nep
        self.latency_from_endpoints = self.initelr()
        self.vids = []

    def add_vid(self, video):
        if video not in self.vids:
            self.vids.append(video)
            self.cap -= video.size



    def initelr(self):
        result = [-1 for i in range(self.nep)]
        return result

    def getLatFromEndpoint(self, endpoint):
        slcs = endpoint.slcs
        return slcs[self.id]


class Endpoint:
    def __init__(self, id, servers, dl):
        self.id = id
        self.dlc = dl
        self.servers = servers

    def getSuitableServer(self,video):
        swvc = [x for x in self.servers if x.cap > video.size]
        if len(swvc) > 0:
            swvc.sort(key=lambda x: x.latency_from_endpoints[self.id])
            return swvc[0]
        else:
            return "dc"


    def nthServerWithShortestLatency(self, n):
        self.servers.sort(key=lambda x: x.latency_from_endpoints[self.id])
        return self.servers[0]

    def getServerFromLatency(self, lc):
        for server in self.servers:
            if server.latency_from_endpoints[self.id] == lc:
                return server


class Request:
    def __init__(self, vid_id, epid, number):
        self.vid_id = vid_id
        self.epid = epid
        self.number = number


class Stream:
    def __init__(self, videos, endpoints, servers, requests):
        self.videos = videos
        self.endpoints = endpoints
        self.requests = requests
        self.commands = []
        self.servers = servers

    def move(self, csid, videos):
        cmd = "%d %s" % (csid, " ".join([str(n.id) for n in videos]))
        self.commands.append(cmd)

    def writeout(self, ofile):
        ofi = open(ofile, "w")
        ofi.write(str(len(self.commands)) + "\n")
        for line in self.commands:
            ofi.write(line + "\n")
        ofi.close()




    # def gswl(self, lc, eps):
    #     for server in eps:
    #         if (lc in server.elr):
    #             return server
    #     return 0

    def solve(self):
        self.requests.sort(key=lambda req:req.number, reverse=True)
        for j in  range(len(self.requests)):
            request = self.requests[j]
            video_requested = self.videos[request.vid_id]
            ep_requested_from = self.endpoints[request.epid]
            swsl = ep_requested_from.getSuitableServer(video_requested)
            print "for request %d of %d coming from endpoint %d"%(j,len(self.requests),ep_requested_from.id)
            if swsl == "dc":
                #datacenter
                continue
            # print "capacity of server is %d and video size is %d"%(swsl.cap,video_requested.size)
            # while swsl!="dc" and swsl.cap - video_requested.size < 0:
            #     ep_requested_from.servers.remove(swsl)
            #     swsl = ep_requested_from.nthServerWithShortestLatency(i)
                # print "swsl is %s"%(str(swsl))
            else:
                # print "best server is gotten and video is added"
                swsl.add_vid(video_requested)
                # print "new capacity of server %d is %d"%(swsl.id,swsl.cap)
                # print "now server %d now contains %d videos"%(swsl.id,len(swsl.vids))
        for server in self.servers:
            self.move(server.id,server.vids)

def rFile(ifile):
    ifi = open(ifile, "r")
    # print("%s input file opened" % ifile)
    requests = []
    endpoints = []
    nv, ne, nr, ns, ccs = [int(n) for n in ifi.readline().split()]
    #print "first line read %d %d %d %d %d" % (nv, ne, nr, ns, ccs)
    video_sizes = [int(n) for n in ifi.readline().split()]
    videos = [Video(i,video_sizes[i]) for i in range(nv)]
    servers = [Server(xs,ccs,ne) for xs in range(ns)]
    for ep in range(ne):
        dlc, ncachs = [int(n) for n in ifi.readline().split()]
        ep_servers = []
        for cachs in range(ncachs):
            csid, cslc = [int(n) for n in ifi.readline().split()]
            nserver = servers[csid]
            nserver.latency_from_endpoints[ep] = cslc
            ep_servers.append(nserver)
            # if(containServer(servers,nserver)== False):
            #     servers.append(nserver)
        endpoints.append(Endpoint(ep, ep_servers, dlc))
        # endpoints.append(Endpoint(ep,dlc,servers)) ||| Error
    for re in range(nr):
        video_id, epid, nrr = [int(n) for n in ifi.readline().split()]
        requests.append(Request(video_id, epid, nrr))
    # print "we have %d number of requests"%(len(requests))
    ifi.close()
    return Stream(videos, endpoints, servers, requests);


def main():
    # print sys.argv
    ifile = sys.argv[1]
    ofile = sys.argv[2]
    # ifile = "trending_today.in"
    # ofile = "tt.out"
    stream = rFile(ifile);
    # print "done reading file"
    stream.solve()
    # print "streaming is solved"
    stream.writeout(ofile)
    # print "file is written out and finished"


if __name__ == "__main__":
    main()
