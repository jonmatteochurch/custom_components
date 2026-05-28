"""Constants for S520619 Mock."""
DOMAIN = "s520619_mock"

CONF_NAME = "name"
CONF_MEASUREMENT_POLL_INTERVAL = "measurement_poll_interval"
CONF_TEMPERATURE_CALIBRATION = "temperature_calibration"
CONF_TEMPERATURE_PRECISION = "temperature_precision"
CONF_THERMOSTAT_UNIT = "thermostat_unit"
CONF_NO_OCCUPANCY_SINCE = "no_occupancy_since"

THERMOSTAT_UNITS = ["celsius", "fahrenheit"]

STATE_KEYPAD_LOCKOUT = "keypad_lockout"
STATE_LINKQUALITY = "linkquality"
STATE_LOCAL_TEMPERATURE = "local_temperature"
STATE_OCCUPANCY = "occupancy"
STATE_OCCUPIED_COOLING_SETPOINT = "occupied_cooling_setpoint"
STATE_OCCUPIED_HEATING_SETPOINT = "occupied_heating_setpoint"
STATE_PI_HEATING_DEMAND = "pi_heating_demand"
STATE_RUNNING_STATE = "running_state"
STATE_SCHNEIDER_PILOT_MODE = "schneider_pilot_mode"
STATE_SYSTEM_MODE = "system_mode"
STATE_TEMPERATURE_DISPLAY_MODE = "temperature_display_mode"
STATE_PI_COOLING_DEMAND = "pi_cooling_demand"
STATE_TEMPERATURE = "temperature"

KEYPAD_LOCKOUTS = ["unlocked", "lock", "lock1"]
RUNNING_STATES = ["idle", "heat", "cool"]
SCHNEIDER_PILOT_MODES = ["contactor", "pilot"]
SYSTEM_MODES = ["off", "heat", "cool"]
TEMPERATURE_DISPLAY_MODES = ["celsius", "fahrenheit"]
