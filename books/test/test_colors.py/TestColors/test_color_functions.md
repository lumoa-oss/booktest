# Color Functions Test


## Colors Disabled

is_color_enabled: False
red('ERROR'): 'ERROR'
yellow('WARNING'): 'WARNING'


## Colors Enabled

is_color_enabled: True
red('ERROR'): '\x1b[91mERROR\x1b[0m'
yellow('WARNING'): '\x1b[93mWARNING\x1b[0m'

✓ All color function tests passed!
