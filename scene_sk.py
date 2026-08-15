from __future__ import annotations

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg, AssetBaseCfg, RigidObjectCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import GroundPlaneCfg
from isaaclab.utils.configclass import configclass

from isaaclab_assets import FRANKA_PANDA_CFG
@configclass
class FrankaSceneCfg_SK(InteractiveSceneCfg):


    #robot -------------------------------------------------------------------------------------------------------------------------------
    robot = FRANKA_PANDA_CFG.replace(
        prim_path="{ENV_REGEX_NS}/Robot",
        init_state=ArticulationCfg.InitialStateCfg(
            joint_pos={
                "panda_joint1": 1.157,
                "panda_joint2": -1.066,
                "panda_joint3": -0.155,
                "panda_joint4": -2.239,
                "panda_joint5": -1.841,
                "panda_joint6": 1.003,
                "panda_joint7": 0.469,
                "panda_finger_joint.*": 0.035,
        },
        pos=(0.0, 0.0, 0.5),
        rot=(1.0, 0.0, 0.0, 0.0),
        ),
        actuators={
        "panda_shoulder": ImplicitActuatorCfg(
            joint_names_expr=["panda_joint[1-4]"],
            effort_limit_sim=87.0,  # wartość w Nm
            stiffness=80.0,
            damping=4.0,
        ),
        "panda_forearm": ImplicitActuatorCfg(
            joint_names_expr=["panda_joint[5-7]"],
            effort_limit_sim=12.0,  # wartość w Nm
            stiffness=80.0,
            damping=4.0,
        ),
        "panda_hand": ImplicitActuatorCfg(
            joint_names_expr=["panda_finger_joint.*"],
            effort_limit_sim=200.0,  # wartość w N
            stiffness=2e3,
            damping=1e2,
        ),
    },
)





    #stół -------------------------------------------------------------------------------------------------------------------------------
    table = AssetBaseCfg(
        prim_path="{ENV_REGEX_NS}/Table",
        init_state=AssetBaseCfg.InitialStateCfg(pos=[0.5,0,0.3],rot=[1.0,0,0,0]),
        spawn=sim_utils.CuboidCfg(
            size=(1.6, 1.2, 0.5), 
            collision_props=sim_utils.CollisionPropertiesCfg(),
            visual_material=sim_utils.PreviewSurfaceCfg(
                diffuse_color=(0.2, 0.2, 0.2), 
            ),
        ),
    )

    #podłoga -------------------------------------------------------------------------------------------------------------------------------
    ground= AssetBaseCfg(
        prim_path="/World/GroundPlane",
        init_state=AssetBaseCfg.InitialStateCfg(pos=[0,0,0]),
        spawn=GroundPlaneCfg(),
    )

    #kostka -------------------------------------------------------------------------------------------------------------------------------

    cube = RigidObjectCfg(
    prim_path="{ENV_REGEX_NS}/Cube",
    init_state=RigidObjectCfg.InitialStateCfg(
        pos=(0.5,0.0,1.08),
    ),
    spawn = sim_utils.CuboidCfg(
        size=(0.05,0.05,0.05),
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,

        ),
        collision_props=sim_utils.CollisionPropertiesCfg(),
        visual_material=sim_utils.PreviewSurfaceCfg(
            diffuse_color=(1.0,0.0,0.0),
        ),
        physics_material=sim_utils.RigidBodyMaterialCfg(
            static_friction=0.5,
            dynamic_friction=0.4,
        ),
    ),
    )

    #light ------------------------------------------------------------------------------------------------------------------------------
    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DomeLightCfg(color=(0.75, 0.75, 0.75), intensity=3000.0),
    )




