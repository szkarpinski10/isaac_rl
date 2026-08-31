# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""This script demonstrates how to create a simple stage in Isaac Sim.

.. code-block:: bash

    # Usage
    ./isaaclab.sh -p scripts/tutorials/00_sim/create_empty.py

"""

"""Launch Isaac Sim Simulator first."""


import argparse
from isaaclab.app import AppLauncher

# create argparser
parser = argparse.ArgumentParser(description="Learning environment.")
# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()
# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""


import torch
from isaaclab.envs import ManagerBasedRLEnv
from isaaclab.sim import SimulationCfg, SimulationContext
from franka_SK import Franka_Env_Cfg

def main():
    """Main function."""

    env_cfg = Franka_Env_Cfg()
    env = ManagerBasedRLEnv(cfg=env_cfg)
    obs, _ = env.reset()
    print("env ready")
    


    while simulation_app.is_running():
        # perform step
        random_actions = 2.0 * torch.rand(
            (env.num_envs, env.action_space.shape[1]), 
            device=env.device
        ) - 1.0
        
        obs, rewards, dones, truncated, info = env.step(random_actions)

if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
