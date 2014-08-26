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

            # px -> rem
            if gd.get('unit', None) == 'px':
                ret = '%3.4f' % (float(gd.get('qty')) / float(self.rem_height))
                while ret[-1] == '0':
                    ret = ret[:-1]
                if ret.endswith('.'):
                    ret = ret[:-1]
                return ret + 'rem'

            # rem -> px
            if gd.get('unit', None) == 'rem':
                ret_val = float(gd.get('qty')) * float(self.rem_height)
                ret = '%3.1f' % ret_val
                if ret.endswith('.0'):
                    ret = ('%3.0f' % ret_val) + 'px'
                else:
                    ret = ret + 'px'
                return ret.strip()

        return re.sub(r'((?P<qty>[0-9\.]+)(?P<unit>px|rem))', repl, str_)
