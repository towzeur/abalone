import gymnasium as gym
import envs
import numpy as np


def test_render():
    env = gym.make("abalone-v2", render_mode="rgb_array")
    obs, info = env.reset()
    frame = env.render()
    print(f"Frame shape: {frame.shape}")
    # assert frame.shape == (130, 130, 3)
    assert isinstance(frame, np.ndarray)

    # Take a step
    mask = obs["action_mask"]
    action = np.random.choice(np.where(mask == 1)[0])
    obs, reward, terminated, truncated, info = env.step(action)
    frame = env.render()
    print(f"Frame shape after step: {frame.shape}")

    # wait for the user to close the window
    # display the frame using matplotlib
    import matplotlib.pyplot as plt

    plt.imshow(frame)
    plt.show()

    # env.close()
    print("Test passed!")


if __name__ == "__main__":
    test_render()
