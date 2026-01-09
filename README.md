# 🤖 RoboParty 机械臂运行指南
超详细的机械臂启动&推理教程，跟着做就对啦✨

## 📌 前置说明
所有命令请根据自己的服务器/本地路径调整，遇到 `[sudo] 密码` 提示时输入对应密码即可～

---

## 0️⃣ 第一步：登录公司服务器，启动机械臂服务端
先搞定硬件端，机械臂才能乖乖听话哦🤏

### 🔍 查看CAN口
```bash
bash /home/shiyanyan/RoboParty_pi_infer/control_your_robot/piper_sdk/piper_sdk/find_all_can_port.sh
```

### ⚡ 激活机械臂
分别激活两个CAN口，缺一不可～
```bash
# 激活can0
bash /home/shiyanyan/RoboParty_pi_infer/control_your_robot/piper_sdk/piper_sdk/can_activate.sh can0 1000000 "3-6.4:1.0"

# 激活can1
bash /home/shiyanyan/RoboParty_pi_infer/control_your_robot/piper_sdk/piper_sdk/can_activate.sh can1 1000000 "3-6.3:1.0"
```

### 📍 机械臂归零
让机械臂回到初始位置～
```bash
python /home/shiyanyan/RoboParty_pi_infer/control_your_robot/piper_sdk/piper_sdk/demo/V2/piper_ctrl_go_zero.py
```

### 🎨 机械臂画圆（原文小修正）
```bash
# 这里替换成画圆的正确脚本哦～如果和归零脚本一样，可备注：“画圆脚本待补充”
python /home/shiyanyan/RoboParty_pi_infer/control_your_robot/piper_sdk/piper_sdk/demo/V2/piper_ctrl_draw_circle.py
```

### 📷 查看/修改相机参数
```bash
python /home/shiyanyan/RoboParty_pi_infer/control_your_robot/my_robot/agilex_piper_dual_base.py
```

---

## 1️⃣ 第二步：登录服务器，启动推理服务端
连接远程服务器，启动模型服务🚀

### 🔌 登录服务器 & 激活环境
```bash
# 登录服务器
ssh syy@h20.roboparty.com -p 51821

# 进入项目目录
cd openpi

# 激活虚拟环境
source ./.venv/bin/activate
```

### 🚀 启动服务（选对应版本即可）
```bash
# pi05_ygx（路径2）
CUDA_VISIBLE_DEVICES=2 uv run scripts/serve_policy.py --port 8005 policy:checkpoint \
  --policy.config pi05_ygx \
  --policy.dir /data0/syy_data/RoboParty_pi_train/openpi/checkpoints/pi05_ygx/piper_ygx/20000
```

---

## 2️⃣ 第三步：本地端口映射（解决端口占用）
单独开一个终端操作，Ubuntu/Windows 版本都给你备好啦💻

### 🐧 Ubuntu 版本
```bash
# 1. 查看8005端口被哪个进程占用（输出数字就是PID）
robo@RoboParty:~/RoboParty_pi$ sudo lsof -t -i:8005

# 2. 杀掉占用进程（把2710021换成上面查到的PID）
robo@RoboParty:~/RoboParty_pi$ sudo kill 2710021

# 3. 建立端口映射（后台运行，不用管）
robo@RoboParty:~/RoboParty_pi$ ssh -L 8005:127.0.0.1:8005 syy@h20.roboparty.com -p 51821 -Nf

# 4. 验证映射是否成功（能看到ssh占用8005端口就对了）
robo@RoboParty:~/RoboParty_pi$ ss -tulpn | grep ":8005"
```

---

## 3️⃣ 第四步：启动Pi0.5客户端（Ubuntu电脑）
终于到最后一步啦！先激活conda环境，再选对应模式运行～

### 📝 第一步：激活conda环境
```bash
conda activate infer
```

### 🧪 模式1：只输出Action，不执行（测试用）
```bash
python control_your_robot/example/deploy/piper_deploy_pi05_ygx.py \
  --remote-ws 127.0.0.1:8005 \
  --dry-run \
  --auto-start \
  --task "There are three blocks on the table, the color of the blocks is red, green and blue. Stack blue on green, green on red."
```

### 🚗 模式2：执行Action（实际控制机械臂）
```bash
# 基础执行版（max-step=100 表示最多执行100步，改成0则无限执行）
python control_your_robot/example/deploy/piper_deploy_pi05_ygx.py \
  --remote-ws 127.0.0.1:8005 \
  --max-step 100 \   # 🔔 改成0是一直输出
  --max-queue-size 50 \  # 最大存储队列动作
  --task "There are three blocks on the table, the color of the blocks is red, green and blue. Stack blue on green, green on red."
```

### 🚀 特殊版：RTC推理（重点！！！）
```bash
# RTC测试模式（只输出不执行）
python control_your_robot/example/deploy/piper_deploy_pi05_ygx.py \
  --remote-ws 127.0.0.1:8005 \
  --dry-run \
  --auto-start \
  --task "There are three blocks on the table, the color of the blocks is red, green and blue. Stack blue on green, green on red."
```
