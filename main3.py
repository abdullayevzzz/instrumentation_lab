import pyvisa
import matplotlib.pyplot as plt

# ****CONNECTION***
rm = pyvisa.ResourceManager()
print(rm.list_resources(), '\n')
my_inst_addr = None
for item in rm.list_resources():
    if 'USB' in item and '::INSTR' in item:
        my_inst_addr = item
my_inst = rm.open_resource(my_inst_addr)
my_inst.timeout = 15000
my_inst.clear()


# ***INITIALIZATION***
my_inst.write("*CLS")
my_inst.write("*RST")


# ***FREQUENCY RESPONSE***
my_inst.write(":WGEN:VOLTage 1.0")
my_inst.write(":WGEN:FREQuency 1")
my_inst.write(":WGEN:FUNCTion SINusoid")
my_inst.write(":WGEN:OUTPut ON")
freq_response = []
frequencies = [2 ** f for f in range(4, 14)]
for f in frequencies:
    my_inst.write(":WGEN:FREQuency %d" % f)
    my_inst.write(":AUToscale")
    voltage = my_inst.query(":MEASure:VAMPlitude?").strip('\n\r')
    freq_response.append(float(voltage))

plt.plot(frequencies, freq_response)
plt.ylabel('Frequency response - Voltage')
plt.xlabel('Frequency - Hertz')
plt.show()

freq_lower_bound = 400
freq_upper_bound = 500
# ***CUTOFF FREQUENCY***
my_inst.write(":WGEN:FREQuency %d" % freq_lower_bound)
my_inst.write(":AUToscale")
for f in range(freq_lower_bound, freq_upper_bound):
    my_inst.write(":WGEN:FREQuency %d" % f)
    voltage = my_inst.query(":MEASure:VAMPlitude?").strip('\n\r')
    if float(voltage) < 1 / (2 ** 0.5):
        print('cutoff: ', f)
        break

my_inst.close()
