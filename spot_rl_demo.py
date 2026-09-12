# Copyright (c) 2024 Boston Dynamics AI Institute LLC. All rights reserved.

import argparse
import sys
from pathlib import Path

import bosdyn.client.util
import orbit.orbit_configuration
from orbit.onnx_command_generator import (
    OnnxCommandGenerator,
    OnnxControllerContext,
    StateHandler,
)
from spot.mock_spot import MockSpot
from spot.spot import Spot
from utils.event_divider import EventDivider

def main():
    """Command line interface. change that is ok"""
    parser = argparse.ArgumentParser()
    bosdyn.client.util.add_base_arguments(parser)
    parser.add_argument("--policy_file_path", type=Path)
    parser.add_argument("-m", "--mock", action="store_true")
    options = parser.parse_args()

    conf_file = options.policy_file_path / "env_cfg.json"
    policy_file = options.policy_file_path / "policy.onnx"

    context = OnnxControllerContext()
    config = orbit.orbit_configuration.load_configuration(conf_file)
    print(config)

    state_handler = StateHandler(context)
    print(options.verbose)
    command_generator = OnnxCommandGenerator(context, config, policy_file, options.verbose)

    # 333 Hz state update / 6 => ~56 Hz control updates
    timeing_policy = EventDivider(context.event, 6)

    if options.mock:
        spot = MockSpot()
    else:
        spot = Spot(options)

    with spot.lease_keep_alive():
        try:
            spot.power_on()
            spot.stand(0.0)
            spot.start_state_stream(state_handler)

            input("Press Enter to start policy...")
            spot.start_command_stream(command_generator, timeing_policy)

            input("Press Enter to stop...")

        except KeyboardInterrupt:
            print("killed with ctrl-c")

        finally:
            print("stop command stream")
            spot.stop_command_stream()
            print("stop state stream")
            spot.stop_state_stream()
            print("powering off")
            spot.power_off()
            print("all stopped")


if __name__ == "__main__":
    if not main():
        sys.exit(1)
