"""Test the ILIFE T20s enum range quirk."""

import json

from tests import create_device
from tuya_device_handlers.device_wrapper.common import DPCodeEnumWrapper
from tuya_device_handlers.registry import QuirksRegistry


def test_status_enum_extended(
    filled_quirks_registry: QuirksRegistry,
) -> None:
    """The quirk adds the docked and cleaning status values."""
    device = create_device("sd_akwrlayfaxcckgfv.json")
    assert device.status["status"] == "base_sleeping"

    wrapper = DPCodeEnumWrapper.find_dpcode(device, "status")
    assert wrapper is not None
    assert wrapper.read_device_status(device) is None

    filled_quirks_registry.initialise_device_quirk(device)

    wrapper = DPCodeEnumWrapper.find_dpcode(device, "status")
    assert wrapper is not None
    assert wrapper.read_device_status(device) == "base_sleeping"


def test_cistern_enum_extended(
    filled_quirks_registry: QuirksRegistry,
) -> None:
    """The quirk adds the missing `closed` cistern value."""
    device = create_device("sd_akwrlayfaxcckgfv.json")
    assert device.status["cistern"] == "closed"

    before = json.loads(device.status_range["cistern"].values)["range"]
    assert "closed" not in before

    filled_quirks_registry.initialise_device_quirk(device)

    after = json.loads(device.status_range["cistern"].values)["range"]
    assert "closed" in after
