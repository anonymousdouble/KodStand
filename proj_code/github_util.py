import os,github,random,requests, traceback,time
from retry import retry
from urllib import request
from bs4 import BeautifulSoup
token_list = [["e02f6b8737478d3f6d6ee1b88ff285607fed6ce1"], ["9c34a60a61bfcb213b52d8b388f577f34c379987"],
              ["6499ee7e5d6186145d50660df4d2594ebb8af0d2"], ['70d784b8f5c5e2cdf4c01f71a0769745f3267645'],
              ['048a88f0c2a738c34e8feb91bb2e1ff5fecebb3d'],['83f3c3fcbfcd1b859686bb00eec6758d62be691e'],
              ['a0dee2601787fe47bf454c4c9915a53eaa390d9d'],['a5ff35e73df8d403e322248a50c7c4eee257e8e5'],
              ['4e50e7b9268fb4f37ac4b83fb6e08a7cbdbd0165'],['507bf00003474eb421af8bd00177c707a017a61b'],
              ['b06b37b6dfd433a2ab51106e32ce25e1e64dcc4f'],['5df9357a04a35b7c66e4b2de4125168eb182ae86'],
              ['3cb8a39fa0bff0fcf859fda44637f9fdec01f465'],['f673d467fb02362e6206e15e129c37e75e3c50e9'],
              ['2fb194c37a1128477dc0ce79d68fc60dbb46c911'],['0a90527ccd836f6afe99f831e487a1c2ced91078'],
              ['be03b9532e2d288f3cea9171fd53836161d7ce74']]
issues_payload = {"per_page": 100,"page": 1,"state": "all" }
num_count=0
@retry(delay=0, tries=6,backoff=1, max_delay=120)
def crawl_issue_html_copy(issue_url):
    # f = request.urlopen(issue_url)
    token_list_my =["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",

                            "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"]

    # opener = request.build_opener()
    response = requests.get(issue_url, headers={'Authorization': f"token {token_list_my[random.randint(0,len(token_list_my)-1)]}"}, timeout=10)

    soup = BeautifulSoup(response.text, 'html.parser')
    # print(">>>soup: ", soup)
    # response = opener.open(f).read()  # f.read()

    return soup
@retry(delay=0, tries=6,backoff=1, max_delay=120)
def crawl_issue_html(issue_url):
    # f = request.urlopen(issue_url)
    token_list_my = ["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",
                     "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",
                     "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"]

    # opener = request.build_opener()
    response = requests.get(issue_url, headers={'Authorization': f"token {token_list_my[random.randint(0,len(token_list_my)-1)]}"}, timeout=10)

    soup = BeautifulSoup(response.text, 'html.parser')
    # print(">>>soup: ", soup)
    # response = opener.open(f).read()  # f.read()

    return soup

def clone_pro(pro_path,url):
    #=
    repo_name = url.split('/')[-1]
    # if repo_name=="covid-19-data":
    #     return 1,repo_name
    if not os.path.exists(pro_path):
        os.makedirs(pro_path)

    os.chdir(pro_path)
    repo_html_url = url
    clone = "git clone " + repo_html_url

    if os.path.exists(pro_path + repo_name + "/"):
        print(pro_path + repo_name + " has existed!")
        return 2,repo_name

    else:

        os.system(clone)  # Cloning
        print(pro_path + repo_name + " is successfully cloned!**************")
        return 1,repo_name
def get_user(query):
    count = 0
    while count < 5:
        try:
            # print("get num querry: ",query)
            global num_count
            num_count += 1
            count += 1
            r = requests.get(query,
                             headers={'Authorization': 'token %s' % get_token()})
            res = r.json()

            try:

                    login=res["login"]
                    return res

            except Exception as e:
                traceback.print_exc()
                print("res: ",query, res, r.headers)
                time.sleep(2)
                continue

        except Exception as e:
            print("error: ", res)
            traceback.print_exc()
            time.sleep(2)
            continue

    return None

def get_comments(query):
    count = 0
    while count < 5:
        try:
            # print("get num querry: ",query)
            global num_count
            num_count += 1
            count += 1
            r = requests.get(query,
                             headers={'Authorization': 'token %s' % get_token()})
            res = r.json()

            try:
                if isinstance(res, list):
                    return res
                else:
                    continue

            except Exception as e:
                traceback.print_exc()
                print("res: ", res, r.headers)
                time.sleep(2)
                continue

        except Exception as e:
            print("error: ", res)
            traceback.print_exc()
            time.sleep(2)
            continue

    return None


def get_commit(query):
    count = 0
    while count < 5:
        try:
            # print("get num querry: ",query)
            global num_count
            num_count += 1
            count += 1
            r = requests.get(query,
                             headers={'Authorization': 'token %s' % get_token()})
            res = r.json()

            try:

                num = res['sha']

                return res
            except Exception as e:
                traceback.print_exc()
                #print("res: ", res, r.headers)
                time.sleep(2)
                continue

        except Exception as e:
            print("error: ", res)
            traceback.print_exc()
            time.sleep(2)
            continue

    return None

def get_token(num=None):
    if num:
        return token_list[num%len(token_list)][0]
    else:
        return token_list[random.randint(0,len(token_list)-1)][0]
def get_respo_star(query):
    count = 0
    while count < 5:
        try:
            print("get num querry: ",query)
            global num_count
            num_count += 1
            count += 1
            r = requests.get(query,
                             headers={'Authorization': 'token %s' % get_token(num_count)})
            res = r.json()

            try:
                stargazers_count=res['stargazers_count']
                language = res['language']
                return stargazers_count,language
            except Exception as e:
                traceback.print_exc()
                print("res: ",r.headers)
                time.sleep(2)
                continue

        except Exception as e:
            print("error: ", repr(e))
            traceback.print_exc()
            time.sleep(2)
            continue
    return -1,-1
@retry(delay=0, tries=6,backoff=1, max_delay=120)
def get_assocaite_pr_a_commit_retry(query):
            token_list_my =["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",
                            "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",
                            "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"]
            r = requests.get(query,
                             headers={'Authorization': f"token {token_list_my[random.randint(0,len(token_list_my)-1)]}"}, timeout=10)
            res = r.json()

            print(res)
            if res!=[]:

                num = res[0]

            return res
@retry(delay=0, tries=6,backoff=1, max_delay=120)
def get_assocaite_pr_a_commit_retry_copy(query):
            token_list_my =["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",

                            "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"]

            r = requests.get(query,
                             headers={'Authorization': f"token {token_list_my[random.randint(0,len(token_list_my)-1)]}"}, timeout=10)
            res = r.json()

            print(res)
            if res!=[]:

                num = res[0]

            return res

def get_assocaite_pr_a_commit(query):
    count = 0
    while count < 5:
        try:
            # print("get num querry: ",query)
            global num_count
            num_count += 1
            count += 1
            # res = requests.get(query, headers={'Authorization': github_util.get_token()}).json()

            r = requests.get(query,
                             headers={'Authorization': "token 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"})
            res = r.json()

            try:
                if res!=[]:
                    num = res[0]

                return res
            except Exception as e:
                if r.status_code == 200:
                    limit_data = r.json()
                    core_limit = limit_data["resources"]["core"]["limit"]
                    core_remaining = limit_data["resources"]["core"]["remaining"]

                    print(f"Rate limit: {core_remaining}/{core_limit}")
                traceback.print_exc()
                print("res: ",res,"\n",r.headers)
                time.sleep(5)
                continue

        except Exception as e:
            print("error: ", res)
            traceback.print_exc()
            time.sleep(5)
            continue

    return None
def get_repo_info(query):
    count = 0
    while count < 5:
        try:
            # print("get num querry: ",query)
            global num_count
            num_count += 1
            count += 1
            # res = requests.get(query, headers={'Authorization': github_util.get_token()}).json()

            r = requests.get(query,
                             headers={'Authorization': get_token()})
            res = r.json()

            try:

                num = res['total_count']

                return res
            except Exception as e:
                # traceback.print_exc()
                # print("res: ",r.headers)
                time.sleep(2)
                continue

        except Exception as e:
            print("error: ", res)
            traceback.print_exc()
            time.sleep(2)
            continue

    return None if not r else r
def get_request(query):
    count = 0
    while count < 5:
        try:
            # print("get num querry: ",query)
            global num_count
            num_count += 1
            count += 1
            r = requests.get(query, params=issues_payload,
                             headers={'Authorization': 'token %s' % get_token(num_count)})
            res = r.json()

            try:

                num = res['full_name']

                return res
            except Exception as e:
                #traceback.print_exc()
                #print("res: ",r.headers)
                time.sleep(2)
                continue

        except Exception as e:
            print("error: ", res)
            traceback.print_exc()
            time.sleep(2)
            continue

    return None

def get_num(query,issues_payload = {"per_page": 100,"page": 1,"state": "all" },error_query_list=[]):
    count=0
    while count<5:
        try:
            #print("get num querry: ",query)
            global num_count
            num_count+=1
            count+=1
            r= requests.get(query, params=issues_payload,
                               headers={'Authorization': 'token %s' % get_token(num_count)})
            res=r.json()

            try:
                num=res['full_name']

                return num,res
            except Exception as e:
                traceback.print_exc()
                print("res: ", res,r.headers)
                time.sleep(2)
                continue

        except Exception as e:
            print("error: ",repr(e))
            traceback.print_exc()
            time.sleep(2)
            continue
    print("num: ",-1)
    error_query_list.append(query)
    return -1,[]
def connect_github(token_num=None):

    token = get_token()
    g = github.Github(token)
    return g
def get_repo(g,repo_name):
    repo = g.get_repo(repo_name)
    return repo

def get_iss_pygithub(repo,issue_number):
    #repo = g.get_repo(repo_name)
    iss = repo.get_issue(number=issue_number)
    return iss
def get_iss_req(url):

    while True:
        try:
            res = requests.get(url,headers={'Authorization': get_token()})# auth=HTTPBasicAuth('zju_blf@foxmail.com', '!QAZxsw2'))#
            #print("headers: ", res.headers)
            '''
            if int(res.headers['X-RateLimit-Remaining'])<5:
                time.sleep(10)
                continue
            '''
            r = res.json()
            return r
        except Exception as e:
            print("exception",e)

            traceback.print_exc()
            continue
        #print(r['message'])
        '''
        print("headers: ",res.headers)
        r = res.json()
        if 'message' in r.keys():
            if "API rate limit exceeded for" in r['message']:
                time.sleep(10)
                continue
        '''
