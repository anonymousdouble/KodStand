from yapf.yapflib import style
from yapf.yapflib import reformatter
from yapf.yapflib import yapf_api
from yapf.yapflib import py3compat

import os,sys
current_dir = os.path.dirname(__file__)
# print(current_dir)
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
# print(parent_dir)
# Append the parent directory to sys.path
sys.path.append(parent_dir)
from code import util
style.SetGlobalStyle(style.CreateGoogleStyle())
data_dir=util.data_root + "test_data/weixin/"
for root, dirs, files in os.walk(data_dir):
  # path = root.split(os.sep)
  # print((len(path) - 1) * '---', os.path.basename(root))
  for file in files:
    if file.endswith(".py"):
      # print(len(path) * '---', file,root,dirs)
      path = root+"/"+file
      source = util.load_file_path(path)

      reformatted_source, _ = yapf_api.FormatCode(
                py3compat.unicode(source),
                filename='aaa',
                style_config="google",
                lines=None,
      print_diff=True,
        verify=False)
      print(">>>>>source: ", source)
      print(">>>>>reformatted_source: ", reformatted_source)
      break
    # break
# source ='''
# class Foo:
#
#             def joe():
#                 pass
# '''

# reformatted_source, _ = yapf_api.FormatCode(
#           py3compat.unicode(source),
#           filename='aaa',
#           style_config="google",
#           lines=None,
# print_diff=False,
#   verify=False)

# yapf_api.FormatCode()
# reformatter.Reformat(llines)
