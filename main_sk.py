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


#----------------------------------------------------------------------------------------------------------------------------------------------

import torch
from scene_sk import FrankaSceneCfg_SK
from isaaclab.envs import ManagerBasedRLEnv

# def main():

#     #Initialize the simulation context
#     sim_cfg=SimulationCfg(dt=0.01)
#     sim=SimulationContext(sim_cfg)

#     #My scene
#     scene_cfg = FrankaSceneCfg_SK(num_envs=9, env_spacing = 3.0)
#     scene = InteractiveScene(scene_cfg)

#     #events
#     env_cfg=FrankaSceneCfg_SK()

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
    # 1. Tworzymy konfigurację środowiska
    env_cfg = FrankaSceneCfg_SK()
    
    # 2. Inicjalizujemy pełne środowisko RL (ono samo zarządza sim, sceną, eventami itp.)
    env = ManagerBasedRLEnv(cfg=env_cfg)

    # 3. Ustawienie głównej kamery (dostęp do sim przez env.unwrapped)
    env.unwrapped.sim.set_camera_view([2.5, 2.5, 2.5], [0.0, 0.0, 0.0])

    # 4. Reset środowiska - TUTAJ ODPALA SIĘ LOSOWANIE KOSTKI Z events_sk.py!
    obs, _ = env.reset()

    # INFO
    print("[INFO]: Setup complete. Środowisko działa!")

    # 5. Pętla symulacji
    while simulation_app.is_running():
        with torch.inference_mode():
            # Na razie podajemy zerowe akcje (robot nic nie robi, tylko stoi w zdefiniowanej pozycji)
            actions = torch.zeros_like(env.action_manager.action)
            
            # Krok środowiska (zastępuje ręczne sim.step())
            obs, rewards, terminated, truncated, info = env.step(actions)


if __name__ == "__main__":
    main()
    simulation_app.close()