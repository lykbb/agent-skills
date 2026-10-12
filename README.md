# Agent Skills

个人 Skill 合集：一个仓库，按用途分类。每套 Skill 保留独立文件夹、`SKILL.md` 和所需资源，不为每套 Skill 单独新建仓库。

## 已收录

| 分类 | Skill | 用途与标签 |
| --- | --- | --- |
| 知识库 | [得到大脑与临时视频转写](skills/knowledge/getnote-browser/SKILL.md) | 浏览器读写、博主订阅、精选文章分类；不入库的云端临时转写 |

当前收录 1 套 Skill；其余类别仅为分类约定，添加实际内容时才创建目录。

## 分类约定

| 目录 | 内容类型 |
| --- | --- |
| `skills/image/` | 生图、图片编辑、视觉风格 |
| `skills/writing/` | 选题、写文章、改稿 |
| `skills/knowledge/` | 知识库、资料收集、笔记管理 |
| `skills/tools/` | 教 AI 操作浏览器、软件、CLI 等工具 |
| `skills/video/` | 视频制作、剪辑、字幕和转写 |

多用途 Skill 选择一个主要类别，在索引中补充标签；不复制到多个目录。得到大脑虽然也涉及工具操作和视频转写，仍只保留在 `knowledge` 类。多套 Skill 可以配合使用，但不必再写一套“怎么使用 Skill 的 Skill”。

## 使用与维护

1. 从索引选择 Skill，读取完整 `SKILL.md`，再按其中指引读取所需参考文件。
2. 按所用 AI 客户端的安装规则，提供完整的叶子目录，例如 `skills/knowledge/getnote-browser/`；不要只复制入口文件。仓库分类不等于所有客户端会自动发现、安装或启用全部 Skill。
3. 本仓库为私有仓库，云端 Agent 需要已有且获准的仓库访问权限；不要把登录凭据、Cookie 或令牌粘进 Skill、笔记或对话。
4. 更新时保留相对引用，核对上传范围；不收录账号配置、知识库正文、浏览器数据或临时媒体。此仓库不自动修改本机全局 Skill，也不自动配置其他 Agent。

Skill 格式与相关 Skill 的组合方式参见 [OpenAI 官方文档](https://developers.openai.com/plugins/build/skills)。这里的分类名称是本仓库的组织约定，不是客户端固定目录要求。
