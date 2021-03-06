#!/usr/bin/env python3
import html, http.cookies
import cgi
import os
import funct, sql
from configparser import ConfigParser, ExtendedInterpolation
import glob
from configparser import ConfigParser, ExtendedInterpolation
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates/'))
template = env.get_template('delver.html')
print('Content-type: text/html\n')
funct.check_login()
funct.page_for_admin()
form = cgi.FieldStorage()
serv = form.getvalue('serv')
stderr = ""
aftersave = ""
file = set()

try:
	cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
	user_id = cookie.get('uuid')
	user = sql.get_user_name_by_uuid(user_id.value)
	servers = sql.get_dick_permit()
except:
	pass

path_config = "haproxy-webintarface.config"
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(path_config)
form = cgi.FieldStorage()
serv = form.getvalue('serv')
Select = form.getvalue('del')
hap_configs_dir = config.get('configs', 'haproxy_save_configs_dir')

def get_files():
	import glob
	file = set()
	return_files = set()
	for files in glob.glob(os.path.join(hap_configs_dir,'*.cfg')):		
		file.add(files.split('/')[6])
	files = sorted(file, reverse=True)
	for file in files:
		ip = file.split("-")
		if serv == ip[0]:
			return_files.add(file)
	return sorted(return_files, reverse=True)

if serv is not None and form.getvalue('open') is not None:
	if Select is not None:
		aftersave = 1
		for get in form:
			if "cfg" in get:
				try:
					os.remove(os.path.join(hap_configs_dir, form.getvalue(get)))
					file.add(form.getvalue(get) + "<br />")
					funct.logging(serv, "delver.py deleted config: %s" % form.getvalue(get))				
				except OSError: 
					stderr = "Error: %s - %s." % (e.filename,e.strerror)
		print('<meta http-equiv="refresh" content="10; url=delver.py?serv=%s&open=open">' % form.getvalue('serv'))		
		
output_from_parsed_template = template.render(h2 = 1, title = "Delete old versions HAProxy config",
													role = sql.get_user_role_by_uuid(user_id.value),
													action = "delver.py",
													user = user,
													select_id = "serv",
													serv = serv,
													aftersave = aftersave,
													return_files = get_files(),
													selects = servers,
													stderr = stderr,
													open = form.getvalue('open'),
													Select = form.getvalue('del'),
													file = file)
print(output_from_parsed_template)