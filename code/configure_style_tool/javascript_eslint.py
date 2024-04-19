import subprocess
import os
import shutil
import time
from multiprocessing import Pool
ignore_dirs = ["node_modules", "plugins"]
config_path = "C:\\Users\\shuli\\workspace\\KodStand\\data\\eslint\\eslint.config.mjs"


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
    save_root = os.path.join(project_root, "data", "eslint_airbnb_result")
    if not os.path.exists(save_root):
        os.makedirs(save_root)
    for proj in os.listdir(repository):
        proj_root = os.path.join(repository, proj)
        save_proj_root = os.path.join(save_root, proj)
        print(f"start check proj: {proj}")
        check_project(proj_root, save_proj_root)


def rm_cofig(repository):
    for proj in os.listdir(repository):
        proj_root = os.path.join(repository, proj)
        for root, dirs, files in os.walk(proj_root):
            for file in files:
                if file == "eslint.config.json":
                    os.remove(os.path.join(root, file))

if __name__ == '__main__':
    check_repositories()
    # rm_cofig("C:\\Users\\shuli\\workspace\\kodstand\\data\\eslint_airbnb_result")