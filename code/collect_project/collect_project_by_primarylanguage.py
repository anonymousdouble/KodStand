from code import util
'''
1. GitHub Public Repository Metadata
https://www.kaggle.com/datasets/pelmers/github-repository-metadata-with-5-stars?resource=download

2. filter projects by primaryLanguage
'''
if __name__ == '__main__':
    all_rules=[]
    data_path= util.data_root + "repo_metadata.json"
    repo_data=util.load_json(util.data_root, "repo_metadata")
    print(repo_data[0])
    java_list,python_list,javascript_list=[],[],[]

    for each_data in repo_data:
        # each_data=repo_data[0]
        if each_data["primaryLanguage"] == 'Python':
            python_list.append(each_data)
            pass

        elif each_data["primaryLanguage"] == 'Java':
            java_list.append(each_data)
            pass

        elif each_data["primaryLanguage"] == 'JavaScript':
            javascript_list.append(each_data)
            pass

    util.save_json(util.data_root, "java_repo_metadata",java_list)
    util.save_json(util.data_root, "python_repo_metadata", python_list)
    util.save_json(util.data_root, "javascript_repo_metadata", javascript_list)
       # for key in each_data:
        #     print(key,": ",each_data[key])
    # file_path =ruff_data_dir + "Rules-Ruff.html"
