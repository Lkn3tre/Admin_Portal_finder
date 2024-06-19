thread_num = 1 
hits = []
import requests, os, sys, argparse, threading, queue, random
try:
    from tqdm import tqdm
except:
    print("[!] Missing modules: tqdm")
    sys.exit(1)


# Parsing arguments
args = []
parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True, help="[?] Enter a target url.")
parser.add_argument("--status", required=True, nargs='+', help="[?] Filter status codes.")
parser.add_argument("--thread", required=False, help="[?] Enter the number of thread you want")
parser.add_argument("--tor", required=True, help="[?] Use tor proxy (1/0)")
args = parser.parse_args()
global q
if args.thread is not None:
        thread_num = int(args.thread)

targeturl = str(args.url)

wlist = open('adminpanellinks.txt','r').read().split('\n')

# Checking how many words in that list and putting in queue
count=0
q = queue.Queue()
for w in wlist:
    q.put(w)
    count+=1 

# Outputs
print(f"[+] Target URL: {targeturl}")
print(f"[+] Status Codes: {args.status}")
print(f"[+] Request using Tor proxy: {args.tor}")
print(f"[+] Number of threads: {args.thread}")
print(f"\n[+] Checking directories please wait...")
print("\n") 

def get_random_agents():
	with open("user-agent.txt", "r") as ua:
		for line in ua:
			rua = random.choice(list(ua))
			agent = {"user-agent": rua.rstrip()}
			return agent

def get_tor_session():
    session = requests.session()
    # default socks port 9050 for Tor
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

def finder():
    counter = 0
    if args.tor == '1':
    	session = get_tor_session()
    else:
    	session = requests.session()
    try:
        while not q.empty():
            directorie = q.get()
            userAgent = get_random_agents()
            url = '{}/{}'.format(targeturl,directorie)
            r = session.get(url,headers=userAgent)
            ret = f'{r.status_code}'           
            if ret in args.status:
                print(f"[*] Status {ret} => {url}")
                hits.append((url,ret))

    except KeyboardInterrupt:
        print(f"\n[!] Program terminated by user.")

# Handling threads
ts = []
for i in range(0,thread_num):
    try:
        t = threading.Thread(target=finder)
        ts.append(t)
        t.start()
    except Exception as e:
        print(e)
for t in ts:
    t.join()
