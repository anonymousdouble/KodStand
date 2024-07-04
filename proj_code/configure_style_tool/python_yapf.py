'''
Get results from yapf for any project ".py"

'''
from code import util
import seaborn as sns
import matplotlib.pyplot as plt
import random
def get_num_pro(data):
    print("count of projects: ",len(data))
def draw_box_plot(data,language = "Python",size=1e6):
    new_data = [e_pro[language] for ind, e_pro in enumerate(data) if
                language in e_pro and e_pro[language] > size]

    sns.boxplot(data=new_data)
    plt.title('Box Plot')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

def sort_by_key(data,language = "Python", size = 1e6):

    for ind,e_pro in enumerate(data):
        for e in e_pro["languages"]:
            if e['name'] == language:
                data[ind][language] = e['size']
                break
    # sorted(data, key=lamda x: x[1])
    new_data = [e_pro for ind,e_pro in enumerate(data) if language in e_pro and e_pro[language]>size]
    print("count of projects: ", len(data),len(new_data))
    sorted_list = sorted(new_data, key=lambda x: x[language])
    # sorted_list = sorted(new_data, key=lambda x: x[language], reverse=True)
    print(sorted_list[:10])

    # sorted_list = sorted(new_data)
    # new_data = [e_pro[language] for ind,e_pro in enumerate(data) if language in e_pro and e_pro[language]>0]
    # sorted_list = sorted(new_data, reverse=True)
    draw_box_plot(new_data, language="Python", size=size)
    return sorted_list
    # print(sorted_list[:10])

    # print("count of projects: ",len(data))


if __name__ == '__main__':
    language = 'javascript'#'java'#'python'
    size = 1e6
    repo_data=util.load_json(util.data_root, language+ "_repo_metadata")
    get_num_pro(repo_data)
    language='javaScript' if language =='javascript' else language
    sorted_list = sort_by_key(repo_data, language=language[:1].upper() + language[1:], size = size)
    # Set a seed for reproducibility
    random.seed(2024)

    # Shuffle the list
    random.shuffle(sorted_list)
    sample_size=380 #378 # 20657 python 21138 [378] java 33119 [378] javascript [380]
    util.save_json(util.data_root, language+ "_repo_metadata_sample", sorted_list[:sample_size])
    # path =
    # util.save_json(util.data_root, "java_repo_metadata", java_list)
    # util.save_json(util.data_root, "python_repo_metadata", python_list)
    # util.save_json(util.data_root, "javascript_repo_metadata", javascript_list)
    # pass