<p align="center"><img src="https://raw.githubusercontent.com/giantpinkrobots/flatsweep/052201fb59de4d6928479efe4646cd0d23bf2e33/screenshots/logo.svg" width=200 /></p>
<h1 align="center">Flatsweep</h1>
<h3 align="center">Flatpak leftover cleaner</h3>
<br><br>
<p align="center"><a href="https://flathub.org/apps/io.github.giantpinkrobots.flatsweep"><img src="https://dl.flathub.org/assets/badges/flathub-badge-i-en.svg" width=300 /></a></p>
When you uninstall a Flatpak, it can leave some files behind on your computer. Flatsweep helps you easily get rid of the residue left on your system by uninstalled Flatpaks.
<br><br>
Flatsweep uses GTK4 and Libadwaita to provide a coherent user interface that integrates nicely with GNOME, but you can use it on any desktop environment of course.
<p align="center"><img src="https://raw.githubusercontent.com/giantpinkrobots/flatsweep/main/screenshots/Screenshot-Flatsweep-1.png" width=500 /></p>
Caution: Flatsweep exclusively looks at the default Flatpak install directory. If you have set a custom install path, it might accidentally delete files that weren't supposed to be deleted. If you have no idea what a 'custom install path' is, you'll be fine.

## Building

Flatsweep was made with GNOME Builder, thus it is the program I recommend you to use when building it. Simply copying this repository into your system and opening it with GNOME Builder will allow you to build it with relative ease.

## Contributing

Contributions are always welcome! And also, here is a guide on how you can translate Flatsweep into your native (or not) language:

### Translating

#### Stage 1:

Localization in Flatsweep is done with separate Python files next to the main.py file. You can start by copying and pasting the "lang_en.py" file and name it according to the language you want. For example, "lang_es.py" for Spanish. In the language file you'll find many different variables with their text equivalents. Do not change the variable names, only change the bits that exist in between quotes.

#### Stage 2:

After creating the file, you have to go to the main.py file, and near the top, you will find a section named "TRANSLATIONS BEGIN". This is a set of if/elif/else statements. Before "else:", you should create an "elif" statement. Here is an example for Spanish:

```python
elif currentLanguage.startswith("es"):
    from flatsweep import lang_es as lang
```

Keep in mind, spacing is important in Python, so make sure the indentations are correct.

This is how it should look like after everything:

```python
#...
elif currentLanguage.startswith("es"):
    from flatsweep import lang_es as lang
else:
    from flatsweep import lang_en as lang
```

#### Stage 3:

Then, you have to go to the meson.build file that exists in the src folder, find the section called "flatsweep_sources", and add your language file at the end.

Here is an example of how it may look like beforehand:

```
flatsweep_sources = [
  'main.py',
  'lang_en.py',
  'lang_tr.py'
]
```

... and this is after you add Spanish:

```
flatsweep_sources = [
  'main.py',
  'lang_en.py',
  'lang_tr.py',
  'lang_es.py'
]
```

That's all there is to it.

#### Stage EXTRA:

You can also translate the appstream information. This is done within the "po" directory. You can use a program like Poedit to do this. After adding your language (e.g. es.po) you should also add the language line (e.g. es) into the "LINGUAS" file.
