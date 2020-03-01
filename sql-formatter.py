import sublime
import sublime_plugin

from .src import formatter

def call_formatter(self, edit, minify):
	self.view.erase_regions('sql_errors')

	regions = []
	error_regions = []

	selection = self.view.sel()
	if len(selection) > 1 or not selection[0].empty():
		regions = [region for region in selection if not(region.empty())]
	if not regions:
		regions = [sublime.Region(0, self.view.size())]

	for region in reversed(regions):
		try:
			formatted_text = formatter.format_query(self.view.substr(region), minify)
			self.view.replace(edit, region, formatted_text)
		except (ValueError, SyntaxError) as err:
			left = min(region.a, region.b)
			right = max(region.a, region.b)
			err_pos = int(str(err))
			if err_pos > 0:
				error_regions.append(sublime.Region(left + err_pos, right))
			else:
				error_regions.append(sublime.Region(right - 1, right))

	
	if error_regions:
		self.view.add_regions('sql_errors', error_regions, scope='invalid', flags=sublime.DRAW_OUTLINED)
		self.view.show(error_regions[0])

	if "Plain text" in self.view.settings().get('syntax'):
		self.view.set_syntax_file("Packages/SQL/SQL.tmLanguage")

class FormatQueryCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		call_formatter(self, edit, False)

class MinifyQueryCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		call_formatter(self, edit, True)
