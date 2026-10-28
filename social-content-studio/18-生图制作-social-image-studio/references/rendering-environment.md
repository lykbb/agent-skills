# 渲染环境与脚本

全部资源从本 Skill 根目录解析；任务产物放对应项目。先检查现有 Node、Python、Playwright、浏览器及视频分支依赖，不自动安装。示例中的项目路径由实际项目替换；不要照搬不存在的上游历史测试目录。

## 静态图片

以下命令在当前图片工作台根目录执行；先根据本 SKILL.md 的实际位置进入该目录，不使用其他全局技能副本。

使用实际可用的 Node 执行，脚本自带依赖探测：先找本 Skill可解析的Playwright，再找 SOCIAL_IMAGE_PLAYWRIGHT，最后检查 Codex 已有的捆绑运行时。浏览器优先 SOCIAL_IMAGE_BROWSER 或已安装Chrome，再检查已存在的Chromium；没有可用项就报告缺失，不下载浏览器。

```bash
node scripts/render-social-card.mjs --html /项目目录/封面.html --selector '#cover' --output /项目目录/output/封面.png --width 1086 --height 1448
```

只检查和在内存中试渲染，不保存过程图：

```bash
node scripts/render-social-card.mjs --html /项目目录/封面.html --selector '#cover' --width 1086 --height 1448 --check-only
```

导出前审查：

```bash
node validate-social-deck.mjs /项目目录/封面.html
```

资源结构检查：

```bash
node scripts/check-skill-docs.mjs
```

脚本默认离线读取本地项目，不借用用户浏览器配置。需要网络资源时先确认来源、实际加载与授权，再用 --allow-network；离线时用可用本地字体或图标。导出拒绝覆盖现有输出；需要改稿另存新版本，清理旧版遵守用户确认规则。

## 复制资源

两套种子保留为原型，生成项目从其中复制或从本组认可源继续。截图纹理路径已调整为项目根的 assets/screenshot-backgrounds；使用哪张就复制哪张。Editorial引用 assets/magazine-bg-webgl.js 时同步复制或内联，确认背景绘制后再截图。模板中的 cover.jpg 等为占位素材，不是缺失的 Skill 文件，制作时必须替换或删去未使用的图片区。

字号与尺寸由系列决定，导出脚本只核对，不偷偷改变1086×1448为模板默认1080×1440。图标和字体未内置为完整字体包，不能称已嵌入Noto或Inter。WebGL保留软件渲染与原有2D回退，照片和截图保留真实内容。

## 实况专用

完整命令与依赖见 live-photo-production.md。保留抽帧联系表、JPG/MOV元数据、PVT、iPhone路径和降级分支。Python包装脚本需要已存在的 makelive；联系表需要ffmpeg/ffprobe；Swift辅助需要macOS相关工具链。文档中的uvx示例会下载工具，未获安装许可不得直接执行。

两个Swift元数据脚本与联系表脚本均拒绝已有输出。它们存在于本Skill，不意味着本机已配置或已验证所有视频能力；没有输入视频时不运行这些分支。
