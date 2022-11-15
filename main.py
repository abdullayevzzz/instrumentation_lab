#  pip install -U pyvisa
# enable Compatibility in USB configuration in Oscilloscope Menu
# press 'Utility' button -> choose 'I/O' -> enable 'Compatibility Mode'

import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
my_inst_addr = None
for item in rm.list_resources():
    if 'USB' in item and '::INSTR' in item:
        my_inst_addr = item
my_inst = rm.open_resource(my_inst_addr)

my_inst.timeout = 15000
my_inst.clear()
my_inst.read_termination = '\n'
my_inst.write_termination = '\n'

print('test_IDN: ', end='')
print(my_inst.query("*IDN?"))

print('test_CLS')
my_inst.write("*CLS")

print('test_RST')
my_inst.write("*RST")

print('test_autoscale')
my_inst.write(":AUToscale")

print('test_set_trigger_mode_edge')
my_inst.write(":TRIGger:MODE EDGE")

print('test_check_trigger_mode: ', end='')
print(my_inst.query(":TRIGger:MODE?"))

