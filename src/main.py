import sys
import gi
import subprocess
from os import listdir
import os
from pathlib import Path
import shutil
import threading

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GLib, Gio

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.leftoverDataSize = 0
        self.deleteErrors = False

        self.set_default_size(400, 600)
        self.set_size_request(400, 600)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_child(self.scroll)

        self.set_title("Flatsweep")
        Gtk.Settings.get_default().set_property("gtk-icon-theme-name", "Adwaita")

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.aboutButton = Gtk.Button(label="About")
        self.header.pack_start(self.aboutButton)
        self.aboutButton.connect("clicked", self.show_about)
        self.aboutButton.set_icon_name("help-about-symbolic")

        self.boxLoading = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, valign = Gtk.Align.CENTER)
        self.boxCleaning = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.boxCleaned = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        #Loading Window Box:
        self.loadingLabel = Gtk.Label()
        self.loadingLabel.set_markup("<span size=\"25000\" weight=\"bold\">Calculating...</span>")
        self.boxLoading.set_margin_top(30)
        self.boxLoading.append(self.loadingLabel)

        #Cleaning Window Box:
        self.cleaningLabel = Gtk.Label()
        self.cleaningLabel.set_markup("<span size=\"25000\" weight=\"bold\">Cleaning...</span>")
        self.boxCleaning.set_margin_top(30)
        self.boxCleaning.append(self.cleaningLabel)

        #Cleaned Window Box:
        self.cleanedLabel = Gtk.Label()
        self.cleanedLabel1 = Gtk.Label()
        self.cleanedLabel1.set_markup("<span size=\"25000\" weight=\"bold\">MB saved.</span>")
        self.cleanedLabelErrors = Gtk.Label()
        self.boxCleaned.set_margin_top(30)
        self.boxCleaned.set_spacing(30)
        self.boxCleaned.append(self.cleanedLabel)
        self.boxCleaned.append(self.cleanedLabel1)
        self.boxCleaned.append(self.cleanedLabelErrors)

        #Main Window Box:
        self.label = Gtk.Label()
        self.label.set_markup("<span size=\"25000\" weight=\"bold\">Leftover data amount:</span>")
        self.box.set_margin_top(30)
        self.box.set_spacing(30)
        self.box.append(self.label)

        self.boxLabelMB = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.boxLabelMB.set_spacing(-30)
        self.labelMB = Gtk.Label()
        self.labelMB1 = Gtk.Label()
        self.labelMB1.set_hexpand(True)
        self.labelMB1.set_markup("<span size=\"40000\" weight=\"bold\">MB</span>")
        self.labelMB.set_hexpand(True)
        self.labelMB1.set_hexpand(True)
        self.boxLabelMB.append(self.labelMB)
        self.boxLabelMB.append(self.labelMB1)
        self.box.append(self.boxLabelMB)

        self.box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign = Gtk.Align.CENTER, valign = Gtk.Align.CENTER)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, valign = Gtk.Align.CENTER)

        self.cleanbuttonBox = Gtk.Box(spacing=100)
        self.cleanbuttonLabel = Gtk.Label()
        self.cleanbuttonLabel.set_markup("<span size=\"25000\" weight=\"bold\">Clean</span>")
        self.cleanbuttonBox.append(self.cleanbuttonLabel)
        self.cleanbutton = Gtk.Button(child=self.cleanbuttonBox)
        self.cleanbutton.get_style_context().add_class("pill")
        self.cleanbutton.get_style_context().add_class("suggested-action")
        self.cleanbutton.connect("clicked", self.init_clean)

        self.box3.append(self.cleanbutton)
        self.box2.append(self.box3)
        self.box.append(self.box2)

        self.toBeCleanedBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign = Gtk.Align.CENTER, valign = Gtk.Align.CENTER)
        self.toBeCleanedBox.set_spacing(10)

        self.toBeCleanedLabel = Gtk.Label()
        self.toBeCleanedLabel.set_markup("To be cleaned:")
        self.toBeCleanedBox.append(self.toBeCleanedLabel)
        self.listBox = Gtk.ListBox(selection_mode = Gtk.SelectionMode.NONE)
        self.listBox.get_style_context().add_class("boxed-list")
        self.toBeCleanedBox.append(self.listBox)
        self.box.append(self.toBeCleanedBox)

        self.connect("realize", self.init_initiate)

    def init_initiate(self, app):
        self.scroll.set_child(self.boxLoading)
        th = threading.Thread(target=self.initiate, args=(app))
        th.start()

    def initiate(self, app, kwargs):
        flatpakList = subprocess.run(['flatpak-spawn', '--host', 'flatpak', '--columns=app', 'list'], stdout=subprocess.PIPE)
        flatpakList = flatpakList.stdout.decode('utf-8').split("\n")

        varApp = listdir(".var/app")

        self.leftoverData = []

        for existingDataDirectory in varApp:
            if ((os.path.exists(".var/app/" + existingDataDirectory + "/cache"))
                and (os.path.exists(".var/app/" + existingDataDirectory + "/config"))
                and (os.path.exists(".var/app/" + existingDataDirectory + "/data"))
                and (" " not in existingDataDirectory)
                and (existingDataDirectory not in flatpakList)):
                    self.leftoverDataSize += sum(foundFile.stat().st_size for foundFile in Path('.var/app/' + existingDataDirectory).glob('**/*') if foundFile.is_file())
                    if (existingDataDirectory not in self.leftoverData):
                        self.leftoverData.append(existingDataDirectory)

        for folder in self.leftoverData:
            self.listBoxRow = Adw.ActionRow(title = folder)
            self.listBox.append(self.listBoxRow)

        self.leftoverDataSize = int(((self.leftoverDataSize / 1024) / 1024) * 1.048576)

        self.labelMB.set_markup("<span size=\"80000\" weight=\"bold\">" + str(self.leftoverDataSize) + "</span>")
        self.scroll.set_child(self.box)

    def show_about(self, app):
        dialog = Adw.AboutWindow(transient_for=self)
        dialog.set_application_name("Flatsweep")
        dialog.set_version("v2023.7.27")
        dialog.set_developer_name("Giant Pink Robots!")
        dialog.set_license_type(Gtk.License(Gtk.License.MPL_2_0))
        dialog.set_comments("Flatpak leftover cleaner")
        dialog.set_website("https://github.com/giantpinkrobots/flatsweep")
        dialog.set_issue_url("https://github.com/giantpinkrobots/flatsweep/issues")
        dialog.set_copyright("2023 Giant Pink Robots!\n\nThe Flatsweep logo was created using the official Flatpak logo as a base, which is licensed under the Creative Commons Attribution 3.0 license. flatpak.org")
        dialog.set_developers(["Giant Pink Robots!"])
        dialog.set_application_icon("io.github.giantpinkrobots.flatsweep")
        dialog.show()

    def init_clean(self, app):
        self.scroll.set_child(self.boxCleaning)
        th = threading.Thread(target=self.clean, args=(app))
        th.start()

    def clean(self, app):
        cleanedData = 0
        for folder in self.leftoverData:
            if (os.path.exists(".var/app/" + folder)):
                try:
                    dataSize = sum(foundFile.stat().st_size for foundFile in Path('.var/app/' + folder).glob('**/*') if foundFile.is_file())
                    shutil.rmtree(".var/app/" + folder)
                    cleanedData += dataSize
                except:
                    self.deleteErrors = True
            if (os.path.exists(".local/share/flatpak/app/" + folder)):
                try:
                    dataSize = sum(foundFile.stat().st_size for foundFile in Path('.var/app/' + folder).glob('**/*') if foundFile.is_file())
                    shutil.rmtree(".local/share/flatpak/app/" + folder)
                    cleanedData += dataSize
                except:
                    self.deleteErrors = True

        cleanedData = int(((cleanedData / 1024) / 1024) * 1.048576)
        self.cleanedLabel.set_markup("<span size=\"80000\" weight=\"bold\">" + str(cleanedData) + "</span>")
        if (self.deleteErrors == True):
            self.cleanedLabelErrors.set_markup("<span size=\"15000\">Some files could not be deleted.</span>")
        self.scroll.set_child(self.boxCleaned)

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

def main(version):
    app = MyApp(application_id="io.github.giantpinkrobots.flatsweep")
    return app.run(sys.argv)
