import string
import sublime
import sublime_plugin
import re

class PxToRemCommand(sublime_plugin.TextCommand):

    def __init__(self, *args, **kwargs):
        super(PxToRemCommand, self).__init__(*args, **kwargs)
        self.rem_height = sublime.load_settings('CSSPxToRem.sublime-settings').get('rem_height', 16)

    def run(self, edit):
        for s in self.view.sel():
            if s.empty():
                s = self.view.word(s)

            txt = self.transform(self.view.substr(s))
            self.view.replace(edit, s, txt)

    def transform(self, str):
        def repl(m):
            return '%3.4frem' % (int(m.group(2)) / float(self.rem_height))
        return re.sub(r'((\d+)\s*px)', repl, str)
