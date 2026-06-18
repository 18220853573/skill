# ClinicalTrials.gov CSV 字段映射表

本文件记录 ClinicalTrials.gov 导出 CSV 的列名与模板字段的对应关系。

## 标准字段映射

| CSV 列名 | 模板章节 | 模板字段 |
|----------|----------|----------|
| NCT Number | §1 研究基本信息 | NCT 编号 |
| Title | §1 研究基本信息 | 研究标题（Brief Title） |
| Official Title | §1 研究基本信息 | 官方标题（Official Title） |
| Acronym | §1 研究基本信息 | 研究简称（Title Acronym） |
| Sponsor | §1 研究基本信息 | 申办方（Sponsor） |
| Responsible Party | §1 研究基本信息 | 负责方（Responsible Party） |
| Collaborators | §1 研究基本信息 | 协作方（Collaborator） |
| Study Type | §1 研究基本信息 | 研究类型（Study Type） |
| Phases | §1 研究基本信息 | 研究阶段（Phase） |
| Status | §1 研究基本信息 | 研究状态（Status） |
| Brief Summary | §1 研究基本信息 | 简要摘要（Brief Summary） |
| Conditions | §2 研究疾病与干预措施 | 疾病/状况（Condition/Disease） |
| Interventions | §2 研究疾病与干预措施 | 干预名称（Intervention/Treatment） |
| Other IDs | §2 研究疾病与干预措施 | 其他研究 ID |
| Primary Purpose | §3 研究设计 | 主要目的（Primary Purpose） |
| Allocation | §3 研究设计 | 分配方式（Allocation） |
| Intervention Model | §3 研究设计 | 干预模型（Intervention Model） |
| Masking | §3 研究设计 | 设盲情况（Masking） |
| Enrollment | §1/备注 | 入组人数（可记入备注或标题） |
| Healthy Volunteers | §5 入组标准 | 接受健康志愿者 |
| Minimum Age | §5 入组标准 | 最低年龄 |
| Maximum Age | §5 入组标准 | 最高年龄 |
| Sex | §5 入组标准 | 接受的性别 |
| Eligibility Criteria | §5 入组标准 | 纳入/排除标准（需拆分） |
| Primary Outcome Measures | §6.1 主要结局指标 | 指标名称 |
| Secondary Outcome Measures | §6.2 次要结局指标 | 指标名称 |
| Other Outcome Measures | §6.3 其他结局指标 | 指标名称 |
| Start Date | §7 时间节点 | 研究开始日期 |
| Primary Completion Date | §7 时间节点 | 主要完成日期 |
| Completion Date | §7 时间节点 | 研究完成日期 |
| First Posted | §7 时间节点 | 首次通过QC并发布 |
| Last Update Posted | §7 时间节点 | 最后更新提交通过QC |
| Locations | §8 研究地点与联系人 | 研究实施国家/地区 |
| Study Documents | §12 结果相关信息 | 参考文档 |
| URL | 备注 | 原始链接 |
| Results First Posted | §12 结果相关信息 | 结果首次发布日期 |
| Was There an Expanded Access Record? | §11 扩展性使用 | 扩展性使用状态 |
| Has Results | §12 结果相关信息 | 是否有结果 |
| Keywords | §13 关键词与术语 | 研究者提供的关键词 |
| MeSH Terms | §13 关键词与术语 | MeSH 相关术语 |

## 字段值翻译对照

### Study Type
| 英文 | 中文标注 |
|------|----------|
| Interventional | ☑ Interventional |
| Observational | ☑ Observational |

### Phase
| 英文 | 标注 |
|------|------|
| Phase 1 | ☑ Phase 1 |
| Phase 2 | ☑ Phase 2 |
| Phase 3 | ☑ Phase 3 |
| Phase 4 | ☑ Phase 4 |
| Early Phase 1 | ☑ Early Phase 1 |
| N/A / Not Applicable | ☑ Not Applicable |

### Status
| 英文 | 中文说明 |
|------|----------|
| Not yet recruiting | 尚未招募 |
| Recruiting | 招募中 |
| Active, not recruiting | 进行中，已停止招募 |
| Completed | 已完成 |
| Enrolling by invitation | 邀请招募 |
| Suspended | 暂停 |
| Terminated | 终止 |
| Withdrawn | 撤回 |
| Unknown status | 状态未知 |

### Allocation
| 英文 | 标注 |
|------|------|
| Randomized | ☑ Randomized |
| Non-Randomized | ☑ Non-randomized |
| N/A | ☑ Not applicable |

### Masking
| 英文 | 标注 |
|------|------|
| None (Open Label) | ☑ No masking |
| Single | ☑ Single blind |
| Double | ☑ Double blind |
| Triple | ☑ Triple |
| Quadruple | ☑ Quadruple |

### Intervention Type（从 Interventions 列提取前缀）
| 英文前缀 | 标注 |
|----------|------|
| DRUG: | ☑ Drug |
| DEVICE: | ☑ Device |
| BIOLOGICAL: | ☑ Biological |
| BEHAVIORAL: | ☑ Behavioral |
| DIETARY_SUPPLEMENT: | ☑ Dietary Supplement |
| OTHER: | ☑ Other |

## 注意事项

1. **Eligibility Criteria 字段**：CSV 中通常合并了纳入和排除标准，需识别 "Inclusion Criteria:" 和 "Exclusion Criteria:" 标题后拆分。
2. **Interventions 字段**：格式通常为 `DRUG: 药物名 (描述)|DRUG: 另一药物`，需按 `|` 分割并去除前缀类型标签。
3. **Outcome Measures 字段**：格式通常为 `指标名 [时间框架]|指标名2 [时间框架2]`，需按 `|` 分割后逐行填入表格。
4. **Locations 字段**：包含具体地点信息，提取国家列表用于 §8。