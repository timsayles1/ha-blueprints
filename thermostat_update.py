ATTR_THERMOSTAT = "thermostat"
ATTR_SENSOR = "sensor"
ATTR_STATE_ONLY = "state_only"
ATTR_TEMP_ONLY = "temp_only"
ATTR_CURRENT_TEMP = "current_temperature"
ATTR_HVAC_MODE = "hvac_modes"
ATTR_FAN_MODE = "fan_mode"
ATTR_TEMPERATURE = "temperature"
ATTR_HIGH = "target_temp_high"
ATTR_LOW = "target_temp_low"

ATTR_HVAC_MODE_DEFAULT = ["heat_cool"]
ATTR_FAN_MODE_DEFAULT = ["auto"]
ATTR_HIGH_DEFAULT = 73
ATTR_LOW_DEFAULT = 70
ATTR_TEMP_DEFAULT = 70
ATTR_STATE_ONLY_DEFAULT = False
ATTR_TEMP_ONLY_DEFAULT = False

thermostat_id = data.get(ATTR_THERMOSTAT)
sensor_id = data.get(ATTR_SENSOR)
hvac_state = data.get(ATTR_HVAC_MODE, ATTR_HVAC_MODE_DEFAULT)
fan_state = data.get(ATTR_FAN_MODE, ATTR_FAN_MODE_DEFAULT)
high_temp = float(data.get(ATTR_HIGH, ATTR_HIGH_DEFAULT))
low_temp = float(data.get(ATTR_LOW, ATTR_LOW_DEFAULT))
target_temp = float(data.get(ATTR_TEMPERATURE, ATTR_TEMP_DEFAULT))
state_only = data.get(ATTR_STATE_ONLY, ATTR_STATE_ONLY_DEFAULT)
temp_only = data.get(ATTR_TEMP_ONLY, ATTR_TEMP_ONLY_DEFAULT)
logger.info("Command state %s temp %s", state_only, temp_only)
logger.info("Thermostat %s state %s", thermostat_id, hvac_state)
logger.info("Fan state %s", fan_state)
if state_only and temp_only:
    logger.error("You can't use state_only and temp_only at the same time! Ignoring.")
    state_only = False
    temp_only = False

temp = None

if not thermostat_id:
    logger.error("Expected %s entity_id, got: %s.", ATTR_THERMOSTAT, thermostat_id)
else:
    thermostat = hass.states.get(thermostat_id)
    if thermostat is None:
        logger.error("Could not get state of %s.", thermostat_id)
    else:
        attributes = thermostat.attributes.copy()
        if not state_only:
            if sensor_id:
                try:
                    temp = float(hass.states.get(sensor_id).state)
                except (ValueError, TypeError):
                    logger.error("Could not get state of %s", sensor_id)
                if temp is None:
                    logger.error("Could not get state of %s.", sensor_id)
                else:
                    attributes[ATTR_CURRENT_TEMP] = temp
                    logger.info("Set temp to %s from %s", temp, sensor_id)
            else:
                logger.error("Expected %s entity_id, got: %s.", ATTR_SENSOR, sensor_id)
        if not temp_only:
            state = [hvac_state][0]
            attributes[ATTR_FAN_MODE] = [fan_state][0]
        if temp_only:
            state = [hvac_state][0]
            attributes[ATTR_FAN_MODE] = [fan_state][0]
            if [hvac_state][0] == "heat_cool":   
                attributes[ATTR_HIGH] = high_temp
                attributes[ATTR_LOW] = low_temp
                attributes[ATTR_TEMPERATURE] = None
                logger.info("HVAC State: %s Temps: High %s Low %s", [hvac_state][0], high_temp, low_temp)
            else:
                attributes[ATTR_TEMPERATURE] = target_temp
                attributes[ATTR_HIGH] = None
                attributes[ATTR_LOW] = None
                logger.info("HVAC State: %s Temps: Target %s", [hvac_state][0], target_temp)
        
        hass.states.set(thermostat_id, state, attributes)
