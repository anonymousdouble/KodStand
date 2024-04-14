import subprocess
import os
import shutil
ignore_dirs = ["node_modules","plugins"]
config_path = "C:\\Users\\shuli\\workspace\\KodStand\\data\\eslint\\eslint.config.mjs"
def check_project(proj_root, save_path):
    shutil.copyfile(config_path, os.path.join(proj_root, "eslint.config.mjs"))
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


if __name__ == '__main__':
    repository = "C:\\Users\\shuli\\workspace\\codestandard_data\\javaScriptrepos"
    save_root = os.path.join(os.getcwd(), "data", "eslint_result")
    if not os.path.exists(save_root):
        os.makedirs(save_root)
    for proj in os.listdir(repository):
        check_project(os.path.join(repository, proj),
                      os.path.join(save_root, f"{proj}.txt"))
