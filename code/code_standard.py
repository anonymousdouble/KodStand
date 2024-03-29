class CodeStandardOption(object):
  def __init__(self,url =None, name = None, description = None):
    self.name = name
    self.url = url
    self.description = description
  def parse_option(self):
    return "\n".join([self.url, self.name, self.description if self.description else "None" ])
class CodeStandard(object):
  """Desc.
  Attributes:

  """

  def __init__(self, url = None, iden = None, name = None, msg = None, state = "Stable", fix = None, content_file_path = None, description = None, suggestion = None, codeExamples = [], options = None,  type = None, other = None):
    """Initializer.
    Arguments:
      state : stable, unstable, deprecated, removed
      fix: None --- do not have   [XXX, XXX] fix strategy from formal doc
      suggestions: own recommendations
      type :  "Error/Warning"
    """
    self.url = url
    self.iden = iden
    self.name = name
    self.description = description
    self.content_file_path = content_file_path
    self.msg = msg
    self.options = options
    self.fix = fix
    self.state = state
    self.suggestion = suggestion
    self.type = type
    self.codeExamples =codeExamples
    self.other = other

class RuffCodeStandard(CodeStandard):
  def parse_msg_to_text(self):
    self.msg
  def preprocess_description(self):
    pre_des="\n".join([e for e in self.description.split("\n") if "What it does" not in e])
    # print(">>>pre_des: ",pre_des, "<<<<<")
    return pre_des
  def preprocess_suggestion(self):
    pre_sugge="\n".join([e for e in self.suggestion.split("\n") if "Why is this bad" not in e])
    # print(">>>pre_suggestion: ",pre_sugge, "<<<<<")
    return pre_sugge
  def parse_code_examples(self):
    examples = []
    for example in self.codeExamples:
     if len(example)>2:
      examples.append("".join(["----neg----:\n", example[0] if example[0] else "None", "----pos----:\n", example[1] if example[1] else "None","----other----:\n",example[2] if len(example)>2 and example[2] else "None"]))
     elif len(example)==2:
       print(">>>example: ",self.url,example)
       examples.append("".join(["----neg----:\n", example[0] if example[0] else "None", "----pos----:\n",
                                example[1] if example[1] else "None"]))
     else:
       print(">>>example: ", self.url, example)
       examples.append("".join([example[0]]))

    return "\n".join(examples)
  def parse_options(self):
    options = []
    for opt in self.options:
      options.append(opt.parse_option())
      # examples = "".join(["----neg----:\n", example[0] if example[0] else "None", "----pos----:\n", example[1] if example[1] else "None","----other----:\n",example[2] if len(example)>2 and example[2] else "None"])
    return "\n".join(options)


  # def __init__(self, dict_content):
  #   pass


