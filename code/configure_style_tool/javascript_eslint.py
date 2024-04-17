import subprocess
import os
import shutil
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
ignore_dirs = ["node_modules","plugins"]
config_path = "C:\\Users\\shuli\\workspace\\KodStand\\data\\eslint\\eslint.config.mjs"
def check_project(proj_root, save_path):
    shutil.copyfile(config_path, os.path.join(proj_root, "eslint.config.mjs"))
    # create thread pool
    with ThreadPoolExecutor(max_workers=16) as executor:
        with open(save_path, "w") as of:
            for root, dirs, files in os.walk(proj_root):
                flag = False
                for item in ignore_dirs:
                    if item in root:
                        flag = True
                        break
                if flag:
                    continue
                for file in files:
                    if file.endswith(".js"):
                        file_path = os.path.join(root, file)
                        print(f"checking {file_path}")
                        cmd = f"cd {root} && eslint {file_path}"
                        # params = ["cd",
                        #     root,
                        #     "&&",
                        #     "eslint",
                        #     "--config",
                        #     "C:\\Users\\shuli\\workspace\\KodStand\\data\\eslint\\eslint.config.mjs",
                        #     file_path]
                        # print(params)
                        subprocess.run(cmd, shell=True, stdout=of, stderr=of)
                        # subprocess.run(["eslint", "--no-ignore",file_path], shell=True, stdout=of, stderr=of)

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
    
    rename_remove_space(repository)

    for proj in os.listdir(repository):
        proj_root = os.path.join(repository, proj)
        save_path = os.path.join(save_root, f"{proj}.txt")
        print(f"start check proj: {proj}")
        check_project(proj_root, save_path)
