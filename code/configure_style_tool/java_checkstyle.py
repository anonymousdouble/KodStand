import subprocess
import os
import shutil
import time
from multiprocessing import Pool
from xml.etree import ElementTree as ET
ignore_dirs = ["plugins"]
def check_file(file_path, output_path):
    cmd = f"java -Duser.language=en -jar checkstyle.jar {file_path} -o {output_path} -f xml -c google_checks.xml"
    p = subprocess.Popen(
        cmd,
        shell=True,
        cwd = "data\\config\\checkstyle")
    p.wait()

def check_repositories():
    repository = "D:\\Work\\Dataset\\codestandard_data\\javarepos"
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    save_root = os.path.join(project_root, "data","result", "checkstyle_google_result")
    if not os.path.exists(save_root):
        os.makedirs(save_root)
    for proj in os.listdir(repository):
        proj_root = os.path.join(repository, proj)
        save_proj_root = os.path.join(save_root, proj)
        print(f"start check proj: {proj}")
        check_project(proj_root, save_proj_root)

def check_project(proj_root, save_root):
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
            if file.endswith(".java"):
                analyze_fpath = os.path.join(current_root, file).replace(".java", ".xml")
                file_path = os.path.join(root, file)
                tasks.append(pool.apply_async(check_file, args=(file_path, analyze_fpath)))
    pool.close()
    pool.join()
    print(f"finished {proj_root} in {time.time()-t} seconds")

if __name__== '__main__':
    check_repositories()