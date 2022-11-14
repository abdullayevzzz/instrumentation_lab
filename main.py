#  pip install -U pyvisa
#  pip install -U pyvisa-py

import pyvisa
rm = pyvisa.ResourceManager()
# rm = pyvisa.ResourceManager('@py')  # pure python backend instead of NI-VISA
print(rm)
rm.list_resources()
# my_inst = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C1234567890::INSTR')
# print(my_inst)
# print(my_inst.query("*IDN?"))
