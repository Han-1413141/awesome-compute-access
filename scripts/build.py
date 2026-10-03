"""Validate the source catalog and generate the Chinese reading views (stdlib only)."""
import argparse
from collections import Counter
import csv
from datetime import date
import io
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    'free-compute': '免费计算与云试用',
    'low-cost': '低价 GPU 与按量计算',
    'education': '学生与教学计划',
    'research': '科研资助与超算分配',
    'startup': '创业扶持与云额度',
    'open-source': '开源项目支持',
    'nonprofit': '公益与非营利支持',
    'china-policy': '国内算力券与地方政策',
    'api': '模型 API 与推理额度',
}
STATUSES = {'active':'可使用', 'application_required':'需申请或候补',
            'paused':'暂停申请', 'closed':'窗口结束或新用户关闭', 'unverified':'待核实'}
VERIFICATION = {'official_page':'已读官方资料', 'official_link_only':'官方入口或部分条款待核实',
                'readme_lead':'第三方线索，未完成官方核实'}
REQUIRED_TEXT = ['id','name','provider','benefit','eligibility','region','application',
                 'limits','cost_risks','status','verification','verified_on']
LIVE = {'active', 'application_required'}

def read_catalog():
    doc = json.loads((ROOT/'data/programs.json').read_text(encoding='utf-8'))
    assert set(doc) == {'schema_version','as_of','programs'}, 'Unknown catalog fields'
    date.fromisoformat(doc['as_of'])
    assert doc['schema_version'] == '1.0', 'Unsupported schema_version'
    assert isinstance(doc['programs'],list) and doc['programs'], 'Empty catalog'
    ids=set()
    for p in doc['programs']:
        assert set(p) == set(REQUIRED_TEXT + ['categories','resource_types','sources','notes']), f"Unknown fields: {p.get('id')}"
        assert isinstance(p['notes'],str), f"Invalid notes: {p.get('id')}"
        for field in REQUIRED_TEXT:
            assert isinstance(p.get(field),str) and p[field].strip(), f"{p.get('id')}: missing {field}"
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['id']), p['id']
        assert p['id'] not in ids, f"Duplicate id: {p['id']}"
        ids.add(p['id'])
        assert p['status'] in STATUSES, f"Unknown status: {p['id']}"
        assert p['verification'] in VERIFICATION, f"Unknown verification: {p['id']}"
        assert date.fromisoformat(p['verified_on']) <= date.fromisoformat(doc['as_of']), p['id']
        for field in ['categories','resource_types','sources']:
            assert isinstance(p.get(field),list) and p[field], f"{p['id']}: missing {field}"
            assert all(isinstance(v,str) and v.strip() for v in p[field]), p['id']
            assert len(p[field]) == len(set(p[field])), f"Duplicate {field}: {p['id']}"
        assert all(c in CATEGORIES for c in p['categories']), f"Unknown category: {p['id']}"
        for source in p['sources']:
            parts=urlsplit(source)
            assert parts.scheme == 'https' and parts.netloc, f"Invalid source: {p['id']}"
        assert not (p['status'] in LIVE and p['verification'] != 'official_page'), f"Unverified live entry: {p['id']}"
    return doc

def cell(s):
    return str(s).replace('|','\\|').replace('\n',' ')

def table(programs, prefix='programs/'):
    lines=['| 项目 | 资源 | 权益摘要 | 状态 | 核对日期 |', '|---|---|---|---|---|']
    for p in programs:
        lines.append(f"| [{cell(p['name'])}]({prefix}{p['id']}.md) | {cell(' / '.join(p['resource_types']))} | {cell(p['benefit'])} | {STATUSES[p['status']]} | {p['verified_on']} |")
    return '\n'.join(lines)

def generate(doc):
    programs = sorted(doc['programs'],key=lambda p:(p['provider'].casefold(),p['name']))
    stats=Counter(p['status'] for p in programs)
    outputs={}
    for p in programs:
        lines=[f"# {p['name']}", '', '[返回首页](../../README.md) · [全部项目](../catalog.md)', '',
               f"**状态：{STATUSES[p['status']]}**　｜　**资料核对：{p['verified_on']}**", '',
               f"提供方：{p['provider']}。资源类型：{'、'.join(p['resource_types'])}。", '',
               f"分类：{' · '.join('['+CATEGORIES[c]+'](../categories/'+c+'.md)' for c in p['categories'])}", '']
        if p['status'] not in LIVE:
            lines += ['> 本项不列入当前可申请推荐。状态所指对象及原因见下文；关闭新用户入口不一定表示现有用户停用。','']
        for title,field in [('可获得的权益','benefit'),('申请资格','eligibility'),('地区与中国大陆适用性','region'),
                            ('申请入口与材料','application'),('额度、期限与使用限制','limits'),('费用与到期处理','cost_risks')]:
            lines += [f'## {title}', '',p[field], '']
        if p.get('notes'): lines += ['## 补充说明','',p['notes'],'']
        lines += ['## 官方依据与核实范围','',f"核实层级：{VERIFICATION[p['verification']]}。核对日期表示阅读或检查来源的日期，不代表实际注册、获批、付费或运行验证。",'']
        lines += [f'- [来源 {i+1}：{urlsplit(url).netloc}]({url})' for i,url in enumerate(p['sources'])]
        lines += ['',f"数据标识：`{p['id']}`。发现变化请提交[更正](../../CONTRIBUTING.md)。",'']
        outputs[f"docs/programs/{p['id']}.md"]='\n'.join(lines)
    for cid,label in CATEGORIES.items():
        selected=[p for p in programs if cid in p['categories']]
        available=[p for p in selected if p['status'] in LIVE]
        other=[p for p in selected if p['status'] not in LIVE]
        lines=[f'# {label}','','[返回首页](../../README.md) · [全部项目](../catalog.md)','',
               f"共 {len(selected)} 项；其中可使用或需申请 {len(available)} 项，暂停、历史或待核实 {len(other)} 项。",'',
               '申请制项目仍需审核；候补状态、地区限制和实际资源类型请打开详情查看。','',table(available,'../programs/')]
        if other: lines+=['','## 暂停、历史与待核实','',table(other,'../programs/')]
        outputs[f'docs/categories/{cid}.md']='\n'.join(lines)+'\n'
    outputs['docs/catalog.md']='# 全部项目目录\n\n[返回首页](../README.md)\n\n同一计划不同档位合为一项，多分类不重复计数。点击项目查看申请资格、地区、费用和官方依据。\n\n'+table(programs)+'\n'
    outputs['docs/archive.md']='# 暂停、历史与待核实项目\n\n[返回首页](../README.md)\n\n这些记录不作为当前可申请权益推荐。保留它们是为了说明旧教程、旧领取入口与历史申报通知的当前状态。\n\n'+table([p for p in programs if p['status'] not in LIVE])+'\n'
    outputs['docs/sources.md']='# 官方来源索引\n\n[返回首页](../README.md)\n\n每条链接都对应具体项目。页面可打开只证明可访问，不证明当前开放、适合所有国家或免费。\n\n'+'\n'.join(f"- [{p['name']}](programs/{p['id']}.md)："+'；'.join(f'[{urlsplit(u).netloc}]({u})' for u in p['sources']) for p in programs)+'\n'
    headline=' · '.join(f"{STATUSES[s]} {stats[s]}" for s in STATUSES)
    lines=['# 算力普惠指南 · Awesome Compute Access','',
      '免费算力、低价 GPU、学生教育、科研资助、创业扶持、开源公益支持与国内算力券的中文申请资料库。', '',
      f"**本轮资料核对：{doc['as_of']} · 收录 {len(programs)} 个计划与平台条目**",'',headline,'',
      '[全部项目](docs/catalog.md) · [暂停与待核实](docs/archive.md) · [申请指南](docs/apply-guide.md) · [低价算力比较方法](docs/pricing-guide.md) · [已有仓库调研](docs/related-repositories.md) · [参与补充](CONTRIBUTING.md)', '',
      '每项记录权益、资格、地区、申请材料、期限与限制、费用、状态和官方来源。免费 Notebook、云抵扣、模型 API、教学实验、工具订阅分别标注；最高资助额不等于人人可领。', '',
      '本版已阅读官方资料并整理中文说明，未逐个平台注册、申请或运行任务。动态配额和无法确认的活动会明确标为待核实；不收共享账号、出售教育认证、滥用注册或返利推广链接。', '',
      '## 按需求查找','',
      '| 你的情况 | 从这里开始 | 先看什么 |','|---|---|---|',
      '| 想立即做小实验 | [免费计算](docs/categories/free-compute.md) | GPU是否保证、会话上限、文件保存 |',
      '| 需要连续跑训练 | [低价GPU](docs/categories/low-cost.md) / [科研计划](docs/categories/research.md) | 显存、是否可抢占、存储与重跑成本 |',
      '| 在校学生或任课教师 | [教育计划](docs/categories/education.md) | 是学生本人还是教师/学校申请 |',
      '| 做学术研究 | [科研与超算](docs/categories/research.md) | 研究方向、机构所在地、成果开放要求 |',
      '| 正在做创业项目 | [创业支持](docs/categories/startup.md) | 公司注册、融资、合作方、分档条件 |',
      '| 维护开源或公益项目 | [开源支持](docs/categories/open-source.md) / [非营利](docs/categories/nonprofit.md) | 项目活跃度、组织资格、资源用途 |',
      '| 中国大陆团队找补贴 | [国内政策](docs/categories/china-policy.md) | 城市、申请窗口、合同发票、补贴对象 |',
      '| 只需调用模型 | [API额度](docs/categories/api.md) | 支持地区、模型限速、数据政策、有效期 |','',
      '## 分类目录','', '| 分类 | 全部条目 | 可使用或需申请 |','|---|---:|---:|']
    for cid,label in CATEGORIES.items():
        selected=[p for p in programs if cid in p['categories']]
        lines.append(f"| [{label}](docs/categories/{cid}.md) | {len(selected)} | {sum(p['status'] in LIVE for p in selected)} |")
    lines += ['', '一个项目可有多个分类，上表不能相加得到总数。学生包等集合入口与单项优惠可能重合，权益金额也不能相加。需申请或候补不代表保证录取，也不代表当前有库存。', '',
      '## 本轮确认的易错信息','',
      '- [SageMaker Studio Lab](docs/programs/sagemaker-studio-lab.md) 已关闭新用户入口，现有用户仍可使用。',
      '- [Cerebras Inference](docs/programs/cerebras-api-trial.md) 当前为绑卡后5美元、30天试用，官方明确无自动续给的永久免费层。',
      '- [DigitalOcean学生200美元](docs/programs/digitalocean-student-historical.md) 的旧入口跳转主页，本版不列为已确认可领取。',
      '- [Modal Starter](docs/programs/modal-starter.md) 的30美元月额度是计算额度，不覆盖Shared Endpoints的token账单。',
      '- [Google Cloud试用](docs/programs/google-cloud-free.md) 默认没有GPU配额；云代金券不是已分配GPU。',
      '- [Hugging Face普通CPU Spaces](docs/programs/huggingface-spaces-cpu.md) 与 [ZeroGPU](docs/programs/huggingface-zerogpu.md) 的新建资格不同，需要分别查看。', '',
      '## 数据与维护','',
      '- [JSON源数据](data/programs.json)：详情与目录的唯一来源。',
      '- [CSV表格](data/programs.csv)：UTF-8 BOM，可下载到Excel筛选。',
      '- [数据格式](data/schema.json)：字段、分类、状态及核实层级。',
      '- [来源索引](docs/sources.md) · [核实方法与覆盖边界](docs/methodology.md) · [更新记录](CHANGELOG.md)。', '',
      '修改源数据后运行 `python scripts/build.py`；提交前运行 `python scripts/build.py --check`。CI只检查数据与生成文档一致性，不会把链接可访问自动当成优惠有效，也不会自动改写核对日期。', '',
      '欢迎补充遗漏项目，尤其是校内HPC、区域算力券、开源维护者和非营利算力支持。每次补充应包含能证明当前权益和资格的官方链接。', '',
      '## 许可证','',
      '本仓库原创中文整理和代码采用 [MIT](LICENSE)。事实来自各计划官方页面，供应商名称、商标及原始条款仍归其权利人；申请与使用按供应商规则执行。已有项目及本次比较见[调研记录](docs/related-repositories.md)。','']
    outputs['README.md']='\n'.join(lines)
    stream=io.StringIO(newline='')
    fields=['id','name','provider','categories','resource_types','benefit','eligibility','region','application','limits','cost_risks','status','verification','verified_on','notes','sources']
    writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore',lineterminator='\n')
    writer.writeheader()
    for p in programs: writer.writerow({k:(' | '.join(p[k]) if isinstance(p.get(k),list) else p.get(k,'')) for k in fields})
    outputs['data/programs.csv']='\ufeff'+stream.getvalue()
    return outputs

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    doc=read_catalog()
    outputs=generate(doc)
    differences=[]
    for rel,text in outputs.items():
        path=ROOT/rel
        expected=text.encode('utf-8')
        if args.check:
            if not path.exists() or path.read_bytes()!=expected: differences.append(rel)
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(expected)
    assert not differences, 'Generated files out of date: '+', '.join(differences)
    # Only local links are checked; availability of an official URL is not program eligibility.
    for rel,text in outputs.items():
        if not rel.endswith('.md'): continue
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if target.startswith(('https://','http://','#')): continue
            assert (ROOT/rel).parent.joinpath(target.split('#')[0]).exists(), f'Broken local link: {rel} -> {target}'
    print(f"OK: {len(doc['programs'])} programs; {len(outputs)} generated files; local links checked")

if __name__=='__main__': main()
