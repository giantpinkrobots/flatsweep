pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'flatsweep')
gnome = import('gnome')

gnome.compile_resources('flatsweep',
  'flatsweep.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'flatsweep.in',
  output: 'flatsweep',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

flatsweep_sources = [
  'main.py',
  'lang_be.py',
  'lang_bg.py',
  'lang_en.py',
  'lang_tr.py',
  'lang_es.py',
  'lang_de.py',
  'lang_el.py',
  'lang_ru.py',
  'lang_zh.py',
  'lang_pl.py',
  'lang_fr.py',
  'lang_pt_BR.py',
  'lang_ar.py',
  'lang_it.py',
  'lang_vi.py'
]

install_data(flatsweep_sources, install_dir: moduledir)
