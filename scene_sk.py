
from __future__ import annotations

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg, AssetBaseCfg, RigidObjectCfg
from isaaclab.envs import DirectRLEnvCfg, ManagerBasedRLEnvCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim import SimulationCfg
from isaaclab.terrains import TerrainImporterCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR, ISAACLAB_NUCLEUS_DIR
from isaaclab.utils.configclass import configclass
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg, GroundPlaneCfg

from isaaclab_assets import FRANKA_PANDA_CFG
import isaaclab.envs.mdp as mdp
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab_tasks.manager_based.manipulation.stack.mdp import franka_stack_events

from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab.managers import ActionTermCfg as ActionTerm
from isaaclab.utils.configclass import configclass

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



@configclass
class Event_rand_SK:
    randomize_cube_positions= EventTerm(
        func=franka_stack_events.randomize_object_pose,
        mode="reset",
        params={
            "pose_range": {"x": (-0.3,0.3),"y":(-0.3,0.3),"z":(0.0,0.0),"yaw": (0.0,0.0,0.0)},
            "min_separation": 0.1,
            #"velocity_range": {},
            "asset_cfgs": SceneEntityCfg("cube"),
        }
    )
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


@configclass
class ActionsCfg:
    """Pusta konfiguracja akcji na start"""

    pass


@configclass
class ObservationsCfg:
    """Pusta konfiguracja obserwacji"""

    @configclass
    class PolicyCfg:
        pass

    policy: PolicyCfg = PolicyCfg()


@configclass
class RewardsCfg:
    """Pusta konfiguracja nagród"""

    pass


@configclass
class TerminationsCfg:
    """Pusta konfiguracja zakończeń"""

    pass

@configclass
class FrankaEnvCfg_SK(ManagerBasedRLEnvCfg):

    scene: FrankaSceneCfg_SK = FrankaSceneCfg_SK(num_envs=9, env_spacing=3.0)
    events: Event_rand_SK = Event_rand_SK()
    observations: ObservationsCfg = ObservationsCfg()
    actions: ActionsCfg = ActionsCfg()
    rewards: RewardsCfg = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()

    def __post_init__(self):
        self.decimation=2
        self.episode_length_s=90
        self.sim.dt=0.01
        self.sim.render_interval=self.decimation