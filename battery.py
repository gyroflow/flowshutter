import vars, target

bat = target.init_bat()
#vars
bat_deadzone = 0.0 # half width of voltage dead zone between each bat_state to avoid jumping bat states due to noise
bat_state_limits = [3.3, 3.6, 3.7, 4., 4.2] #upper limits of each bat.

#linear fit from measuring adc values at diferent voltages
adc_v_slope = 0.001305 # unit volt
adc_v_offset = 0.3471

def check(t):
    
    bat_readout = bat.read()
    bat_scaled = scale(bat_readout)
    print(bat_readout)
    set_batstate(bat_scaled)
    vars.bat_voltage=bat_scaled

def scale(adcValue):
    v_scaled = adcValue*adc_v_slope + adc_v_offset #TODO add scaling according to voltage divider
    return v_scaled

def set_batstate(v):
    
    if v <= bat_state_limits[0] - bat_deadzone:
        vars.bat_state=0
    elif (bat_state_limits[0] + bat_deadzone <= v <= bat_state_limits[1] - bat_deadzone):
        vars.bat_state=1
    elif (bat_state_limits[1] + bat_deadzone <= v <= bat_state_limits[2] - bat_deadzone):
        vars.bat_state=2
    elif (bat_state_limits[2] + bat_deadzone <= v <= bat_state_limits[3] - bat_deadzone):
        vars.bat_state=3
    elif (bat_state_limits[3] + bat_deadzone <= v <= bat_state_limits[4] - bat_deadzone):
        vars.bat_state=4
    elif (v >= bat_state_limits[4] + bat_deadzone):
        vars.bat_state=5
        
    else:
        pass # do not update batstate within deadzones