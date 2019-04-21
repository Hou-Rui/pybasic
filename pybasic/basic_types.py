from .symbol_table import global_table

global_table.set('Integer', int)
global_table.set('Decimal', float)
global_table.set('String', str)