import subprocess
import os
import shutil
import shutil
import time
from multiprocessing import Pool
ignore_dirs = ["node_modules", "plugins"]
config_path = "C:\\Users\\shuli\\workspace\\KodStand\\data\\eslint\\eslint.config.mjs"


def check_project(proj_root, save_root):
    shutil.copyfile(config_path, os.path.join(proj_root, "eslint.config.mjs"))
    shutil.rmtree(save_root, ignore_errors=True)
    os.makedirs(save_root, exist_ok=True)
    pool = Pool(24)
    tasks = []
    t = time.time()
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
            if file.endswith(".js"):
                analyze_fpath = os.path.join(current_root, file).replace(".js", ".txt")
                file_path = os.path.join(root, file)
                tasks.append(pool.apply_async(analyze, args=(root, analyze_fpath, file_path)))
    pool.close()
    pool.join()
    print(f"finished {proj_root} in {time.time()-t} seconds")

def analyze(root, analyze_fpath, file_path):
    print(f"checking {file_path}")
    cmd = f"eslint {file_path}"
    with open(analyze_fpath, "w") as of:
        p = subprocess.Popen(cmd, shell=True, stdout=of, stderr=of, cwd=root)
        p.wait()


def rename_remove_space(proj_root):
    for root, dirs, files in os.walk(proj_root):
        # rename dir
        for dir in dirs:
            if " " in dir:
                dir_path = os.path.join(root, dir)
                new_dir_path = os.path.join(root, dir.replace(" ", "_"))
                os.rename(dir_path, new_dir_path)
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)
                if " " in file_path:
                    new_file_path = os.path.join(root, file.replace(" ", "_"))
                    if os.path.exists(new_file_path):
                        new_file_path = new_file_path.replace(".js", "_1.js")
                    os.rename(file_path, new_file_path)


if __name__ == '__main__':
    repository = "C:\\Users\\shuli\\workspace\\codestandard_data\\javaScriptrepos"
    save_root = os.path.join(os.getcwd(), "data", "eslint_airbnb_result")
    if not os.path.exists(save_root):
        os.makedirs(save_root)
    # rename_remove_space(repository)
    for proj in os.listdir(repository):
        proj_root = os.path.join(repository, proj)
        save_proj_root = os.path.join(save_root, proj)
        print(f"start check proj: {proj}")
        check_project(proj_root, save_proj_root)
