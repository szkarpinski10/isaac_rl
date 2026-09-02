import gymnasium as gym
from . import franka_SK
from . import rsl_rl_ppo_SK


gym.register(
    id = "Lift_SK",
    entry_point = "isaaclab.envs:ManagerBasedRLEnv",
    kwargs = {
        "env_cfg_entry_point": f"{__name__}.franka_SK:Franka_Env_Cfg",
        "rsl_rl_cfg_entry_point": f"{__name__}.rsl_rl_ppo_SK:PPO_runner_SK",
    },
    disable_env_checker = True,
)