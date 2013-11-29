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
                s = self.view.line(s)

            txt = self.transform(self.view.substr(s))
            self.view.replace(edit, s, txt)

    def transform(self, str_):
        def repl(m):
            gd = m.groupdict()
            if gd.get('unit', None) == 'px':
                return '%3.4frem' % (int(float(gd.get('qty'))) / float(self.rem_height))
            if gd.get('unit', None) == 'rem':
                return str(int(float(gd.get('qty')) * float(self.rem_height))) + u'px'

        return re.sub(r'((?P<qty>[0-9\.]+)(?P<unit>px|rem))', repl, str_)
