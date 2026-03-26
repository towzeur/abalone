# Gymnasium contract:
# reset() -> (obs_dict, info)
# step(action_id) -> (obs_dict, reward, terminated, truncated, info)

# obs_dict keys:
# - "observation": np.int8 (3,61)
# - "action_mask": np.int8 (3721,)
