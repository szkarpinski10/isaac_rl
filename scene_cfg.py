import isaaclab.sim as sim_utils
from isaaclab.scene import InteractiveSceneCfg, InteractiveScene
from isaaclab.assets import ArticulationCfg, AssetBaseCfg, RigidObjectCfg
from isaaclab.sim import SimulationContext
from isaaclab.utils import configclass
from isaaclab_assets import FRANKA_PANDA_CFG, FRANKA_TABLE_CFG
from isaaclab.env import DirectRLEnv, DirectRLEnvCfg 

@configclass
class MyScene(InteractiveSceneCfg):
    
    ground = AssetBaseCfg(prim_path="/World/defaultGroundPlane",
                          spawn=sim_utils.GroundPlaneCfg())

    dome_light= AssetBaseCfg(prim_path="/World/Light",
                             spawn=sim_utils.DomeLightCfg(intensity=3000.0, color=(0.75,0.75,0.75)))

    table = FRANKA_TABLE_CFG.replace(prim_path="{ENV_REGEX_NS}/table")
    robot= FRANKA_PANDA_CFG.replace(prim_path="{ENV_REGEX_NS}/robot")
    cube = RigidObjectCfg(prim_path="{ENV_REGEX_NS}/Cube",spawn=sim_utils.CuboidCfg(
                        size=(0.04, 0.04, 0.04),
                        rigid_props=sim_utils.RigidBodyPropertiesCfg(),
                        mass_props=sim_utils.MassPropertiesCfg(mass=0.1),
                        collision_props=sim_utils.CollisionPropertiesCfg(),  
                        visual_material=sim_utils.PreviewSurfaceCfg(
                        diffuse_color=(1.0, 0.0, 0.0)),
                        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.5, 0.0, 0.05)
        ),
    )

@configclass
class MyEnvCfg(DirectRLEnvCfg):
    scene:MyScene=MyScene(num_envs=32,env_spacing=2.5)
    decimation=2
    episode_length_s=5.0
    num_actions=7
    num_observations=14