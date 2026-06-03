"""Constants for MINI-ZB2GS Mock."""
DOMAIN = "minizb2gs_mock"

CONF_NAME = "name"
CONF_INCHING_CONTROL_L1 = "inching_control_l1"
CONF_INCHING_CONTROL_L2 = "inching_control_l2"
CONF_INCHING_TIME_L1 = "inching_time_l1"
CONF_INCHING_TIME_L2 = "inching_time_l2"
CONF_INCHING_MODE_L1 = "inching_mode_l1"
CONF_INCHING_MODE_L2 = "inching_mode_l2"

INCHING_CONTROLS = ["ENABLE", "DISABLE"]
INCHING_MODES = ["ON", "OFF"]

STATE_DELAYED_POWER_ON_STATE_CHANNEL_1_L1 = "delayed_power_on_state_channel_1_l1"
STATE_DELAYED_POWER_ON_STATE_CHANNEL_2_L2 = "delayed_power_on_state_channel_2_l2"
STATE_DELAYED_POWER_ON_TIME_L1 = "delayed_power_on_time_l1"
STATE_DELAYED_POWER_ON_TIME_L2 = "delayed_power_on_time_l2"
STATE_DETACH_RELAY_MODE = "detach_relay_mode"
STATE_DETACH_RELAY_OUTLET1 = "detach_relay_outlet1"
STATE_DETACH_RELAY_OUTLET2 = "detach_relay_outlet2"
STATE_DETACH_RELAY_OUTLET3 = "detach_relay_outlet3"
STATE_EXTERNAL_TRIGGER_MODE_L1 = "external_trigger_mode_l1"
STATE_EXTERNAL_TRIGGER_MODE_L2 = "external_trigger_mode_l2"
STATE_LINKQUALITY = "linkquality"
STATE_POWER_ON_BEHAVIOR_L1 = "power_on_behavior_l1"
STATE_POWER_ON_BEHAVIOR_L2 = "power_on_behavior_l2"
STATE_STATE = "state"
STATE_TURBO_MODE = "turbo_mode"
STATE_UPDATE = "update"

EXTERNAL_TRIGGER_MODES = ["edge", "pulse", "following(off)", "following(on)"]
POWER_ON_BEHAVIORS = ["off", "on", "toggle", "previous"]