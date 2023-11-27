"""
This script updates the Carrier Infinity state and current
temperature from external sensor.
Arguments:
 - thermostat			      - thermostat entity_id (required)
 - sensor				        - sensor entity_id (required)
 - state_only           - with state_only set to 'true' script will update only state
                          of the thermostat (optional)
 - temp_only            - with temp_only set to 'true' script will update only
                          current_temperature of the thermostat (optional)

Configuration example:

service: python_script.thermostat_update

"""
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

ATTR_HVAC_MODE_DEFAULT = "heat_cool"
ATTR_FAN_MODE_DEFAULT = "auto"
ATTR_HIGH_DEFAULT = 73
ATTR_LOW_DEFAULT = 70
ATTR_STATE_ONLY_DEFAULT = False
ATTR_TEMP_ONLY_DEFAULT = False

thermostat_id = data.get(ATTR_THERMOSTAT)
sensor_id = data.get(ATTR_SENSOR)
hvac_state = data.get(ATTR_HVAC_MODE, ATTR_HVAC_MODE_DEFAULT)
fan_state = data.get(ATTR_FAN_MODE, ATTR_FAN_MODE_DEFAULT)
high_temp = float(data.get(ATTR_HIGH, ATTR_HIGH_DEFAULT))
low_temp = float(data.get(ATTR_LOW, ATTR_LOW_DEFAULT))
state_only = data.get(ATTR_STATE_ONLY, ATTR_STATE_ONLY_DEFAULT)
temp_only = data.get(ATTR_TEMP_ONLY, ATTR_TEMP_ONLY_DEFAULT)
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
            else:
                logger.error("Expected %s entity_id, got: %s.", ATTR_SENSOR, sensor_id)
        if not temp_only:
            attributes[ATTR_HVAC_MODE] = [hvac_state]
            attributes[ATTR_FAN_MODE] = [fan_state]
        if temp_only:
            state = hass.states.get(thermostat_id).state
            attributes[ATTR_HIGH] = high_temp
            attributes[ATTR_LOW] = low_temp
        
        hass.states.set(thermostat_id, state, attributes)
