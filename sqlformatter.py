import sublime
import sublime_plugin

from .src import formatter

class FormatQueryCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		
		selection = view.sel()
		if len(selection) > 1 or not selection[0].empty():
			regions = [region for region in selection if not(region.empty())]
		else:
			regions = [sublime.Region(0, self.view.size())]

		for region in regions:
			formatted_text = formatter.format_query(view.substr(region))
			self.view.replace(edit, region, formatted_text)
