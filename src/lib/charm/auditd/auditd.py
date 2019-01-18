from jinja2 import Template

from charmhelpers.core.host import (
    service_restart,
)
from charmhelpers.core.hookenv import config

TEMPLATES = 'templates/'
AUDITD_CFG = '/etc/postfix/auditd.conf'
AUDITD_RULES = '/etc/postfix/auditd.rules'


def restart_auditd():
    service_restart('')

def write_configs():
    


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
