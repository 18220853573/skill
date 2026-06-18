#!/usr/bin/env python3
"""
parse_trial_csv.py — ClinicalTrials.gov CSV 解析器
将下载的 CSV 文件转换为结构化 JSON，供后续模板填充使用

用法：
    python parse_trial_csv.py <csv_file_path> [--index N]

参数：
    csv_file_path   ClinicalTrials.gov 导出的 CSV 文件路径
    --index N       仅处理第 N 条记录（0起始），默认输出所有记录

输出：
    标准输出 JSON 格式的解析结果
"""

import csv
import json
import sys
import argparse
import re
from pathlib import Path


def split_pipe(value: str) -> list[str]:
    """按竖线分隔字段值，并去除首尾空白。"""
    if not value or value.strip() == '':
        return []
    return [v.strip() for v in value.split('|') if v.strip()]


def parse_intervention(raw: str) -> dict:
    """
    解析 Interventions 字段。
    格式: "DRUG: 药物名 (描述)" 或 "DRUG: 名称"
    返回: {type: str, name: str, description: str}
    """
    type_prefix_map = {
        'DRUG': 'Drug',
        'DEVICE': 'Device',
        'BIOLOGICAL': 'Biological',
        'BEHAVIORAL': 'Behavioral',
        'DIETARY_SUPPLEMENT': 'Dietary Supplement',
        'OTHER': 'Other',
        'PROCEDURE': 'Procedure',
        'RADIATION': 'Radiation',
        'COMBINATION_PRODUCT': 'Combination Product',
        'DIAGNOSTIC_TEST': 'Diagnostic Test',
        'GENETIC': 'Genetic',
    }
    result = {'type': 'Other', 'name': raw, 'description': ''}
    for prefix, label in type_prefix_map.items():
        if raw.upper().startswith(prefix + ':'):
            result['type'] = label
            rest = raw[len(prefix) + 1:].strip()
            # 提取括号内的描述
            paren_match = re.search(r'\((.+?)\)$', rest)
            if paren_match:
                result['description'] = paren_match.group(1).strip()
                result['name'] = rest[:paren_match.start()].strip()
            else:
                result['name'] = rest
            break
    return result


def parse_outcome(raw: str) -> dict:
    """
    解析结局指标字段。
    格式: "指标名 [时间框架]"
    返回: {name: str, timeframe: str}
    """
    bracket_match = re.search(r'\[(.+?)\]', raw)
    if bracket_match:
        timeframe = bracket_match.group(1).strip()
        name = raw[:bracket_match.start()].strip()
    else:
        name = raw.strip()
        timeframe = ''
    return {'name': name, 'timeframe': timeframe, 'description': ''}


def parse_eligibility(raw: str) -> dict:
    """
    拆分纳入/排除标准。
    """
    inclusion = []
    exclusion = []

    # 尝试按标准标题分割
    inc_match = re.search(r'Inclusion Criteria\s*:(.+?)(?=Exclusion Criteria\s*:|$)',
                          raw, re.IGNORECASE | re.DOTALL)
    exc_match = re.search(r'Exclusion Criteria\s*:(.+?)$',
                          raw, re.IGNORECASE | re.DOTALL)

    def extract_items(text: str) -> list[str]:
        text = text.strip()
        # 尝试按数字编号或星号拆分
        items = re.split(r'\n\s*[\d\*\-•]+[\.\)]\s*|\n\s*-\s+', text)
        result = []
        for item in items:
            item = item.strip().replace('\n', ' ')
            if item and len(item) > 2:
                result.append(item)
        return result

    if inc_match:
        inclusion = extract_items(inc_match.group(1))
    if exc_match:
        exclusion = extract_items(exc_match.group(1))

    # 若未识别到标准标题，保留原文
    if not inclusion and not exclusion and raw.strip():
        inclusion = [raw.strip()]

    return {'inclusion': inclusion, 'exclusion': exclusion}


def parse_row(row: dict) -> dict:
    """将 CSV 的一行解析为结构化字典。"""

    # 字段别名（处理 CSV 列名变体）
    def get(row, *keys):
        for k in keys:
            if k in row and row[k].strip():
                return row[k].strip()
        return ''

    interventions_raw = split_pipe(get(row, 'Interventions'))
    interventions_parsed = [parse_intervention(i) for i in interventions_raw]
    intervention_types = list(dict.fromkeys(i['type'] for i in interventions_parsed))

    primary_outcomes = [parse_outcome(o) for o in split_pipe(get(row, 'Primary Outcome Measures'))]
    secondary_outcomes = [parse_outcome(o) for o in split_pipe(get(row, 'Secondary Outcome Measures'))]
    other_outcomes = [parse_outcome(o) for o in split_pipe(get(row, 'Other Outcome Measures'))]

    eligibility_raw = get(row, 'Eligibility Criteria', 'Eligibility criteria')
    eligibility = parse_eligibility(eligibility_raw)

    return {
        'nct_number': get(row, 'NCT Number', 'nct_id'),
        'brief_title': get(row, 'Title', 'Brief Title'),
        'official_title': get(row, 'Official Title'),
        'acronym': get(row, 'Acronym'),
        'sponsor': get(row, 'Sponsor', 'Lead Sponsor'),
        'responsible_party': get(row, 'Responsible Party'),
        'collaborators': split_pipe(get(row, 'Collaborators')),
        'study_type': get(row, 'Study Type'),
        'phases': split_pipe(get(row, 'Phases')),
        'status': get(row, 'Status', 'Overall Status'),
        'brief_summary': get(row, 'Brief Summary'),
        'conditions': split_pipe(get(row, 'Conditions')),
        'intervention_types': intervention_types,
        'interventions': interventions_parsed,
        'other_ids': split_pipe(get(row, 'Other IDs', 'Other Study IDs')),
        'primary_purpose': get(row, 'Primary Purpose'),
        'allocation': get(row, 'Allocation'),
        'intervention_model': get(row, 'Intervention Model'),
        'masking': get(row, 'Masking'),
        'enrollment': get(row, 'Enrollment'),
        'healthy_volunteers': get(row, 'Healthy Volunteers'),
        'minimum_age': get(row, 'Minimum Age'),
        'maximum_age': get(row, 'Maximum Age'),
        'sex': get(row, 'Sex'),
        'eligibility': eligibility,
        'primary_outcomes': primary_outcomes,
        'secondary_outcomes': secondary_outcomes,
        'other_outcomes': other_outcomes,
        'start_date': get(row, 'Start Date'),
        'primary_completion_date': get(row, 'Primary Completion Date'),
        'completion_date': get(row, 'Completion Date'),
        'first_posted': get(row, 'First Posted'),
        'last_update_posted': get(row, 'Last Update Posted'),
        'results_first_posted': get(row, 'Results First Posted'),
        'locations': get(row, 'Locations'),
        'funded_bys': split_pipe(get(row, 'Funded Bys', 'Funder Type')),
        'study_documents': get(row, 'Study Documents'),
        'url': get(row, 'URL'),
        'has_results': get(row, 'Has Results'),
        'expanded_access': get(row, 'Was There an Expanded Access Record?',
                               'Expanded Access Record'),
        'keywords': split_pipe(get(row, 'Keywords')),
        'mesh_terms': split_pipe(get(row, 'MeSH Terms', 'Condition MeSH',
                                  'Intervention MeSH')),
    }


def main():
    parser = argparse.ArgumentParser(description='Parse ClinicalTrials.gov CSV')
    parser.add_argument('csv_file', help='CSV file path')
    parser.add_argument('--index', type=int, default=None,
                        help='Parse only the Nth record (0-based)')
    args = parser.parse_args()

    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(json.dumps({'error': f'File not found: {csv_path}'}))
        sys.exit(1)

    results = []
    try:
        with open(csv_path, encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if args.index is not None and i != args.index:
                    continue
                results.append(parse_row(row))
    except UnicodeDecodeError:
        # 尝试 GBK 编码
        with open(csv_path, encoding='gbk', newline='') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if args.index is not None and i != args.index:
                    continue
                results.append(parse_row(row))

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
