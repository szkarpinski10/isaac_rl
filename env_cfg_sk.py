from isaaclab.assets import ArticulationCfg, RigidObjectCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import FrameTransformerCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
from isaaclab.utils.configclass import configclass

from isaaclab_tasks.manager_based.manipulation.stack import mdp
from isaaclab_tasks.manager_based.manipulation.stack.mdp import franka_stack_events
from isaaclab_tasks.manager_based.manipulation.stack.stack_env_cfg import StackEnvCfg


@configclass
class EventCfg_SK:
    
    randomize_cube = EventTerm(
        func=franka_stack_events.randomize_object_pose,
        mode="reset",
        params={
            "pose_range": {"x": (0.4, 0.6),"y": (-0.10, 0.10),"z": (0.58, 0.58),"yaw": (-1.0, 1.0, 0)},
            "min_separation": 0.1,
            "asset_cfgs": [SceneEntityCfg("cube")],
        },
    )


@configclass
class FrankaCubeStackEnvCfg_SK(StackEnvCfg):

    def __post_init__(self):
        super().__post_init__()
        self.events =EventCfg_SK()
        self.scene.robot = 