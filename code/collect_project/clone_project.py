import os,sys
# Get the current directory
current_dir = os.path.dirname(__file__)

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Append the parent directory to sys.path
sys.path.append(parent_dir)
import util
import code.github_util as github_util
'''
4. Clone project based on filtered projects
'''
def clone_repo(pro_root, repo_info_items):
    repo_name_list = []
    count = 0
    exist_count = 0
    repo_list = []
    for index, repo_info in enumerate(repo_info_items[:100]):
        # if index!=116:
        #     continue
        file_html = repo_info['owner']
        repo_name = repo_info["name"]
        url_list = ["https://github.com", file_html, repo_name]
        # url = file_html.split("/")[:5]
        url = "/".join(url_list)
        # print("repo_name: ", repo_name, url)
        # url = "https://github.com/kholia/OSX-KVM"
        # count+=1
        # break
        # count = 0
        # exist_count = 0
        # repo_list = []
        # for repo_info in pro_info_python_list[:10000]:
        #     url = repo_info['html_url']
        clone_flag, repo_name = github_util.clone_pro(pro_root, url)
        if repo_name in repo_list:
            print(f"{repo_name} is existed", url)
        repo_list.append(repo_name)

        if clone_flag == 1:
            count += 1
        elif clone_flag == 2:
            exist_count += 1
        # end = time.time()
        print("clone count: ", count)
        print("exist count: ", exist_count, len(repo_list), len(set(repo_list)))  # 850,1000

if __name__ == '__main__':
    language ="javaScript"#'java'#'python' # 'javaScript'#
    data_root = "c:\\users\\shuli\\workspace\\KodStand\\data"
    for l in ["java","python"]:

        file_name = os.path.join(data_root, l + "_repo_metadata_sample")
        repo_data=util.load_json(file_name,"")
        pro_root = os.path.join(data_root, l + "repos/")
        clone_repo(pro_root, repo_data[:100])
    pass
# while i < len(self.__op):
#     if self.__op[i] == command[0:6] and self.__op[i] != '000000':
#         assembly = assembly + self.__com[i] + ' '
#         if self.__inType[i] == 'R':
#             if self.__rd[i] == 'l':
#                 regR = command[16:21]
#                 assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__rs[i] == 'l':
#                 if self.__com[i] == 'SLLV' or self.__com[i] == 'SRAV' or self.__com[i] == 'SRLV':
#                     regR = command[11:16]
#                 else:
#                     regR = command[6:11]
#                 assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__rt[i] == 'l':
#                 if self.__com[i] == 'SLLV' or self.__com[i] == 'SRAV' or self.__com[i] == 'SRLV':
#                     regR = command[6:11]
#                 else:
#                     regR = command[11:16]
#                 assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__shamt[i] == 'l':
#                 regR = '000' + command[21:26]
#                 assembly = assembly + '0x' + self.__binToHex(regR)
#         elif self.__inType[i] == 'I':
#             if self.__rt[i] == 'l':
#                 if self.__com[i] == 'BNE' or self.__com[i] == 'BEQ':
#                     regR = command[6:11]
#                 else:
#                     regR = command[11:16]
#                 assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__rs[i] == 'l':
#                 if self.__com[i] == 'BNE' or self.__com[i] == 'BEQ':
#                     regR = command[11:16]
#                     assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#                 elif self.__form[i].find('(') != -1:
#                     regR = command[16:]
#                     assembly = assembly + '0x' + self.__binToHex(regR)
#                 else:
#                     regR = command[6:11]
#                     assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__imm[i] == 'l':
#                 if self.__form[i].find('(') != -1:
#                     regR = command[6:11]
#                     assembly = assembly + '(' + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ')'
#                 else:
#                     regR = command[16:]
#                     assembly = assembly + '0x' + self.__binToHex(regR)
#         elif self.__inType[i] == 'J':
#             regR = '00' + command[6:]
#             assembly = assembly + '0x' + self.__binToHex(regR)
#         break
#     elif self.__func[i] == command[26:32] and self.__op[i] == '000000' and (command[0:6] == '000000'):
#         assembly = assembly + self.__com[i] + ' '
#         if self.__inType[i] == 'R':
#             if self.__rd[i] == 'l':
#                 regR = command[16:21]
#                 assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__rs[i] == 'l':
#                 if self.__com[i] == 'SLLV' or self.__com[i] == 'SRAV' or self.__com[i] == 'SRLV':
#                     regR = command[11:16]
#                 else:
#                     regR = command[6:11]
#                 assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__rt[i] == 'l':
#                 if self.__com[i] == 'SLLV' or self.__com[i] == 'SRAV' or self.__com[i] == 'SRLV':
#                     regR = command[6:11]
#                 else:
#                     regR = command[11:16]
#                 assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__shamt[i] == 'l':
#                 regR = '000' + command[21:26]
#                 assembly = assembly + '0x' + self.__binToHex(regR)
#         elif self.__inType[i] == 'I':
#             if self.__rt[i] == 'l':
#                 if self.__com[i] == 'BNE' or self.__com[i] == 'BEQ':
#                     regR = command[6:11]
#                 else:
#                     regR = command[11:16]
#                 assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__rs[i] == 'l':
#                 if self.__com[i] == 'BNE' or self.__com[i] == 'BEQ':
#                     regR = command[11:16]
#                     assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#                 elif self.__form[i].find('(') != -1:
#                     regR = command[16:]
#                     assembly = assembly + '0x' + self.__binToHex(regR)
#                 else:
#                     regR = command[6:11]
#                     assembly = assembly + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ' '
#             if self.__imm[i] == 'l':
#                 if self.__form[i].find('(') != -1:
#                     regR = command[6:11]
#                     assembly = assembly + '(' + self.__findRegFromBin(regR, self.__regName, self.__regCode, jarvis) + ')'
#                 else:
#                     regR = command[16:]
#                     assembly = assembly + '0x' + self.__binToHex(regR)
#         elif self.__inType[i] == 'J':
#             regR = '00' + command[6:]
#             assembly = assembly + '0x' + self.__binToHex(regR)
#         break
#     i = i + 1
# else:
#     jarvis.say('No such command exists.')
#     return