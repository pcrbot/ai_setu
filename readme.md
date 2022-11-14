# AI_SETU

![效果图](TempImage/readme.jpg)

### **介绍**

利用[Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 的api 或是路路提供的友情api来实现**HoshinoBot**快速进行AI绘图。

额外提供快捷调用huggingface的某几个特定仓库和开源模型的方法

### 使用方法

- 装额外依赖 `hjson`,`pyahocorasick`,`pyyaml`,`aiofiles`

  ```
  pip install XXX
  ```
- 命令行输入

  ```
  cp config_example.yaml config.yaml
  ```

  然后根据注释提示自行修改 `config.yaml`

### 功能

* **(SD)绘图**
* **(SD)以图绘图**
* **个人/本群XP排行/缝合**
* **上传pic**
* **查看本群/个人/全部pic**
* **点赞/删除pic**
* **超分pic x倍超分 [保守/不]降噪   X为2，3，4   []内为可选参数**
* **鉴赏图片**
* **动漫化**
* **(SD)元素法典吟唱**
* **(SD)今天我是什么少女**

前缀含有**SD**则使用[Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 的api

无前缀默认使用路路提供的友情api


**PS:渣代码,欢迎提出改进建议~**
