from jinja2 import Template
import os

from charmhelpers.core.host import (
    service_restart,
    compare
)
from charmhelpers.core.hookenv import config

TEMPLATES = 'templates/'
AUDITD_CFG = '/etc/postfix/auditd.conf'
AUDITD_RULES = '/etc/postfix/auditd.rules'


def write_configs():
    context = AuditdContext()()

    cfg_template_path = os.path.join(TEMPLATES, 'auditd.conf')
    with open(cfg_template_path) as t:
        cfg_template = Template(t.read())
    with open(AUDITD_CFG, 'w+') as f:
        f.write(cfg_template.render(context))

    rules_template_path = os.path.join(TEMPLATES, 'auditd.rules')
    with open(rules_template_path) as t:
        rules_template = Template(t.read())
    with open(AUDITD_RULES, 'w+') as f:
        f.write(rules_template.render(context))


def update_grub():
    """
    This seems risky.. confer with OSE team and Dima
    """
    with open('/etc/default/grub', 'w+') as grub:
        config = grub.readlines()
        for line in config:
            line_key = line.split('=', 1)[0]
            line_val = line.split('=', 1)[1].strip('"')
            pos = config.index(line)
            if line_key == 'GRUB_CMDLINE_LINUX':
                if not 'audit=1' in line_val:
                    line_val = [line_val, 'audit=1']
                    line_val = ','.join(line_val)
                    line = '{}="{}"'.format(line_key, line_val)
                config[pos] = line
        grub.write(config)
    subprocess.check_call('update-grub')


class AuditdContext():
    def __call__(self):
        ctxt =  {}
        ctxt['config'] = config()
        return ctxt
