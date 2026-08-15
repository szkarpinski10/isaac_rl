import argparse
from isaaclab.app import AppLauncher

# create argparser
parser = argparse.ArgumentParser(description="Test programu")

#append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)

#parse the arguments
args_cli=parser.parse_args()

#launch app
app_launcher=AppLauncher(args_cli)
simulation_app=app_launcher.app


#import modules

from isaaclab.sim import SimulationCfg, SimulationContext
from isaaclab.scene import InteractiveScene
from isaaclab.managers import EventManager
#----------------------------------------------------------------------------------------------------------------------------------------------

from scene_sk import FrankaSceneCfg_SK, Event_rand_SK


import torch
from isaaclab.envs import ManagerBasedRLEnv
from scene_sk import FrankaEnvCfg_SK
# def main():

#     #Initialize the simulation context
#     sim_cfg=SimulationCfg(dt=0.01)
#     sim=SimulationContext(sim_cfg)

#     #My scene
#     scene_cfg = FrankaSceneCfg_SK(num_envs=9, env_spacing = 3.0)
#     scene = InteractiveScene(scene_cfg)

#     #events
#     events= Event_rand_SK()

#     #Set main camera
#     sim.set_camera_view([2.5,2.5,2.5],[0.0,0.0,0.0])

#     #Play the simulator
#     sim.reset()



#     #INFO
#     print("[INFO]: Setup complete")

#     #Simulate physics
#     while simulation_app.is_running():
#         scene.write_data_to_sim()
#         sim.step()
#         scene.update(dt=sim.get_physics_dt())

# if __name__== "__main__":
#     #run the main function
#     main()
#     #close sim app
#     simulation_app.close()

def main():
    # Inicjalizacja środowiska z gotowej konfiguracji
    env_cfg = FrankaEnvCfg_SK()
    env = ManagerBasedRLEnv(cfg=env_cfg)

    # Uruchomienie resetu - odpala automatycznie zdarzenia (Events) z trybem mode="reset"
    obs, _ = env.reset()

    print("[INFO]: Setup complete")

    # Główna pętla symulacji
    while simulation_app.is_running():
        # Losowe akcje testowe
        actions = torch.zeros_like(env.action_manager.action)
        obs, rewards, terminated, truncated, info = env.step(actions)


if __name__ == "__main__":
    main()
    simulation_app.close()