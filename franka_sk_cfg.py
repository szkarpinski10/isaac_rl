
from __future__ import annotations

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg
from isaaclab.envs import DirectRLEnvCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim import SimulationCfg
from isaaclab.terrains import TerrainImporterCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR, ISAACLAB_NUCLEUS_DIR
from isaaclab.utils.configclass import configclass

@configclass
class FrankaSkCfg(DirectRLEnvCfg):
    episode_length_= 9999 #dlugosc trwania 
    decimation = 2
    action_space = 9 
    observation_space = 23
    state_space = 0 

    sim: SimulationCfg = SimulationCfg(
        dt = 1/120,
        render_interval=decimation,
        physics_material = sim_utils.RigidBodyMaterialCfg(
            friction_material = "multiply",
            restitution_combine_mode = "multiply",
            static_friction = 1.0,
            dynamic_friction = 1.0,
            restitution = 0.0,
        ),
     )

    scene: InteractiveSceneCfg = InteractiveSceneCfg (
        num_envs = 4096,
        env_spacing = 3.0,
        replicate_physics = True,
        clone_in_fabric = True
    )

    robot = ArticulationCfg(
        prim_path = "World/envs/env.*/Robot",
        spawn = sim_utils.UsdFileCfg(
            usd_path = f"{}"
        )
    )