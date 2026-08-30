import isaaclab.sim as sim_utils
from isaaclab.utils.configclass import configclass
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.assets import ArticulationCfg, RigidObjectCfg, AssetBaseCfg
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from isaaclab.sensors import FrameTransformerCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg

from isaaclab_tasks.manager_based.manipulation.stack.stack_env_cfg import StackEnvCfg
from isaaclab_tasks.manager_based.manipulation.stack.mdp import franka_stack_events
from isaaclab_assets.robots.franka import FRANKA_PANDA_CFG
from isaaclab_tasks.manager_based.manipulation.stack import mdp
from isaaclab.envs.mdp import JointPositionActionCfg, BinaryJointPositionActionCfg
from isaaclab.markers.config import FRAME_MARKER_CFG
from isaaclab.managers import RewardTermCfg as RewTerm
import rewards_SK


_FRANKA_STACK_IK_REL_INIT_JOINT_POS: dict[str, float] = {
    "panda_joint1": 0.0444,
    "panda_joint2": -0.1894,
    "panda_joint3": -0.1107,
    "panda_joint4": -2.5148,
    "panda_joint5": 0.0044,
    "panda_joint6": 2.3775,
    "panda_joint7": 0.6952,
    "panda_finger_joint.*": 0.0400,
}


@configclass
class EventCfg:
    randomize_franka_joints_state = EventTerm(
        func=franka_stack_events.randomize_joint_by_gaussian_offset,
        mode = "reset",
        params = {
            "mean" : 0.0,
            "std" : 0.8,
            "asset_cfg": SceneEntityCfg("robot"),
        }
    )
    randomize_cube_postitions = EventTerm(
        func = franka_stack_events.randomize_object_pose,
        mode = "reset",
        params={
            "pose_range": {"x": (0.4, 0.6), "y": (-0.10, 0.10), "z": (0.6, 0.6), "yaw": (-1.0, 1, 0)},
            "min_separation": 0.1,
            "asset_cfgs": [SceneEntityCfg("cube_1"), SceneEntityCfg("cube_2"), SceneEntityCfg("cube_3")],
        },
    )


@configclass
class RewardsCfg:
    grasping_reward = RewTerm (func = rewards_SK.grasp_reward,params = {
            "robot_cfg": SceneEntityCfg("robot"),
            "ee_frame_cfg": SceneEntityCfg("ee_frame"),
            "object_cfg": SceneEntityCfg("cube_1"),
            "constant": 10.0,
            "object_grasped_reward": 5.0},weight = 1.0)

@configclass
class Franka_Env_Cfg(StackEnvCfg):

    def __post_init__(self):
        super().__post_init__()
        self.scene.num_envs = 4         
        self.scene.env_spacing = 3.0

        # utilities for gripper status check
        self.gripper_joint_names = ["panda_finger_.*"]
        self.gripper_open_val = 0.04
        self.gripper_threshold = 0.005

        self.events=EventCfg()
        self.rewards = RewardsCfg()

        self.scene.robot = FRANKA_PANDA_CFG.replace(
            prim_path = "{ENV_REGEX_NS}/Robot",
            init_state = ArticulationCfg.InitialStateCfg(
                pos = [0.0,0.0,0.55],
                joint_pos = _FRANKA_STACK_IK_REL_INIT_JOINT_POS),
        )

        self.scene.table = AssetBaseCfg(
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


        cube_properties = RigidBodyPropertiesCfg(
            solver_position_iteration_count=16,
            solver_velocity_iteration_count=1,
            max_angular_velocity=1000.0,
            max_linear_velocity=1000.0,
            max_depenetration_velocity=5.0,
            disable_gravity=False,
        )


        self.scene.cube_1 = RigidObjectCfg( 
            prim_path="{ENV_REGEX_NS}/Cube_1", 
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.45, 0.0, 1.08],         
            ),
            spawn=sim_utils.CuboidCfg(
                size=(0.05, 0.05, 0.05),
                rigid_props=sim_utils.RigidBodyPropertiesCfg(
                    disable_gravity=False,
                ),
                collision_props=sim_utils.CollisionPropertiesCfg(),
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(1.0, 0.0, 0.0),
                ),
                physics_material=sim_utils.RigidBodyMaterialCfg(
                    static_friction=0.5,
                    dynamic_friction=0.4,
                ),
            ),
        )


        self.scene.cube_2 = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Cube_2",  
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.50, 0.0, 1.08],         
            ),
            spawn=sim_utils.CuboidCfg(
                size=(0.05, 0.05, 0.05),
                rigid_props=sim_utils.RigidBodyPropertiesCfg(
                    disable_gravity=False,
                ),
                collision_props=sim_utils.CollisionPropertiesCfg(),
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(0.0, 1.0, 0.0),
                ),
                physics_material=sim_utils.RigidBodyMaterialCfg(
                    static_friction=0.5,
                    dynamic_friction=0.4,
                ),
            ),
        )

        self.scene.cube_3 = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Cube_3",  
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.55, 0.0, 1.08],         
            ),
            spawn=sim_utils.CuboidCfg(
                size=(0.05, 0.05, 0.05),
                rigid_props=sim_utils.RigidBodyPropertiesCfg(
                    disable_gravity=False,
                ),
                collision_props=sim_utils.CollisionPropertiesCfg(),
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(0.0, 0.0, 1.0),
                ),
                physics_material=sim_utils.RigidBodyMaterialCfg(
                    static_friction=0.5,
                    dynamic_friction=0.4,
                ),
            ),
        )

        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name = "robot",joint_names = ["panda_joint.*"], scale = 0.5, use_default_offset = True
        )

        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name = "robot",
            joint_names = ["panda_finger.*"],
            open_command_expr = {"panda_finger_.*" : 0.04},
            close_command_expr = {"panda_finger_.*": 0.0},
        )
        
        marker_cfg = FRAME_MARKER_CFG.copy()
        marker_cfg.markers["frame"].scale = (0.1, 0.1, 0.1)
        marker_cfg.prim_path = "/Visuals/FrameTransformer"
        self.scene.ee_frame = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot/panda_link0",
            debug_vis=False,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/panda_hand",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=[0.0, 0.0, 0.1034],
                    ),
                ),
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/panda_rightfinger",
                    name="tool_rightfinger",
                    offset=OffsetCfg(
                        pos=(0.0, 0.0, 0.046),
                    ),
                ),
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/panda_leftfinger",
                    name="tool_leftfinger",
                    offset=OffsetCfg(
                        pos=(0.0, 0.0, 0.046),
                    ),
                ),
            ],
        )




