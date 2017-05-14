import json
import transmissionrpc


# load configs
auth = []
with open('auth.json', 'r') as fp:
        auth = json.load(fp)

finished={}
try:
        fp = open('finished.json', 'r')
        finished = json.load(fp)
except:
        pass


# login transmissionrpc
print( "authenticate rpc server..."+auth['address'])
try:
        tc = transmissionrpc.Client(auth['address'], port=auth['port'],
                user=auth['user'], password=auth['password'])
except Exception as e:
        print(str(e))
        exit(1)

print("update finished json ...")
ts = []
try:
        ts = tc.get_torrents()
except Exception as e:
        print(str(e))
        exit(1)

for t in ts:
        if t.isFinished:
                print(t.name, 'is finished')
                finished.update({ t.hashString : t.name })

print("write back ...")
with open('finished.json', 'w') as fp:
        json.dump(finished,fp)

