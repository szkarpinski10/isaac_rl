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

#----------------------------------------------------------------------------------------------------------------------------------------------

from scene_sk import FrankaSceneCfg_SK 
def main():

    #Initialize the simulation context
    sim_cfg=SimulationCfg(dt=0.01)
    sim=SimulationContext(sim_cfg)

    #My scene
    scene_cfg = FrankaSceneCfg_SK(num_envs=9, env_spacing = 3.0)
    scene = InteractiveScene(scene_cfg)

    #Set main camera
    sim.set_camera_view([2.5,2.5,2.5],[0.0,0.0,0.0])

    #Play the simulator
    sim.reset()

    #INFO
    print("[INFO]: Setup complete")

    #Simulate physics
    while simulation_app.is_running():
        scene.write_data_to_sim()
        sim.step()
        scene.update(dt=sim.get_physics_dt())

if __name__== "__main__":
    #run the main function
    main()
    #close sim app
    simulation_app.close()