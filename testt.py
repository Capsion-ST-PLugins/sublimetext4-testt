import sublime,sublime_plugin
import os,re

if int(sublime.version()) < 3176:
    raise ImportWarning("本插件不支持当前版本，请使用大于等于3176的sublime Text")

def plugin_loaded():
    print('加载testt插件')


class TesttCommand(sublime_plugin.TextCommand):
    def run(self, edit, str:str=""):
        pass

# 快速打印一个参数
class TesttPrintParam(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view

        # 获取当前行的region
        currt_region:sublime.Region =  self.view.sel()[0]
        currt_line_region = view.full_line(currt_region)

        # 获取下一行
        newt_line_start:int = currt_line_region.b

        # 获取关键字
        select_str = self.view.substr(currt_region)
        if not select_str or len(select_str) <= 0:
            return print('没有任何选择')

        # 获取前置缩进
        currt_line_str = self.view.substr(currt_line_region)

        # 提取前缩进
        res = re.compile(r'^(\s*)?(.*)').findall(currt_line_str)

        # 根据不同格式插入不同
        name,ext = os.path.splitext(view.file_name())
        if ext == '.py':
            insert_tmpl = '{indent}print("{param}: ", {param})\n'
        elif ext in ['.js','.ts','.vue']:
            insert_tmpl = '{indent}console.log("{param}: ", {param})\n'
        else:
            return False

        if res and len(res)>0 :
            view.insert(edit, newt_line_start, insert_tmpl.format(indent=res[0][0], param=select_str))


# 打开当前文件的文件夹
class TesttOpenCurrtFolder(sublime_plugin.TextCommand):
    def run(self, edit):
        print('打开当前文件夹')
        #调用当前激活的窗口来执行 run_command命令(无法使用 self.view 调用 run_command)
        fdir, fname = os.path.split(self.view.file_name()) 
        sublime.active_window().run_command("open_dir", {"dir": fdir})

# 设置语法
class TesttSetSyntaxCommand(sublime_plugin.TextCommand):
    def run(self,edit,syntax):
        syntaxDict = {
          "html":"Packages/HTML/HTML.sublime-syntax",
          "vue":"Packages/Vue Syntax Highlight/Vue Component.sublime-syntax",
          "js":"Packages/JavaScriptNext - ES6 Syntax/JavaScriptNext.tmLanguage"
        }
        if syntax : self.view.set_syntax_file(syntaxDict[syntax])

# 清除所有注释
class TesttRemoveCommentsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        comments = self.view.find_by_selector('comment')
        # 遍历所有注释块
        for region in reversed(comments):
            self.view.erase(edit, region)
