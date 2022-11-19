# AI_SETU

<img src="TempImage/readme.jpg" alt="效果图" style="zoom: 50%;" />

### **介绍**

利用[Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 的api 或是路路提供的友情api来实现**HoshinoBot**快速进行AI绘图。

额外提供快捷调用huggingface的某几个特定仓库和开源模型的方法

### 使用方法

- 来到HoshinoBot插件目录,输入以下命令克隆本仓库并安装依赖

  ```python
  git clone https://github.com/pcrbot/ai_setu.git
  cd ai_setu
  pip install -r requirements.txt
  ```

  > 若此处有报错信息，请务必解决，将错误信息复制到百度搜索一般即可找到解决办法。
  >
  > 若安装python依赖库时下载速度缓慢，可以尝试使用 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`
  >
- 在当前目录下重命名文件 `config_example.yaml`为 `config.yaml`

  或输入指令

  ```
  cp config_example.yaml config.yaml
  ```
- 编辑器打开 `config.yaml`并根据注释修改

  > 如果您不清楚某项设置的作用，请保持默认。
  >

    至此你已经成功部署本插件,期待您合法合理使用~

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
