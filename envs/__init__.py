from gymnasium.envs.registration import register

register(
    id="abalone-v2",
    entry_point="envs.abalone_env:AbaloneGymEnv",
    max_episode_steps=200,
)
