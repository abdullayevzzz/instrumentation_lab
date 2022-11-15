#  pip install -U pyvisa
# enable Compatibility in USB configuration in Oscilloscope Menu
# press 'Utility' button -> choose 'I/O' -> enable 'Compatibility Mode'
import struct
import pyvisa


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
print('Identification: ', end='')
print(my_inst.query("*IDN?"))


# ***INITIALIZATION***
print('Clear screen\n')
my_inst.write("*CLS")

print('Reset\n')
my_inst.write("*RST")

print('Autoscale\n')
my_inst.write(":AUToscale")

print('Set trigger mode to edge')
my_inst.write(":TRIGger:MODE EDGE")

print('Check trigger mode: ', end='')
print(my_inst.query(":TRIGger:MODE?"))


# ***MEASUREMENT***
print('Set measurement source')
my_inst.write(":MEASure:SOURce CHANnel1")

print('Check measurement source: ', end='')
print(my_inst.query(":MEASure:SOURce?"))

print('Measure amplitude: ', end='')
print(my_inst.query(":MEASure:VAMPlitude?").strip('\n\r'), '\n')

print('Measure frequency: ', end='')
print(my_inst.query(":MEASure:FREQuency?").strip('\n\r'), '\n')


# ***SIGNAL GENERATOR***
print('Set waveform generator amplitude voltage\n')
my_inst.write(":WGEN:VOLTage 0.5")

print('Set waveform generator frequency\n')
my_inst.write(":WGEN:FREQuency 2000")

print('Set waveform generator function\n')
my_inst.write(":WGEN:FUNCTion SINusoid")

print('Turn on waveform generator output\n')
my_inst.write(":WGEN:OUTPut ON")


# ***SAVING WAVEFORM***
print('Saving display image')
sDisplay = my_inst.query_binary_values(":DISPlay:DATA? PNG, COLor", datatype='s')
f = open("screen_image.png", "wb")
f.write(bytes(sDisplay))
f.close()
print("Screen image written to screen_image.png.\n")

print('Saving waveform data')
my_inst.write(":WAVeform:POINts:MODE RAW")  # set waveform points mode
my_inst.write(":WAVeform:POINts 10240")  # set number of waveform points
my_inst.write(":WAVeform:SOURce CHANnel1")  # set waveform source
my_inst.write(":WAVeform:FORMat BYTE")  # set data format
# Get numeric values for later calculations.
x_increment = float(my_inst.query(":WAVeform:XINCrement?"))
x_origin = float(my_inst.query(":WAVeform:XORigin?"))
y_increment = float(my_inst.query(":WAVeform:YINCrement?"))
y_origin = float(my_inst.query(":WAVeform:YORigin?"))
y_reference = float(my_inst.query(":WAVeform:YREFerence?"))
# Get the waveform data
sData = bytes(my_inst.query_binary_values(":WAVeform:DATA?", datatype='s'))
values = struct.unpack("%dB" % len(sData), sData)
# Save waveform data values to CSV file.
f = open("waveform_data.csv", "w")
for i in range(0, len(values) - 1):
    time_val = x_origin + (i * x_increment)
    voltage = ((values[i] - y_reference) * y_increment) + y_origin
    f.write("%E, %f\n" % (time_val, voltage))
f.close()
print("Waveform format BYTE data written to waveform_data.csv.")

my_inst.close()
