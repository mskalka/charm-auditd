from templating

from charms.reactive import when, when_not, set_flag
from charm.auditd.auditd import (
    write_configs,
    restart_auditd,
)

@when_not('auditd.installed')
def install_auditd():
    # Maybe do something here?
    set_flag('src.installed')


@reactive.hook('config-changed')
def config_changed():
    status_set('maintenance', 'Updating auditd configuration')
    write_configs()
    restart_auditd()
    status_set('active', 'Unit is ready.')
