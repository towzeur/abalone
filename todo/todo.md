# Abalone Project Status & Tasks

## Status
- [x] **Engine V1 (Legacy)** analyzed.
- [x] **Engine V2 (High Perf)** core implemented and verified.
  - [x] Parity with V1 on `get_legal_actions` for classical start (44 moves).
  - [x] Efficient 1D board representation (61 nodes).
  - [x] Native Python core (Minimizing NumPy dependency for logic).
- [x] **Adapters**
  - [x] `obs_codec.py`: (3, 61) planes + action mask.
  - [x] `action_codec.py`: (pos0, pos1) encoding.
  - [x] `AbaloneGymEnv`: Gymnasium compatible wrapper.
- [ ] **PettingZoo Adapter**
  - [ ] Implement `AbalonePettingZooEnv` (AEC format).

## Todo
1. **Optimization**
   - Precompute neighbors and Sumito paths in `EngineV2` for speed.
   - Refactor `apply` to be more surgical (avoid coordinate lookups).
2. **Testing**
   - Add random-walk parity tests between V1 and V2.
   - Test Ejection/Game Over logic in V2.
3. **Training Ready**
   - Verify `AbaloneGymEnv` works with `MaskablePPO`.
