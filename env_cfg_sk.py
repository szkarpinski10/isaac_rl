from isaaclab.assets import RigidObjectCfg
from isaaclab.sensors import FrameTransformerCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
from isaaclab.utils.configclass import configclass

from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab.utils.configclass import configclass

from scene import FrankaSceneCfg_SK
from events import EventCfg

@configclass
class ActionsCfg:
    pass

@configclass
class ObservationsCfg:
    @configclass
    class PolicyCfg:
        pass
    policy: PolicyCfg = PolicyCfg()

@configclass
class RewardsCfg:
    pass

@configclass
class TerminationsCfg:
    pass

@configclass
class FrankaStackEnvCfg_SK(ManagerBasedRLEnvCfg):
    

    scene: FrankaSceneCfg_SK = FrankaSceneCfg_SK(num_envs=9, env_spacing=3.0)
    events: EventCfg = EventCfg()

   
    actions: ActionsCfg = ActionsCfg()
    observations: ObservationsCfg = ObservationsCfg()
    rewards: RewardsCfg = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()

    def __post_init__(self):
        super().__post_init__()
        self.decimation = 2
        self.episode_length_s = 5.0
        self.sim.dt = 0.01
        self.sim.render_interval = self.decimation