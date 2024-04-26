from collections import defaultdict
import subprocess
import os
import shutil
import time
from multiprocessing import Pool
import json
ignore_dirs = ["node_modules", "plugins"]
config_path = "C:\\Users\\shuli\\workspace\\KodStand\\data\\config\\eslint\\eslint.config.mjs"


def check_project(proj_root, save_root):
    shutil.copyfile(config_path, os.path.join(proj_root, "eslint.config.mjs"))
    shutil.rmtree(save_root, ignore_errors=True)
    os.makedirs(save_root, exist_ok=True)
    t = time.time()
    pool = Pool(24)
    tasks = []
    for root, dirs, files in os.walk(proj_root):
        flag = False
        for item in ignore_dirs:
            if item in root:
                flag = True
                break
        if flag:
            continue
        current_root = root.replace(proj_root, save_root)
        os.makedirs(current_root, exist_ok=True)
        for file in files:
            if file.endswith(".js") or file.endswith(".mjs"):
                analyze_fpath = os.path.join(current_root, file).replace(".js", ".json").replace(".mjs", ".json")
                file_path = os.path.join(root, file)
                tasks.append(pool.apply_async(analyze, args=(root, analyze_fpath, file_path)))
    pool.close()
    pool.join()
    print(f"finished {proj_root} in {time.time()-t} seconds")

def analyze(root, analyze_fpath, file_path):
    print(f"checking {file_path}")
    cmd = f"eslint {file_path} -f json -o {analyze_fpath}"
    p = subprocess.Popen(cmd, shell=True, cwd=root)
    p.wait()


def rename_remove_space(proj_root):
    for root, dirs, files in os.walk(proj_root):
        # rename dir
        for dir in dirs:
            if " " in dir:
                dir_path = os.path.join(root, dir)
                new_dir_path = os.path.join(root, dir.replace(" ", "_"))
                os.rename(dir_path, new_dir_path)

    for root, dirs, files in os.walk(proj_root):
        for file in files:
            if file.endswith(".js") or file.endswith(".mjs"):
                file_path = os.path.join(root, file)
                if " " in file_path:
                    new_file_path = os.path.join(root, file.replace(" ", "_"))
                    if os.path.exists(new_file_path):
                        new_file_path = new_file_path.replace(".js", "_1.js")
                    os.rename(file_path, new_file_path)

def check_repositories():
    repository = "C:\\Users\\shuli\\workspace\\codestandard_data\\javaScriptrepos"
    # get current project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    save_root = os.path.join(project_root, "data","result", "eslint_google_result")
    if not os.path.exists(save_root):
        os.makedirs(save_root)
    for proj in os.listdir(repository):
        proj_root = os.path.join(repository, proj)
        save_proj_root = os.path.join(save_root, proj)
        print(f"start check proj: {proj}")
        check_project(proj_root, save_proj_root)
        # break

def rm_cofig(repository):
    for proj in os.listdir(repository):
        proj_root = os.path.join(repository, proj)
        for root, dirs, files in os.walk(proj_root):
            for file in files:
                if file == "eslint.config.json":
                    os.remove(os.path.join(root, file))

def result_stat(errors,result_path):
    local_errors = {}
    with open(result_path, "r",encoding='utf-8') as f:
        data = json.load(f)
        messages = data[0]["messages"]
        for msg in messages:
            if msg["ruleId"] is None:
                continue
            if msg["ruleId"] not in local_errors:
                local_errors[msg["ruleId"]] = 0
            local_errors[msg["ruleId"]] += 1

    local_errors = sorted(local_errors.items(), key=lambda x: x[1], reverse=True)
    csv_path = result_path.replace(".json", ".csv")
    with open(csv_path, "w",encoding='utf-8') as f:
        f.write("rule,instance,percentage\n")
        for k,v in local_errors:
            f.write(f"{k},{v},{v/len(messages)*100:.2f}\n")
    for k,v in local_errors:
        if k not in errors:
            errors[k] = 0
        errors[k] += v
    return errors

def proj_result_stat(proj_root):
    print(f"start stat proj: {proj_root}")
    proj_errors = {}
    for root, dirs, files in os.walk(proj_root):
        for file in files:
            if file.endswith(".json"):
                proj_errors = result_stat(proj_errors, os.path.join(root, file))
    proj_errors = sorted(proj_errors.items(), key=lambda x: x[1], reverse=True)
    cnt = sum([v for _,v in proj_errors])
    with open(os.path.join(proj_root, "result.csv"), "w", encoding='utf-8') as f:
        f.write("rule,instance,percentage\n")
        for k,v in proj_errors:
            f.write(f"{k},{v},{v/cnt*100:.2f}\n")
    print(f"finished stat proj: {proj_root}")
    return proj_errors

def stat_all_repositories(data_root):
    pool = Pool(24)
    tasks = []
    for proj in os.listdir(data_root):
        proj_root = os.path.join(data_root, proj)
        tasks.append(pool.apply_async(proj_result_stat, args=(proj_root,)))
    pool.close()
    pool.join()
    print("finished all repos")

def get_corresponding_code(json_path,rule):

    with open(json_path, "r",encoding='utf-8') as f:
        data = json.load(f)
        code = data[0]["source"]
        messages = data[0]["messages"]
        errors = []
        for msg in messages:
            if msg["ruleId"] == rule:
                errors.append(msg)
        for error in errors:
            start_line = error["line"] - 1
            start_column = error["column"] - 1
            end_line = error["endLine"] - 1
            end_column = error["endColumn"]
            code = code.split("\r\n")# windows
            detail_code = ""
            if start_line == end_line:
                detail_code = code[start_line][start_column:end_column]
            else:
                detail_code = code[start_line][start_column:]
                for i in range(start_line+1, end_line):
                    detail_code += f"\n{code[i]}"
                detail_code += f"\n{code[end_line][:end_column]}"
            print(f"error: {error['message']}")
            print("code:")
            print(detail_code)
if __name__ == '__main__':
    # check_repositories()
    # rm_cofig("data\\result\\eslint_google_result")

    # result_stat({},"data\\result\\eslint_google_result\\311-data\\components\\main\\desktop\\councilselector\\index.json")
    # corresponding_code("data\\result\\eslint_google_result\\311-data\\public\\duckdb-browser-mvp.worker.json", "no-await-in-loop")
    # proj_result_stat("data\\result\\eslint_google_result\\311-data")

    stat_all_repositories("C:\\Users\\shuli\\workspace\\kodstand\\data\\result\\eslint_google_result")