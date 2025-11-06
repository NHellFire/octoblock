import yaml
from appdaemontestframework import automation_fixture
from freezegun import freeze_time

from apps.octoblock.octoblock import OctoBlock
from attrs import *

with open("tests/config.yaml") as f:
    config = yaml.safe_load(f)["octoblock"]


@automation_fixture(OctoBlock)
def octoblock(given_that):
    given_that.time_is(datetime.datetime(2025, 11, 6, 12, 0, 0, 0))

    for k, v in config.items():
        given_that.passed_arg(k).is_set_to(v)

    given_that.state_of("event.octopus_energy_electricity_current_day_rates").is_set_to("2025-11-06T11:38:41.367+00:00", current_day)

    given_that.state_of("event.octopus_energy_electricity_next_day_rates").is_set_to("2025-11-06T11:38:41.367+00:00", next_day)


def test_get_import_prices(octoblock):
    octoblock.get_import_prices()
    assert octoblock.incoming_tariff is not None


@freeze_time("2025-11-06 12:00:00")
def test_period_and_cost_callback(given_that, octoblock):
    octoblock.period_and_cost_callback(None)
