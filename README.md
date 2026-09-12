![Spot RL Inference](media/handstand_real.gif)

---

# Spot RL Inference

Real-time deployment runtime for running reinforcement learning policies on the Boston Dynamics
Spot quadruped. It takes ONNX policies exported from
[spot_rl_train](https://github.com/SaxionMechatronics/spot_rl_train) and runs them on the real
robot through the Spot SDK.

The runtime streams robot state from Spot, builds the same observation vector used during
training, runs the policy, and streams joint position commands back to the robot.

## Installation

This project uses [Pixi](https://pixi.sh) to manage its environment. The Boston Dynamics SDK
wheels (v5.1.1) are included in `vendor/`.

1. Install Pixi by following the [installation guide](https://pixi.sh/latest/#installation).

2. Clone this repository:

   ```bash
   git clone git@github.com:SaxionMechatronics/spot_rl_inference.git && cd spot_rl_inference
   ```

3. Install the dependencies:

   ```bash
   pixi install
   ```

4. Convert the training config of the policy you want to deploy. Run the converter and, when
   prompted, enter the path to the `params/` directory of a
   [spot_rl_train](https://github.com/SaxionMechatronics/spot_rl_train) checkpoint (the one
   containing `env.yaml`). It writes an `env_cfg.json` next to `env.yaml`:

   ```bash
   pixi run python spot_rl_runtime/utils/env_convert.py
   # Enter the path to the env.yaml directory
   # /path/to/spot_rl_train/checkpoints/<run>/params
   ```

5. Copy the exported policy and the converted config into `models/`:

   ```bash
   cp /path/to/spot_rl_train/checkpoints/<run>/exported/policy.onnx models/policy.onnx
   cp /path/to/spot_rl_train/checkpoints/<run>/params/env_cfg.json models/env_cfg.json
   ```

## Usage

Before running, set your robot's credentials and IP address in [`pixi.toml`](pixi.toml):

```toml
[activation.env]
BOSDYN_CLIENT_USERNAME="user"
BOSDYN_CLIENT_PASSWORD="PutYourPasswordHere"

[tasks]
doyourthing = "python spot_rl_demo.py 192.168.50.3 --policy_file_path ./models -v"
```

Then start the control loop:

```bash
pixi run doyourthing
```

This connects to Spot, loads the policy from `./models`, and begins streaming commands.

## Contact

Kousheek Chakraborty - kousheekc@gmail.com

Project Link: https://github.com/SaxionMechatronics/spot_rl_inference

If you encounter any difficulties, feel free to reach out through the Issues section. If you find any bugs or have improvements to suggest, don't hesitate to make a pull request.

## Citation

If you use this work in your research, please cite:

```bibtex
@inproceedings{chakraborty2026actuator,
  author    = {Chakraborty, Kousheek and Rajendra, Chandan K. and Alharbat, Ayham and Mersha, Abeje Y.},
  title     = {Actuator Dynamics Curricula for Narrow-Viability Tasks in Legged Robot Learning},
  booktitle = {Conference on Robot Learning (CoRL)},
  year      = {2026},
}
```
