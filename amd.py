import sublime, sublime_plugin

class MakeAmdModuleCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.edit = edit
    self.amd_name = None
    self.view.window().show_input_panel("AMD Return Name", "", self.input_done, None, None)

  def input_done(self, text):
    if len(text) > 0:
      self.amd_name = text
      self.make_amd()

  def get_tab_str(self):
    settings = self.view.settings()
    tab_size = int(settings.get('tab_size', 8))
    use_spaces = settings.get('translate_tabs_to_spaces')
    if use_spaces:
      return tab_size * ' '
    else:
      return '\t'

  def make_amd(self):
    region = sublime.Region(0, self.view.size())
    final_str = ''
    tab_str = self.get_tab_str()
    line_endings = '\n'
    for l in self.view.split_by_newlines(region):
      final_str += tab_str + self.view.substr(l) + line_endings
    final_str = 'define([], function() { ' + line_endings + final_str 
    final_str += '  return'
    if self.amd_name is not None and len(self.amd_name) > 0:
      final_str += ' ' + self.amd_name + ';'
    else:
      final_str += ';'
    final_str += line_endings + '});'
    self.view.replace(self.edit, region, final_str)