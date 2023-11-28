tATTR_THERMOSTAT = "thermostat"
ATTR_SENSOR = "sensor"
ATTR_CURRENT_TEMP = "current_temperature"
ATTR_HVAC_MODE = "hvac_mode"
ATTR_FAN_MODE = "fan_mode"
ATTR_TARGET = "temperature"
ATTR_HIGH = "target_temp_high"
ATTR_LOW = "target_temp_low"

ATTR_HVAC_MODE_DEFAULT = ["heat_cool"]
ATTR_FAN_MODE_DEFAULT = ["auto"]
ATTR_HIGH_DEFAULT = 73
ATTR_LOW_DEFAULT = 70
ATTR_TEMP_DEFAULT = 70
ATTR_THERM_MODE = "manual"
ATTR_HOLD_STATE_TOGGLE = "on"
ATTR_HOLD_STATE = "Hold"

thermostat_id = data.get(ATTR_THERMOSTAT)
sensor_id = data.get(ATTR_SENSOR)
hvac_state = data.get(ATTR_HVAC_MODE, ATTR_HVAC_MODE_DEFAULT)
fan_state = data.get(ATTR_FAN_MODE, ATTR_FAN_MODE_DEFAULT)
high_temp = float(data.get(ATTR_HIGH, ATTR_HIGH_DEFAULT))
low_temp = float(data.get(ATTR_LOW, ATTR_LOW_DEFAULT))
target_temp = float(data.get(ATTR_TARGET, ATTR_TEMP_DEFAULT))
therm_mode = data.get(ATTR_THERM_MODE)
hold_state = data.get(ATTR_HOLD_STATE)
hold_state_toggle = data.get(ATTR_HOLD_STATE_TOGGLE)
logger.info("Thermostat %s state %s", thermostat_id, hvac_state)
logger.info("Fan state %s", fan_state)
temp = None
if not thermostat_id:
    logger.error("Expected %s entity_id, got: %s.", ATTR_THERMOSTAT, thermostat_id)
else:
    thermostat = hass.states.get(thermostat_id)
    if thermostat is None:
        logger.error("Could not get state of %s.", thermostat_id)
    else:
        attributes = thermostat.attributes.copy()
        if sensor_id:
            temp = float(hass.states.get(sensor_id).state)
        else:
            logger.error("Expected %s entity_id, got: %s.", ATTR_SENSOR, sensor_id)
        if temp is None:
            logger.error("Could not get state of %s.", sensor_id)
        else:
            attributes[ATTR_CURRENT_TEMP] = temp
            logger.info("Set temp to %s from %s", temp, sensor_id)
            if [hvac_state][0] == "heat_cool":
                attributes[ATTR_HIGH] = high_temp
                attributes[ATTR_LOW] = low_temp
                attributes[ATTR_TARGET] = None
                logger.info(
                    "HVAC State: %s Temps: High %s Low %s",
                    [hvac_state][0],
                    high_temp,
                    low_temp,
                )
            else:
                attributes[ATTR_TARGET] = target_temp
                attributes[ATTR_HIGH] = None
                attributes[ATTR_LOW] = None
                logger.info(
                    "HVAC State: %s Temps: Target %s", [hvac_state][0], target_temp
                )

        state = [hvac_state][0]
        attributes[ATTR_FAN_MODE] = [fan_state][0]
        hass.states.set(thermostat_id, state, attributes)
