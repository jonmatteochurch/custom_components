"""Constants for ZBMINIR2 Mock."""
DOMAIN = "zbminir2_mock"

CONF_NAME = "name"
CONF_INCHING_CONTROL = "inching_control"
CONF_INCHING_TIME = "inching_time"
CONF_INCHING_MODE = "inching_mode"

INCHING_CONTROLS = ["ENABLE", "DISABLE"]
INCHING_MODES = ["ON", "OFF"]

STATE_DELAYED_POWER_ON_STATE = "delayed_power_on_state"
STATE_DELAYED_POWER_ON_TIME = "delayed_power_on_time"
STATE_DETACH_RELAY_MODE = "detach_relay_mode"
STATE_EXTERNAL_TRIGGER_MODE = "external_trigger_mode"
STATE_LINKQUALITY = "linkquality"
STATE_POWER_ON_BEHAVIOR = "power_on_behavior"
STATE_STATE = "state"
STATE_TURBO_MODE = "turbo_mode"
STATE_UPDATE = "update"

EXTERNAL_TRIGGER_MODES = ["edge", "pulse", "following(off)", "following(on)"]
POWER_ON_BEHAVIORS = ["off", "on", "toggle", "previous"]