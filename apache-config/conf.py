import yaml
from jinja2 import Template

with open('data.yml') as file:
    config_data = yaml.load(file, Loader=yaml.FullLoader)

with open('vhosts.j2') as file:
    template_html = file.read()

template = Template(template_html)
vhosts_conf = template.render(config_data)

#env = Environment(loader=FileSystemLoader('.'))
#template = env.get_template('vhosts.j2')

#output = template.render(virtual_hosts=data['virtual_hosts'])

with open('vhosts.conf', 'w') as file:
    file.write(vhosts_conf)
