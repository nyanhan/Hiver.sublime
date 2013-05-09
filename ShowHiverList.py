import sublime
import sublime_plugin
import subprocess

s = sublime.load_settings('Hiver.tools (' + sublime.platform().upper() +').sublime-settings')

CommandHash = {}

RESULT_VIEW_NAME = "hiver_tools_output"

CommandHash["Edit " + s.get("hosts_path")] = "hiver_edit_hosts"

if s.get("nginx_conf_path"):
    CommandHash["Edit " + s.get("nginx_conf_path")] = "hiver_edit_nginx"
    pass

if s.get("nginx_path"):
    CommandHash["Nginx reload"] = "hiver_reload_nginx"
    CommandHash["Nginx start"] = "hiver_start_nginx"
    CommandHash["Nginx stop"] = "hiver_stop_nginx"
    pass

CommandList = sorted(CommandHash.keys())


class ShowHiverListCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_quick_panel(CommandList, self.on_done, sublime.MONOSPACE_FONT)
        pass

    def on_done(self, index):
        if index >= 0:
            cmd = CommandList[index]
            self.window.run_command(CommandHash[cmd])
            
        pass

class HiverEditHostsCommand(sublime_plugin.WindowCommand):
    def run(self):
        hosts = s.get("hosts_path");
        self.window.open_file(hosts);
        pass

class HiverEditNginxCommand(sublime_plugin.WindowCommand):
    def run(self):
        conf = s.get("nginx_conf_path");
        self.window.open_file(conf);
        pass

LOG_PANEL = None

class HiverReloadNginx(sublime_plugin.WindowCommand):
    def run(self):

        global LOG_PANEL

        LOG_PANEL = self.window.get_output_panel(RESULT_VIEW_NAME)

        conf = s.get("nginx_path")
        
        e = subprocess.Popen(conf + " -s reload", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

        error = e.stderr.readlines()

        if error:
            sublime.error_message((b"".join(error).decode("utf-8")))
        else:
            sublime.message_dialog("Nginx reload success.")
            # panel_edit = LOG_PANEL.begin_edit()
            # LOG_PANEL.insert(panel_edit, LOG_PANEL.size(), "Reload Success...")
            # LOG_PANEL.end_edit(panel_edit)
            # LOG_PANEL.show(LOG_PANEL.size());
            # # self.window.run_command("close_panel", { "panel": "output." + RESULT_VIEW_NAME })
            # self.window.run_command("show_panel", { "panel": "output." + RESULT_VIEW_NAME })

class HiverStartNginx(sublime_plugin.WindowCommand):
    def run(self):
        conf = s.get("nginx_path");

        e = subprocess.Popen(conf, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

        error = e.stderr.readlines()

        if error:
            sublime.error_message((b"".join(error).decode("utf-8")))
        else:
            sublime.message_dialog("Nginx start success.")

class HiverStopNginx(sublime_plugin.WindowCommand):
    def run(self):
        conf = s.get("nginx_path");

        e = subprocess.Popen(conf + " -s stop", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        
        error = e.stderr.readlines()

        if error:
            sublime.error_message((b"".join(error).decode("utf-8")))
        else:
            sublime.message_dialog("Nginx stop success.")
            