# 独立生图工作台与模板路由

原内容 Skill 继续负责选题、材料与文案；独立 social-image-studio 已实际包含完整模板、背景、参考、制作脚本和审查机制。用户选定此类版式后自动读取本文件，无需用户再切换或重复调用另一个 Skill。

## 单一来源与读取方式

- 模板库实体：`../../social-image-studio`。
- 先读取其 [SKILL.md](../../18-生图制作-social-image-studio/SKILL.md)，再按当前页面需要读取参考，不一次加载整个参考库；同一任务已读过的内容无需每轮重复读取。
- 生图资源完整保存在独立工作台，不再依赖原 Guizang 目录。下表路径均相对于模板库根目录解析，不能相对于本文件解析。
- 若主文件或某项资源缺失，先核对当前总包的实体文件；不可用时说明具体缺项，不改去依赖其他全局副本，也不自动安装、下载字体或声称已调用缺失模板。

## 能力入口

| 当前需要 | 读取模板库中的文件 |
|---|---|
| 从文案组织页序与信息量 | `references/content-planning.md`；按类别需要再读 `references/category-cookbook.md` |
| 选择完整版式 | `references/layout-recipes.md`，含 M01–M16 与 S01–S12 共 28 种配方 |
| 选风格、配色、字体和组件 | `references/style-system.md`、`references/theme-presets.md`、`references/components.md` |
| 安排竖版空间 | `references/portrait-fill.md` |
| 瑞士风排版起点 | `assets/template-swiss-card.html` |
| 杂志风排版起点 | `assets/template-editorial-card.html`，需要背景层时配套 `references/background-systems.md` |
| 使用真实截图 | `references/screenshot-treatment.md` |
| 照片叠字与人物避让 | `references/image-overlay.md` |
| 地图与位置关系 | `references/map-component.md` |
| 跨平台尺寸、公众号封面 | `references/platform-specs.md`、`references/title-shortener.md` |
| 制作和导出 PNG | `references/production-workflow.md` |
| 基本检查 | `references/qa-checklist.md` |
| 用户要求完整自动检查 | `validate-social-deck.mjs` |
| 明确要实况照片或视频拼图 | `references/live-photo-production.md` 及其中调用的脚本 |

杂志风包含封面、照片手记、分栏文章、引语、清单、证据墙、长条目、边注、章节分隔、问题页、流程与前后对比等版式；瑞士风包含强调色封面、对比、界面卡、警示行、架构、要点账本、图片主视觉、数值图及矩阵等版式。按页面职责选择，不因模板存在就给内容加上不存在的数据或流程。

## 本用户的优先规则

1. 已确认的题材、文案、总张数、当前页和风格优先。模板的默认 5–9 页不覆盖用户给定张数；已有风格时不反复重选。需要比较时只给少量有明显差别的方向，先试一张。
2. 模板只负责表达，不重新发明主线。目录与组件清单可以借用矩阵或条目视觉，但没有执行顺序时不加流程箭头；数字图必须有真实数量依据。
3. 所有生成物放当前项目目录，不使用模板库中的 `local-tests/` 作为本用户的默认产出目录。沿用已选定的画布和命名；本组 1086×1448 不被种子默认值覆盖。
4. 用户明确要求静态图时交付 PNG。文字卡片编辑 HTML/CSS；需要新插画或位图改图时保留 imagegen 分支。真实截图不重绘后冒充原图。
5. 基本文字、边界、尺寸和目检正常完成。按独立工作台执行完整的适用审查与HTML校验，不在每一页重复询问检查方式；不为密度提示编造角标、日期、来源或装饰。
6. 模板示例不构成素材使用授权。图片来源、署名、费用、外部上传和发布仍按当前用户授权与实际来源处理，不将下载成功等同于可任意使用。
7. 风格规则是默认设计方法。用户要求更粗字体、更明确分区或指定标题时，在当前授权范围内优先满足，不拿模板默认值否定已确认要求。

## 复制与导出时保留依赖

- 新任务从对应种子复制到项目，保留其组件和主题结构；已有同组可编辑源文件时优先复用最新认可版本。只复制本页实际需要的资源。
- 检查 HTML、CSS 和脚本的相对路径。种子中的截图纹理引用使用 `assets/screenshot-backgrounds/`；复制到项目后按实际目录核对，并将用到的纹理复制到项目的 `assets/`。
- Editorial 若调用 `assets/magazine-bg-webgl.js`，同时复制或内联该背景资源；不留下缺失脚本。Swiss 不借用另一套字体和背景。
- 种子含远程字体和图标资源。网络受限时，优先使用已安装字体和可用本地图标，去掉不再使用的远程请求，核对实际字形和换行；不擅自安装字体。
- 使用现有可用浏览器导出目标画布节点；Playwright、浏览器或运行时缺失时先检查已配置的工作区依赖，不假定模板库自带渲染环境。使用包内 `scripts/render-social-card.mjs` 导出，并先核对真实运行依赖；脚本存在不等于渲染已经跑通。
- 静态图不引入实况照片所需的 ffmpeg、makelive 等依赖。只在用户明确要该类型时读取对应制作分支。
- 导出前检查布局，微调尽量在内存或当前页面内完成；最终保留可编辑源和实际交付 PNG，不为每次试算新建一批过程报告或重复文件。
