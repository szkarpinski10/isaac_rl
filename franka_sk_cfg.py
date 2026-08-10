
from __future__ import annotations

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg, AssetBaseCfg
from isaaclab.envs import DirectRLEnvCfg, ManagerBasedRLEnvCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim import SimulationCfg
from isaaclab.terrains import TerrainImporterCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR, ISAACLAB_NUCLEUS_DIR
from isaaclab.utils.configclass import configclass

@configclass
class FrankaSceneCfg_SK(InteractiveSceneCfg):


#robot -------------------------------------------------------------------------------------------------------------------------------
    robot = ArticulationCfg(
        prim_path = "/World/envs/env.*/Robot",
        spawn = sim_utils.UsdFileCfg(
            usd_path = f"{ISAACLAB_NUCLEUS_DIR}/Robots/FrankaEmika/Legacy/panda_instanceable.usd",
            activate_contact_sensors=False,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity= False,
                max_depenetration_velocity=5.0,

            ),
            articulation_props=sim_utils.ArticulationRootPropertiesCfg(
                enabled_self_collisions=False,
                solver_position_iteration_count=12,
                solver_velocity_iteration_count=1,
            ),

        ),
        init_state=ArticulationCfg.InitialStateCfg(
            joint_pos={
                "panda_joint1":0.0,
                "panda_joint2":0.0,
                "panda_joint3":0.0,
                "panda_joint4":0.0,
                "panda_joint5":0.0,
                "panda_joint6":0.0,
                "panda_joint7":0.0,
                "panda_finger_joint.*":0.4,
            },
            pos=(0.0,0.0,0.0),
            rot=(1.0,0.0,0.0,0.0),
        ),
        actuators={
            "panda_shoulder":ImplicitActuatorCfg(
                joint_names_expr=["panda_joint[1-4]"],
                effort_limit_sim=87.0, # wartos w N
                stiffness=80.0, 
                damping=4.0, 
            ),

            "panda_forearm":ImplicitActuatorCfg(
                joint_names_expr=["panda_joint[5-7]"],
                effort_limit_sim=12.0, # wartos w N
                stiffness=80.0, 
                damping=4.0, 
            ),


            "panda_hand":ImplicitActuatorCfg(
                joint_names_expr=["panda_finger_joint.*"],
                effort_limit_sim=200.0, # wartos w N
                stiffness=2e3, 
                damping=1e2, 
            ),

        }
    )

#stół -------------------------------------------------------------------------------------------------------------------------------
    table=AssetBaseCfg(
        prim_path="/World/envs/env.*/table",
        spawn=sim_utils.UsdFileCfg(
            usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Tables/table.usd",
        ),
        init_state=AssetBaseCfg.InitialStateCfg(
            pos=(0.5,0.0,0.0),
        ),
    )

    terrain=TerrainImporterCfg(
        prim_path="/World/ground",
        terrain_type="plane",
        collision_group=-1,
        physics_material=sim_utils.RigidBodyMaterialCfg(
            friction_combine_mode="multiply",
            restitution_combine_mode="multiply",
            static_friction=1.0,
            dynamic_friction=1.0,
            restitution=0.0,
        )
    )

    #-----------