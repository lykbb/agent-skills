# Social Content Studio

中文社交内容 Skill 工作台，包含 1 个总入口、5 个文体入口和 9 个共用能力，共 15 个 Skill。支持长文、小红书静态图文、短帖、教程和资讯调研。

## 公开版已脱敏

本目录为独立发布副本：已移除私人保存目录、Notion 页面与数据库标识、用户项目图片和个案版本记录。通用方法、必要脚本、上游背景纹理、来源署名和许可证保留。

公开版不附私人原稿、参考截图和已认可视觉基准。没有实际图片时不能声称已查看；参考图由使用者另行提供。文本配置不等于已经连接 Notion，也不代表完整内容产线或真实生图已通过验证。

## 使用

将整个 `social-content-studio/` 目录交给支持 Agent Skills 的客户端，先读取 [SKILL.md](SKILL.md)。保留内部目录结构，不能只复制总入口。用法与维护入口见 [项目说明](项目说明.md)。

五个入口：

| 场景 | 入口 |
| --- | --- |
| 深度观点长文 | [long-article](01-长文-long-article/SKILL.md) |
| 小红书静态图文 | [xiaohongshu-post](02-图文-xiaohongshu-post/SKILL.md) |
| 短帖与推文串 | [short-posts](03-短帖-short-posts/SKILL.md) |
| 教程 | [tutorial-article](04-教程-tutorial/SKILL.md) |
| 资讯调研 | [news-research-brief](05-资讯调研-news-brief/SKILL.md) |

共用能力包括转写整理、选题大纲、研究核验、正文写作、图文分页、标题、配图规划、生图和发布复核。正文自然表达与内容保护由 [writing-skill](14-正文写作-writing-skill/SKILL.md) 负责。

## 使用者本地配置

- 正文、视觉素材和可编辑源的保存位置由使用者指定，不创建原作者的目录。
- 使用 Notion 时，先在本地配置选题库、数据库、维护清单和成稿归档位置，见 [选题库适配](references/notion-topic-library.md)。不要把真实配置提交到仓库。
- 联网研究、生图、独立审阅、Notion 与浏览器等能力由当前客户端提供；缺失时按相应 Skill 说明限制，不静默安装或虚构执行结果。
- 结构图需要当前环境具备 `diagram-design` 或按使用者授权提供的对应能力；正文、图片和发布分别验收，不将文件检查当作全链路验证。

## 检查

在本目录运行：

```bash
python3 scripts/check-package.py
node 18-生图制作-social-image-studio/scripts/check-skill-docs.mjs
```

以上检查包结构、文件与引用，不联网、不调用模型、不执行公开发布。

## 来源与许可证

各模块沿用各自的许可证和来源说明，不给整个集合擅自添加统一许可。正文写作模块保留其 MIT 许可证；生图模块基于公开的 Guizang Social Card Skill 适配，保留其 AGPL-3.0-only 许可证、原作者署名和商业授权说明，详见 [来源说明](18-生图制作-social-image-studio/references/upstream-source.md)。公开文章链接只用于来源定位，不表示转载其图片或整篇正文。
