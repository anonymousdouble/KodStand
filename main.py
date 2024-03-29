# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    import re
    print(re.MULTILINE)
    text = "foo\nbar"
    matches = re.findall("^bar$", text)
    print(matches)

    text = 'foo1\nfoo2\n'
    matches = re.findall("foo.$", text,re.MULTILINE)
    print(matches)
    matches = re.findall("foo.$", text)
    print(matches)

    import re

    text = "hello, this is a world example."
    pattern = "^hello.*world$"

    match = re.search(pattern, text)

    if match:
        print("匹配成功！")
    else:
        print("匹配失败。")

    text = "hello, this is a world"
    pattern = "^hello.*world$"

    match = re.search(pattern, text)

    if match:
        print("匹配成功！")
    else:
        print("匹配失败。")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
