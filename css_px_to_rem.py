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
            gd = m.groupdict()
            if gd.get('unit', None) == 'px':
                return '%3.4frem%s' % (int(gd.get('qty')) / float(self.rem_height), gd.get('foll'))
            if gd.get('unit', None) == 'rem':
                return '%dpx%s' % (int(float(gd.get('qty')) * float(self.rem_height)), gd.get('foll'))

        return re.sub(r'((?P<qty>[\d\.]+)\s*(?P<unit>px|rem)(?P<foll>[\s;]))', repl, str)
