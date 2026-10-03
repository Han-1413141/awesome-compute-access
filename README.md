# 算力普惠指南 · Awesome Compute Access

免费算力、低价 GPU、学生教育、科研资助、创业扶持、开源公益支持与国内算力券的中文申请资料库。

**本轮资料核对：2026-10-03 · 收录 103 个计划与平台条目**

可使用 39 · 需申请或候补 49 · 暂停申请 2 · 窗口结束或新用户关闭 5 · 待核实 8

[全部项目](docs/catalog.md) · [暂停与待核实](docs/archive.md) · [申请指南](docs/apply-guide.md) · [低价算力比较方法](docs/pricing-guide.md) · [已有仓库调研](docs/related-repositories.md) · [参与补充](CONTRIBUTING.md)

每项记录权益、资格、地区、申请材料、期限与限制、费用、状态和官方来源。免费 Notebook、云抵扣、模型 API、教学实验、工具订阅分别标注；最高资助额不等于人人可领。

本版已阅读官方资料并整理中文说明，未逐个平台注册、申请或运行任务。动态配额和无法确认的活动会明确标为待核实；不收共享账号、出售教育认证、滥用注册或返利推广链接。

## 按需求查找

| 你的情况 | 从这里开始 | 先看什么 |
|---|---|---|
| 想立即做小实验 | [免费计算](docs/categories/free-compute.md) | GPU是否保证、会话上限、文件保存 |
| 需要连续跑训练 | [低价GPU](docs/categories/low-cost.md) / [科研计划](docs/categories/research.md) | 显存、是否可抢占、存储与重跑成本 |
| 在校学生或任课教师 | [教育计划](docs/categories/education.md) | 是学生本人还是教师/学校申请 |
| 做学术研究 | [科研与超算](docs/categories/research.md) | 研究方向、机构所在地、成果开放要求 |
| 正在做创业项目 | [创业支持](docs/categories/startup.md) | 公司注册、融资、合作方、分档条件 |
| 维护开源或公益项目 | [开源支持](docs/categories/open-source.md) / [非营利](docs/categories/nonprofit.md) | 项目活跃度、组织资格、资源用途 |
| 中国大陆团队找补贴 | [国内政策](docs/categories/china-policy.md) | 城市、申请窗口、合同发票、补贴对象 |
| 只需调用模型 | [API额度](docs/categories/api.md) | 支持地区、模型限速、数据政策、有效期 |

## 分类目录

| 分类 | 全部条目 | 可使用或需申请 |
|---|---:|---:|
| [免费计算与云试用](docs/categories/free-compute.md) | 31 | 25 |
| [低价 GPU 与按量计算](docs/categories/low-cost.md) | 18 | 18 |
| [学生与教学计划](docs/categories/education.md) | 25 | 20 |
| [科研资助与超算分配](docs/categories/research.md) | 36 | 26 |
| [创业扶持与云额度](docs/categories/startup.md) | 25 | 19 |
| [开源项目支持](docs/categories/open-source.md) | 10 | 9 |
| [公益与非营利支持](docs/categories/nonprofit.md) | 2 | 2 |
| [国内算力券与地方政策](docs/categories/china-policy.md) | 6 | 1 |
| [模型 API 与推理额度](docs/categories/api.md) | 20 | 16 |

一个项目可有多个分类，上表不能相加得到总数。学生包等集合入口与单项优惠可能重合，权益金额也不能相加。需申请或候补不代表保证录取，也不代表当前有库存。

## 本轮确认的易错信息

- [SageMaker Studio Lab](docs/programs/sagemaker-studio-lab.md) 已关闭新用户入口，现有用户仍可使用。
- [Cerebras Inference](docs/programs/cerebras-api-trial.md) 当前为绑卡后5美元、30天试用，官方明确无自动续给的永久免费层。
- [DigitalOcean学生200美元](docs/programs/digitalocean-student-historical.md) 的旧入口跳转主页，本版不列为已确认可领取。
- [Modal Starter](docs/programs/modal-starter.md) 的30美元月额度是计算额度，不覆盖Shared Endpoints的token账单。
- [Google Cloud试用](docs/programs/google-cloud-free.md) 默认没有GPU配额；云代金券不是已分配GPU。
- [Hugging Face普通CPU Spaces](docs/programs/huggingface-spaces-cpu.md) 与 [ZeroGPU](docs/programs/huggingface-zerogpu.md) 的新建资格不同，需要分别查看。

## 数据与维护

- [JSON源数据](data/programs.json)：详情与目录的唯一来源。
- [CSV表格](data/programs.csv)：UTF-8 BOM，可下载到Excel筛选。
- [数据格式](data/schema.json)：字段、分类、状态及核实层级。
- [来源索引](docs/sources.md) · [核实方法与覆盖边界](docs/methodology.md) · [更新记录](CHANGELOG.md)。

修改源数据后运行 `python scripts/build.py`；提交前运行 `python scripts/build.py --check`。CI只检查数据与生成文档一致性，不会把链接可访问自动当成优惠有效，也不会自动改写核对日期。

欢迎补充遗漏项目，尤其是校内HPC、区域算力券、开源维护者和非营利算力支持。每次补充应包含能证明当前权益和资格的官方链接。

## 许可证

本仓库原创中文整理和代码采用 [MIT](LICENSE)。事实来自各计划官方页面，供应商名称、商标及原始条款仍归其权利人；申请与使用按供应商规则执行。已有项目及本次比较见[调研记录](docs/related-repositories.md)。
