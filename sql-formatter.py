import sublime
import sublime_plugin

from .src import formatter

def call_formatter(self, edit, minify):
	regions = []
	selection = self.view.sel()
	if len(selection) > 1 or not selection[0].empty():
		regions = [region for region in selection if not(region.empty())]
	if not regions:
		regions = [sublime.Region(0, self.view.size())]

	for region in regions:
		formatted_text = formatter.format_query(self.view.substr(region), minify)
		self.view.replace(edit, region, formatted_text)

	if "Plain text" in self.view.settings().get('syntax'):
		self.view.set_syntax_file("Packages/SQL/SQL.tmLanguage")

class FormatQueryCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		call_formatter(self, edit, False)

class MinifyQueryCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		call_formatter(self, edit, True)
