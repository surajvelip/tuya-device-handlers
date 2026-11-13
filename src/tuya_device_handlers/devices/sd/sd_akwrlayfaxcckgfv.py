"""Quirk for ILIFE T20s robot vacuum (product_id akwrlayfaxcckgfv).

The cloud database under-declares two enum datapoints:

- ``status`` (dpid 5) lists only the 12 generic values, but the device
  also reports docked states (``base_charging``, ``adapter_charging``,
  ``continuation_charging``, ``base_sleeping``, ``adapter_sleeping``)
  and cleaning modes (``smart``, ``edge``, ``explore``,
  ``explore_clean``), which are rejected as invalid ENUM values.
- ``cistern`` (dpid 10) omits ``closed``, which the device reports when
  the mop water tank is removed.

Redeclare the full ranges so Home Assistant accepts the reported values.

See https://github.com/home-assistant-libs/tuya-device-handlers/issues/756
"""

from tuya_device_handlers import TUYA_QUIRKS_REGISTRY
from tuya_device_handlers.builder import DeviceQuirk
from tuya_device_handlers.const import DPMode

(
    DeviceQuirk()
    .applies_to(product_id="akwrlayfaxcckgfv")
    .add_dpid_enum(
        dpid=5,
        dpcode="status",
        dpmode=DPMode.READ,
        enum_range=[
            "standby",
            "zone_clean",
            "part_clean",
            "cleaning",
            "paused",
            "goto_pos",
            "pos_arrived",
            "pos_unarrive",
            "goto_charge",
            "charging",
            "charge_done",
            "sleep",
            "smart",
            "edge",
            "explore",
            "explore_clean",
            "base_charging",
            "adapter_charging",
            "base_sleeping",
            "adapter_sleeping",
            "continuation_charging",
        ],
    )
    .add_dpid_enum(
        dpid=10,
        dpcode="cistern",
        dpmode=DPMode.READ | DPMode.WRITE,
        enum_range=["low", "middle", "high", "closed"],
    )
    .register(TUYA_QUIRKS_REGISTRY)
)
