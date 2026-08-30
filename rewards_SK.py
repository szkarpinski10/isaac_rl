import torch
from isaaclab.managers import SceneEntityCfg
from isaaclab.envs import ManagerBasedRLEnv
import observations

def grasp_reward (env: ManagerBasedRLEnv, robot_cfg: SceneEntityCfg, ee_frame_cfg: SceneEntityCfg, object_cfg: SceneEntityCfg, constant: float,object_grasped_reward: float
                    )-> torch.Tensor:

    
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]
    object: RigidObject = env.scene[object_cfg.name]

    object_pos = object.data.root_pos_w.torch
    end_effector_pos = ee_frame.data.target_pos_w.torch[:, 0, :]
    distance_ee_to_obj = torch.linalg.vector_norm(object_pos - end_effector_pos, dim=1)
    
    reward_reach = torch.exp(-distance_ee_to_obj*constant)
    check_if_grasped = object_grasped(env,robot_cfg,ee_frame_cfg,object_cfg)


    reward_grasped = torch.where(check_if_grasped,object_grasped_reward, 0.0)
    
    total_reward = reward_reach + reward_grasped

    return total_reward
