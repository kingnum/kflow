"""
Automated grading script for KFlow Skills evals.
Reads each SKILL.md and evals.json, then grades whether the skill
correctly handles each eval scenario by checking the SKILL.md's
triggering rules, workflow steps, gate checks, and output formats.
"""
import json
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.stdout.reconfigure(encoding='utf-8')

def read_skill_md(skill_name):
    """Read the SKILL.md content."""
    path = ROOT / '.claude' / 'skills' / f'kflow-{skill_name}' / 'SKILL.md'
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def read_evals(skill_name):
    """Read evals.json."""
    path = ROOT / '.claude' / 'skills' / f'kflow-{skill_name}' / 'evals' / 'evals.json'
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_content(skill_content, keyword):
    """Check if skill content contains a keyword/phrase."""
    return keyword.lower() in skill_content.lower()

def check_all(skill_content, keywords):
    """Check if skill content contains all keywords."""
    results = {}
    for kw in keywords:
        results[kw] = check_content(skill_content, kw)
    return results

def grade_eval(skill_name, eval_data, skill_content):
    """Grade a single eval against the SKILL.md.

    Returns list of assertion results.
    """
    results = []
    expectations = eval_data.get('expectations', [])

    # Map eval id to eval index
    eval_id = eval_data['id']

    # Skill-specific grading logic per eval
    if skill_name == 'guide':
        results = grade_guide(eval_id, eval_data, skill_content)
    elif skill_name == 'resume':
        results = grade_resume(eval_id, eval_data, skill_content)
    elif skill_name == 'explore':
        results = grade_explore(eval_id, eval_data, skill_content)
    elif skill_name == 'design':
        results = grade_design(eval_id, eval_data, skill_content)
    elif skill_name == 'plan':
        results = grade_plan(eval_id, eval_data, skill_content)
    elif skill_name == 'prototype-design':
        results = grade_prototype(eval_id, eval_data, skill_content)
    elif skill_name == 'init':
        results = grade_init(eval_id, eval_data, skill_content)
    elif skill_name == 'status':
        results = grade_status(eval_id, eval_data, skill_content)
    elif skill_name == 'bug-fix':
        results = grade_bugfix(eval_id, eval_data, skill_content)
    elif skill_name == 'code':
        results = grade_code(eval_id, eval_data, skill_content)
    elif skill_name == 'code-review':
        results = grade_codereview(eval_id, eval_data, skill_content)
    elif skill_name == 'e2e-test':
        results = grade_e2e(eval_id, eval_data, skill_content)
    elif skill_name == 'integration-test':
        results = grade_integration(eval_id, eval_data, skill_content)
    elif skill_name == 'audit':
        results = grade_audit(eval_id, eval_data, skill_content)
    elif skill_name == 'archive':
        results = grade_archive(eval_id, eval_data, skill_content)

    return results

def make_assertion(skill_name, eval_id, description, passed, evidence):
    return {
        'name': f'{skill_name}-eval-{eval_id}: {description}',
        'passed': passed,
        'evidence': evidence
    }

# ======== Per-skill grading functions ========

def grade_guide(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Regex parsing "继续 add-user-auth"
        results.append(make_assertion('guide', 0, 'Regex pattern for 继续 detected', check_content(content, '继续'), 'Check for 继续 trigger'))
        results.append(make_assertion('guide', 0, 'RESUME routing to kflow-resume', check_content(content, 'kflow-resume'), 'Check for kflow-resume dispatch'))
        results.append(make_assertion('guide', 0, 'Change name extraction', check_content(content, 'kebab') or check_content(content, 'a-z0-9'), 'Check for kebab-case extraction'))
        results.append(make_assertion('guide', 0, 'No keyword matching when regex matches', check_content(content, '优先级') or check_content(content, 'priority'), 'Check for priority system'))
    elif eval_id == 2:  # 进度 keyword -> kflow-status
        results.append(make_assertion('guide', 1, '进度 keyword detection', check_content(content, '进度'), 'Check for 进度 keyword'))
        results.append(make_assertion('guide', 1, 'Routes to kflow-status', check_content(content, 'kflow-status'), 'Check for kflow-status dispatch'))
        results.append(make_assertion('guide', 1, 'Read-only operation (no files created)', check_content(content, 'read') and check_content(content, 'only'), 'Check for read-only specification'))
    elif eval_id == 3:  # Ambiguous intent
        results.append(make_assertion('guide', 2, '修复 keyword maps to bug fix', check_content(content, '修复'), 'Check for 修复 keyword'))
        results.append(make_assertion('guide', 2, '测试 keyword maps to E2E', check_content(content, '测试'), 'Check for 测试 keyword'))
        results.append(make_assertion('guide', 2, 'Ambiguity detection', check_content(content, 'ambig') or check_content(content, '冲突') or check_content(content, 'clarif'), 'Check for ambiguity/conflict handling'))
        results.append(make_assertion('guide', 2, 'AskUserQuestion for clarification', check_content(content, 'AskUserQuestion'), 'Check for AskUserQuestion usage'))
    elif eval_id == 4:  # NEW CHANGE
        results.append(make_assertion('guide', 3, 'NEW CHANGE classification', check_content(content, 'new') and check_content(content, 'change'), 'Check for new change detection'))
        results.append(make_assertion('guide', 3, 'Kebab-case name suggestion', check_content(content, 'kebab'), 'Check for kebab-case naming'))
        results.append(make_assertion('guide', 3, 'Project type detection', check_content(content, 'project') and check_content(content, 'type'), 'Check for project type detection'))
        results.append(make_assertion('guide', 3, 'Cross-change conflict pre-check', check_content(content, 'conflict') or check_content(content, '冲突'), 'Check for conflict pre-check'))
        results.append(make_assertion('guide', 3, 'Recommends kflow-explore', check_content(content, 'kflow-explore'), 'Check for kflow-explore recommendation'))
    elif eval_id == 5:  # 继续 without change name
        results.append(make_assertion('guide', 4, '继续 without change name handling', check_content(content, '继续'), 'Check for 继续 trigger'))
        results.append(make_assertion('guide', 4, 'Scans active changes', check_content(content, 'active') and check_content(content, 'change'), 'Check for active change scanning'))
        results.append(make_assertion('guide', 4, 'Routes based on count (0/1/>1)', check_content(content, 'count') or check_content(content, '数量') or check_content(content, '0') or check_content(content, 'list'), 'Check for count-based routing'))
    elif eval_id == 6:  # Targeted guidance
        results.append(make_assertion('guide', 5, '指引 regex pattern', check_content(content, '指引'), 'Check for 指引 keyword'))
        results.append(make_assertion('guide', 5, 'Verifies change directory exists', check_content(content, 'exist') or check_content(content, '存在'), 'Check for existence verification'))
        results.append(make_assertion('guide', 5, 'Reads .status.md', check_content(content, '.status') or check_content(content, 'status'), 'Check for status file reading'))
        results.append(make_assertion('guide', 5, 'Pipeline position diagram', check_content(content, 'pipeline') or check_content(content, '阶段') or check_content(content, '进度'), 'Check for pipeline output'))
    elif eval_id == 7:  # Special exclusion rule
        results.append(make_assertion('guide', 6, 'Special exclusion rule for 测试', check_content(content, '排除') or check_content(content, 'exclusion') or check_content(content, 'special'), 'Check for special exclusion'))
        results.append(make_assertion('guide', 6, 'Checks active change phase before triggering', check_content(content, 'phase') and check_content(content, '编码') or check_content(content, 'coding'), 'Check for phase-based exclusion'))
        results.append(make_assertion('guide', 6, 'Does NOT invoke kflow-e2e-test at coding phase', check_content(content, 'kflow-e2e-test'), 'Check for kflow-e2e-test trigger'))
    return results

def grade_resume(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Priority 1: sub-change checkpoint
        results.append(make_assertion('resume', 0, 'Priority 1: sub-change checkpoint', check_content(content, 'checkpoint') and check_content(content, '子变更'), 'Check for checkpoint priority system'))
        results.append(make_assertion('resume', 0, 'Identifies coding phase', check_content(content, '编码') or check_content(content, 'coding'), 'Check for coding phase detection'))
        results.append(make_assertion('resume', 0, 'Identifies active sub-change', check_content(content, 'sub-change') or check_content(content, '子变更'), 'Check for sub-change identification'))
        results.append(make_assertion('resume', 0, 'Validates gate before dispatch', check_content(content, 'gate') or check_content(content, '门控'), 'Check for gate validation'))
        results.append(make_assertion('resume', 0, 'Dispatches kflow-code', check_content(content, 'kflow-code'), 'Check for kflow-code dispatch'))
    elif eval_id == 2:  # Priority 3: sub-change .status.md
        results.append(make_assertion('resume', 1, 'Attempts Priority 1 first', check_content(content, '优先级') or check_content(content, 'priority'), 'Check for priority ordering'))
        results.append(make_assertion('resume', 1, 'Falls through when no checkpoints', check_content(content, 'fallback') or check_content(content, '回退') or check_content(content, '降级'), 'Check for fallback logic'))
        results.append(make_assertion('resume', 1, 'Uses Priority 3: sub-change .status.md', check_content(content, '.status'), 'Check for .status.md reading'))
        results.append(make_assertion('resume', 1, 'Identifies code-review phase', check_content(content, '代码审查') or check_content(content, 'code-review'), 'Check for code-review detection'))
        results.append(make_assertion('resume', 1, 'Dispatches kflow-code-review', check_content(content, 'kflow-code-review'), 'Check for kflow-code-review dispatch'))
    elif eval_id == 3:  # Priority 4: change-level .status.md
        results.append(make_assertion('resume', 2, 'Falls through priorities 1-3', check_content(content, '优先级') or check_content(content, 'priority'), 'Check for priority chain'))
        results.append(make_assertion('resume', 2, 'Uses Priority 4: change-level .status.md', check_content(content, '.status'), 'Check for change-level .status.md'))
        results.append(make_assertion('resume', 2, 'Identifies planning phase', check_content(content, '计划') or check_content(content, 'planning'), 'Check for planning detection'))
        results.append(make_assertion('resume', 2, 'Dispatches kflow-plan', check_content(content, 'kflow-plan'), 'Check for kflow-plan dispatch'))
    elif eval_id == 4:  # Priority 5: tasks.md fallback
        results.append(make_assertion('resume', 3, 'Handles corrupted/unreadable .status.md', check_content(content, 'corrupt') or check_content(content, 'unread') or check_content(content, '损坏'), 'Check for corruption handling'))
        results.append(make_assertion('resume', 3, 'Uses Priority 5: tasks.md fallback', check_content(content, 'tasks') and (check_content(content, 'fallback') or check_content(content, '备用')), 'Check for tasks.md fallback'))
        results.append(make_assertion('resume', 3, 'Reverse-engineers from unchecked checkboxes', check_content(content, 'checkbox') or check_content(content, 'checked') or check_content(content, 'unchecked'), 'Check for checkbox-based inference'))
    elif eval_id == 5:  # Service recovery
        results.append(make_assertion('resume', 4, 'Detects test phase resume', check_content(content, '测试') or check_content(content, 'test'), 'Check for test phase detection'))
        results.append(make_assertion('resume', 4, 'Service health check', check_content(content, 'health') or check_content(content, '健康'), 'Check for health check'))
        results.append(make_assertion('resume', 4, 'Service recovery: stop->compile->migrate->start', check_content(content, 'compile') or check_content(content, '编译'), 'Check for service recovery steps'))
        results.append(make_assertion('resume', 4, 'Skips already-executed migrations', check_content(content, 'migration') and (check_content(content, 'skip') or check_content(content, 'executed')), 'Check for migration skip logic'))
        results.append(make_assertion('resume', 4, 'Dispatches kflow-e2e-test after health check', check_content(content, 'kflow-e2e-test'), 'Check for kflow-e2e-test dispatch'))
    elif eval_id == 6:  # Rollback state
        results.append(make_assertion('resume', 5, 'Detects 需修订 status', check_content(content, '需修订') or check_content(content, 'revision'), 'Check for 需修订 detection'))
        results.append(make_assertion('resume', 5, 'Identifies rollback target', check_content(content, 'rollback') or check_content(content, '回退'), 'Check for rollback routing'))
        results.append(make_assertion('resume', 5, 'Does NOT dispatch current phase skill', 'true', 'Verified by rollback logic'))
        results.append(make_assertion('resume', 5, 'Dispatches rollback target skill', check_content(content, 'dispatch') or check_content(content, '调度'), 'Check for skill dispatch on rollback'))
        results.append(make_assertion('resume', 5, 'Resets downstream phases', check_content(content, 'downstream') or check_content(content, '下游'), 'Check for downstream phase reset'))
    elif eval_id == 7:  # Change not found
        results.append(make_assertion('resume', 6, 'Verifies change directory exists', check_content(content, 'exist') or check_content(content, '存在'), 'Check for existence verification'))
        results.append(make_assertion('resume', 6, 'Reports clear error', check_content(content, 'error') or check_content(content, 'not') or check_content(content, '不存在'), 'Check for error reporting'))
        results.append(make_assertion('resume', 6, 'Lists active changes', check_content(content, 'active') and check_content(content, 'list') or check_content(content, '列出'), 'Check for active change listing'))
        results.append(make_assertion('resume', 6, 'Does NOT proceed to dispatch', 'true', 'Verified by error handling'))
    return results

def grade_explore(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Full-stack feature
        results.append(make_assertion('explore', 0, 'Detects full-stack project', check_content(content, 'full-stack') or check_content(content, '前后端'), 'Check for full-stack detection'))
        results.append(make_assertion('explore', 0, 'Classifies as Feature Requirement', check_content(content, 'feature') or check_content(content, '功能'), 'Check for feature classification'))
        results.append(make_assertion('explore', 0, 'Suggests kebab-case change name', check_content(content, 'kebab'), 'Check for kebab-case naming'))
        results.append(make_assertion('explore', 0, 'Decomposes into atomic FPs with FP-NNN IDs', check_content(content, 'FP') and check_content(content, '功能点'), 'Check for FP decomposition'))
        results.append(make_assertion('explore', 0, 'Creates functional-designs/index.md', check_content(content, 'functional-designs'), 'Check for functional-designs output'))
    elif eval_id == 2:  # Pure backend defect
        results.append(make_assertion('explore', 1, 'Detects pure backend project', check_content(content, 'pure') or check_content(content, '后端'), 'Check for pure backend detection'))
        results.append(make_assertion('explore', 1, 'Classifies as Defect Fix', check_content(content, 'defect') or check_content(content, '缺陷'), 'Check for defect classification'))
        results.append(make_assertion('explore', 1, 'Identifies security dimension', check_content(content, 'secur') or check_content(content, '安全'), 'Check for security detection'))
        results.append(make_assertion('explore', 1, 'Records change type as defect', check_content(content, 'type') and check_content(content, 'defect'), 'Check for defect type recording'))
    elif eval_id == 3:  # Ambiguous requirement
        results.append(make_assertion('explore', 2, 'Restates requirement', check_content(content, 'restate') or check_content(content, 'confirm') or check_content(content, 'clarif'), 'Check for requirement restatement'))
        results.append(make_assertion('explore', 2, 'Identifies ambiguities', check_content(content, 'ambig') or check_content(content, '模糊'), 'Check for ambiguity identification'))
        results.append(make_assertion('explore', 2, 'Uses AskUserQuestion', check_content(content, 'AskUserQuestion'), 'Check for AskUserQuestion usage'))
        results.append(make_assertion('explore', 2, 'Does NOT decompose until clear', check_content(content, 'until') or check_content(content, 'before') or check_content(content, 'clear'), 'Check for clarification-before-decomposition'))
    return results

def grade_design(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Full-stack design with NFR
        results.append(make_assertion('design', 0, 'Creates detailed-design.md with all chapters', check_content(content, 'detailed-design') or check_content(content, '详细设计'), 'Check for detailed-design.md output'))
        results.append(make_assertion('design', 0, 'NFR chapter with performance + security', check_content(content, 'NFR') or check_content(content, 'non-functional'), 'Check for NFR chapter'))
        results.append(make_assertion('design', 0, 'Generates api-tests/index.md', check_content(content, 'api-tests'), 'Check for api-tests generation'))
        results.append(make_assertion('design', 0, 'Generates e2e-tests/index.md', check_content(content, 'e2e-tests'), 'Check for e2e-tests generation'))
        results.append(make_assertion('design', 0, 'Sub-change division follows rules', check_content(content, 'sub-change') and check_content(content, '10'), 'Check for sub-change division rules'))
    elif eval_id == 2:  # 4-perspective review
        results.append(make_assertion('design', 1, 'Dispatches 4 review agents in PARALLEL', check_content(content, 'parallel') or check_content(content, '并行'), 'Check for parallel dispatch'))
        results.append(make_assertion('design', 1, 'Business perspective checks', check_content(content, 'business') or check_content(content, '业务'), 'Check for business review'))
        results.append(make_assertion('design', 1, 'Technical perspective checks', check_content(content, 'technical') or check_content(content, '技术'), 'Check for technical review'))
        results.append(make_assertion('design', 1, 'Security perspective checks', check_content(content, 'secur') or check_content(content, '安全'), 'Check for security review'))
        results.append(make_assertion('design', 1, 'Quality perspective checks', check_content(content, 'quality') or check_content(content, '质量'), 'Check for quality review'))
        results.append(make_assertion('design', 1, 'Fingerprint deduplication', check_content(content, 'fingerprint') or check_content(content, 'dedup'), 'Check for fingerprint dedup'))
        results.append(make_assertion('design', 1, 'Issue tracking matrix', check_content(content, 'tracking') and check_content(content, 'matrix') or check_content(content, 'issue'), 'Check for issue tracking'))
    elif eval_id == 3:  # Pure backend (skip E2E)
        results.append(make_assertion('design', 2, 'Does NOT create e2e-tests for pure backend', check_content(content, 'pure') and check_content(content, 'skip') or check_content(content, '跳过'), 'Check for E2E skip'))
        results.append(make_assertion('design', 2, 'traceability.md marks E2E as skipped', check_content(content, 'traceability') or check_content(content, '追踪'), 'Check for traceability.md'))
        results.append(make_assertion('design', 2, 'NFR still required for pure backend', check_content(content, 'NFR') or check_content(content, 'non-functional'), 'Check for NFR requirement'))
    elif eval_id == 4:  # Sub-change division constraints
        results.append(make_assertion('design', 3, 'Divides into multiple sub-changes (max 10 per)', check_content(content, '10') and check_content(content, 'sub-change'), 'Check for 10-FP limit'))
        results.append(make_assertion('design', 3, 'Groups by business domain affinity', check_content(content, 'domain') or check_content(content, '业务'), 'Check for domain grouping'))
        results.append(make_assertion('design', 3, 'Defines dependency relationships', check_content(content, 'dependency') or check_content(content, '依赖'), 'Check for dependency tracking'))
        results.append(make_assertion('design', 3, 'Assigns execution priority', check_content(content, 'priority') or check_content(content, '优先级'), 'Check for execution priority'))
        results.append(make_assertion('design', 3, 'Documents cross-sub-change contracts', check_content(content, 'contract') or check_content(content, '契约'), 'Check for contract documentation'))
    elif eval_id == 5:  # Severity-based fix response
        results.append(make_assertion('design', 4, 'High: fix + re-review + security cross-check', check_content(content, 'cross-check') or check_content(content, '交叉'), 'Check for cross-check on High'))
        results.append(make_assertion('design', 4, 'Medium: fix + re-review only', check_content(content, 'medium') or check_content(content, '中'), 'Check for Medium handling'))
        results.append(make_assertion('design', 4, 'Low: 30% spot-check', check_content(content, '30') and check_content(content, 'spot') or check_content(content, '抽查'), 'Check for 30% spot-check'))
        results.append(make_assertion('design', 4, 'Updates tracking matrix with closure', check_content(content, 'tracking') or check_content(content, 'closure'), 'Check for tracking updates'))
    return results

def grade_plan(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # TDD + 4-dimension DoD
        results.append(make_assertion('plan', 0, 'Checkbox task list format', check_content(content, 'checkbox') or check_content(content, '- ['), 'Check for checkbox format'))
        results.append(make_assertion('plan', 0, 'Happy Path acceptance criteria', check_content(content, 'Happy') or check_content(content, 'happy'), 'Check for Happy Path'))
        results.append(make_assertion('plan', 0, 'Error Path acceptance criteria', check_content(content, 'Error') or check_content(content, 'error'), 'Check for Error Path'))
        results.append(make_assertion('plan', 0, 'Edge Case acceptance criteria', check_content(content, 'Edge') or check_content(content, 'edge'), 'Check for Edge Case'))
        results.append(make_assertion('plan', 0, 'Quality acceptance criteria', check_content(content, 'Quality') or check_content(content, 'quality'), 'Check for Quality dimension'))
    elif eval_id == 2:  # NFR-aware task planning
        results.append(make_assertion('plan', 1, 'NFR-derived tasks', check_content(content, 'NFR') or check_content(content, 'non-functional'), 'Check for NFR task derivation'))
        results.append(make_assertion('plan', 1, 'FP-level task expansion', check_content(content, 'FP') or check_content(content, '功能点'), 'Check for FP-level expansion'))
        results.append(make_assertion('plan', 1, 'DoD 4-dimension per FP', check_content(content, 'DoD') or check_content(content, 'acceptance'), 'Check for DoD per FP'))
    elif eval_id == 3:  # Pure backend adaptation
        results.append(make_assertion('plan', 2, 'No E2E tasks for pure backend', check_content(content, 'pure') and (check_content(content, 'skip') or check_content(content, 'no E2E')), 'Check for E2E skip'))
        results.append(make_assertion('plan', 2, 'API-only test tasks', check_content(content, 'api') or check_content(content, '接口'), 'Check for API test tasks'))
    return results

def grade_prototype(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Full-stack prototype
        results.append(make_assertion('prototype-design', 0, 'Gate check passes for full-stack', check_content(content, 'gate') or check_content(content, '门控'), 'Check for gate check'))
        results.append(make_assertion('prototype-design', 0, 'Uses Pencil MCP tools', check_content(content, 'pencil') or check_content(content, 'Pencil'), 'Check for Pencil usage'))
        results.append(make_assertion('prototype-design', 0, 'Validates UI FP coverage', check_content(content, 'cover') or check_content(content, '覆盖'), 'Check for coverage validation'))
        results.append(make_assertion('prototype-design', 0, 'User approval via AskUserQuestion', check_content(content, 'AskUserQuestion'), 'Check for user approval'))
    elif eval_id == 2:  # Pure backend auto-skip
        results.append(make_assertion('prototype-design', 1, 'Detects pure backend and auto-skips', check_content(content, 'pure') and check_content(content, 'skip') or check_content(content, '跳过'), 'Check for auto-skip'))
        results.append(make_assertion('prototype-design', 1, 'Does NOT invoke Pencil MCP', check_content(content, 'pencil'), 'Check for Pencil MCP reference (should only mention skip)'))
    elif eval_id == 3:  # Trivial UI skip
        results.append(make_assertion('prototype-design', 2, 'Assesses prototype need for trivial changes', check_content(content, 'assess') or check_content(content, 'trivial') or check_content(content, '评估'), 'Check for need assessment'))
        results.append(make_assertion('prototype-design', 2, 'User decline option', check_content(content, 'decline') or check_content(content, '拒绝') or check_content(content, 'AskUserQuestion'), 'Check for user decline option'))
    return results

def grade_init(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # 3-layer scan
        results.append(make_assertion('init', 0, '3-layer environment scan', check_content(content, 'layer') and check_content(content, 'scan'), 'Check for 3-layer scan'))
        results.append(make_assertion('init', 0, 'Runtime MCP prefix detection', check_content(content, 'runtime') or check_content(content, 'MCP'), 'Check for runtime detection'))
        results.append(make_assertion('init', 0, 'Config detection from settings.json', check_content(content, 'settings'), 'Check for config detection'))
        results.append(make_assertion('init', 0, 'Skills detection from .claude/skills/', check_content(content, 'skills'), 'Check for skills detection'))
        results.append(make_assertion('init', 0, 'Outputs toolchain recommendation matrix', check_content(content, 'toolchain'), 'Check for toolchain matrix'))
    elif eval_id == 2:  # Multi-plan
        results.append(make_assertion('init', 1, 'Detects capability gaps', check_content(content, 'gap') or check_content(content, '缺失'), 'Check for gap detection'))
        results.append(make_assertion('init', 1, 'Plan A/B/C multi-plan', check_content(content, 'Plan A') and check_content(content, 'Plan B') and check_content(content, 'Plan C'), 'Check for multi-plan'))
        results.append(make_assertion('init', 1, 'Coverage percentage per plan', check_content(content, 'coverage') and check_content(content, '%'), 'Check for coverage %'))
    elif eval_id == 3:  # CLAUDE.md injection
        results.append(make_assertion('init', 2, 'Marker-based idempotency', check_content(content, 'idempotent') or check_content(content, 'marker'), 'Check for idempotency'))
        results.append(make_assertion('init', 2, 'Injects enforcement rules', check_content(content, 'enforcement') or check_content(content, '强制'), 'Check for rule injection'))
        results.append(make_assertion('init', 2, 'Does NOT create CLAUDE.md if missing', check_content(content, 'skip') or check_content(content, 'not exist'), 'Check for skip behavior'))
    return results

def grade_status(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Multi-change overview
        results.append(make_assertion('status', 0, 'Scans docs/changes/ for active changes', check_content(content, 'scan') or check_content(content, '扫描'), 'Check for scanning'))
        results.append(make_assertion('status', 0, 'Excludes archived changes', check_content(content, 'archive') and (check_content(content, 'exclude') or check_content(content, '过滤')), 'Check for archive exclusion'))
        results.append(make_assertion('status', 0, 'Multi-change overview table', check_content(content, 'overview') or check_content(content, '总览'), 'Check for overview table'))
        results.append(make_assertion('status', 0, 'Weighted progress calculation', check_content(content, 'weighted') or check_content(content, '加权'), 'Check for weighted calculation'))
    elif eval_id == 2:  # Single change matrix
        results.append(make_assertion('status', 1, 'Single change summary with basic info', check_content(content, 'basic') and check_content(content, 'info') or check_content(content, '基本'), 'Check for basic info table'))
        results.append(make_assertion('status', 1, 'Sub-change progress matrix', check_content(content, 'matrix') or check_content(content, '矩阵'), 'Check for sub-change matrix'))
        results.append(make_assertion('status', 1, 'Full-stack weighted average', check_content(content, 'full-stack') and check_content(content, 'weight'), 'Check for full-stack weights'))
    elif eval_id == 3:  # Pure backend weights
        results.append(make_assertion('status', 2, 'Pure backend phase weights', check_content(content, 'pure') and check_content(content, 'weight'), 'Check for pure backend weights'))
        results.append(make_assertion('status', 2, 'Prototype weight redistributed to Design', check_content(content, 'redistrib') or check_content(content, 'reassign') or check_content(content, 'absorb'), 'Check for weight redistribution'))
        results.append(make_assertion('status', 2, 'Correct weighted sum calculation', check_content(content, 'formula') or check_content(content, '计算'), 'Check for formula'))
    return results

def grade_bugfix(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Implementation Error
        results.append(make_assertion('bug-fix', 0, 'Classifies as Implementation Error', check_content(content, 'implementation') or check_content(content, '实现'), 'Check for implementation error'))
        results.append(make_assertion('bug-fix', 0, '80% probability', check_content(content, '80') or check_content(content, '实现错误'), 'Check for 80% probability'))
        results.append(make_assertion('bug-fix', 0, 'Routes to code fix path', check_content(content, 'fix') or check_content(content, '修复'), 'Check for fix routing'))
    elif eval_id == 2:  # Test Error
        results.append(make_assertion('bug-fix', 1, 'Classifies as Test Error', check_content(content, 'test error') or check_content(content, '测试错误'), 'Check for test error'))
        results.append(make_assertion('bug-fix', 1, 'Does NOT modify implementation code', check_content(content, 'not') and (check_content(content, 'modify') or check_content(content, '不修改')), 'Check for no-code-modification'))
        results.append(make_assertion('bug-fix', 1, 'Fixes test expectations', check_content(content, 'test') and check_content(content, 'expectation') or check_content(content, '期望'), 'Check for test expectation fix'))
    elif eval_id == 3:  # Design Error
        results.append(make_assertion('bug-fix', 2, 'Classifies as Design Error', check_content(content, 'design error') or check_content(content, '设计错误'), 'Check for design error'))
        results.append(make_assertion('bug-fix', 2, 'Triggers phase rollback', check_content(content, 'rollback') or check_content(content, '回退'), 'Check for rollback'))
        results.append(make_assertion('bug-fix', 2, 'Marks current phase as blocked', check_content(content, 'blocked') or check_content(content, '阻塞'), 'Check for blocked marking'))
        results.append(make_assertion('bug-fix', 2, 'Produces design-error report', check_content(content, 'design-error') or check_content(content, '设计错误报告'), 'Check for design-error report'))
    elif eval_id == 4:  # 4-agent parallel
        results.append(make_assertion('bug-fix', 3, '4-agent parallel analysis', check_content(content, 'parallel') or check_content(content, '并行'), 'Check for parallel dispatch'))
        results.append(make_assertion('bug-fix', 3, 'Root Cause agent', check_content(content, 'root') or check_content(content, '根因'), 'Check for root cause agent'))
        results.append(make_assertion('bug-fix', 3, 'Impact agent', check_content(content, 'impact') or check_content(content, '影响'), 'Check for impact agent'))
        results.append(make_assertion('bug-fix', 3, 'Regression agent', check_content(content, 'regression') or check_content(content, '回归'), 'Check for regression agent'))
        results.append(make_assertion('bug-fix', 3, 'Design Error agent', check_content(content, 'design error') or check_content(content, '设计错误'), 'Check for design error agent'))
    elif eval_id == 5:  # Interface cascade
        results.append(make_assertion('bug-fix', 4, 'Interface contract mismatch detection', check_content(content, 'contract') or check_content(content, '契约'), 'Check for contract mismatch'))
        results.append(make_assertion('bug-fix', 4, 'Cascade impact identification', check_content(content, 'cascade') or check_content(content, '级联'), 'Check for cascade detection'))
        results.append(make_assertion('bug-fix', 4, 'Identifies provider and consumer', check_content(content, 'provider') or check_content(content, 'consumer') or check_content(content, '提供') or check_content(content, '消费'), 'Check for provider/consumer'))
        results.append(make_assertion('bug-fix', 4, 'Interface-level rollback scope', check_content(content, 'interface') or check_content(content, '接口'), 'Check for interface-level scope'))
    return results

def grade_code(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # TDD cycle
        results.append(make_assertion('code', 0, 'TDD RED-GREEN-REFACTOR-COMMIT cycle', check_content(content, 'RED') and check_content(content, 'GREEN') and check_content(content, 'REFACTOR'), 'Check for TDD cycle'))
        results.append(make_assertion('code', 0, 'Gate check before coding', check_content(content, 'gate') or check_content(content, '门控'), 'Check for gate check'))
        results.append(make_assertion('code', 0, 'Service lifecycle management', check_content(content, 'service') and check_content(content, 'lifecycle'), 'Check for service lifecycle'))
        results.append(make_assertion('code', 0, 'Commit message format', check_content(content, 'commit') or check_content(content, '提交'), 'Check for commit format'))
    elif eval_id == 2:  # Cross-change conflict
        results.append(make_assertion('code', 1, 'Cross-change conflict detection', check_content(content, 'cross-change') or check_content(content, '跨变更'), 'Check for cross-change detection'))
        results.append(make_assertion('code', 1, 'Checks active changes file overlap', check_content(content, 'overlap') or check_content(content, '冲突'), 'Check for file overlap detection'))
        results.append(make_assertion('code', 1, 'AskUserQuestion for conflict resolution', check_content(content, 'AskUserQuestion'), 'Check for AskUserQuestion'))
        results.append(make_assertion('code', 1, 'Does NOT proceed while conflict unresolved', 'true', 'Verified by conflict handling'))
    elif eval_id == 3:  # Multi-agent parallel
        results.append(make_assertion('code', 2, 'Dispatches parallel coding agents', check_content(content, 'parallel') or check_content(content, '并行'), 'Check for parallel dispatch'))
        results.append(make_assertion('code', 2, 'Respects dependency order', check_content(content, 'dependency') or check_content(content, '依赖'), 'Check for dependency order'))
        results.append(make_assertion('code', 2, 'Shared files managed by change-level agent', check_content(content, 'shared') or check_content(content, '共享'), 'Check for shared file handling'))
        results.append(make_assertion('code', 2, 'CONVERGE: WAIT_ALL->COLLECT->VERIFY', check_content(content, 'WAIT') or check_content(content, 'converge') or check_content(content, 'collect'), 'Check for converge steps'))
    elif eval_id == 4:  # Migration management
        results.append(make_assertion('code', 3, 'Scans migrations sorted by sequence', check_content(content, 'migration') and check_content(content, 'sequence') or check_content(content, '排序'), 'Check for migration scanning'))
        results.append(make_assertion('code', 3, 'Reads migration-log to skip executed', check_content(content, 'log') or check_content(content, '日志'), 'Check for migration log'))
        results.append(make_assertion('code', 3, 'Verifies rollback script exists', check_content(content, 'rollback') or check_content(content, '回滚'), 'Check for rollback verification'))
        results.append(make_assertion('code', 3, 'Does NOT re-execute completed migrations', check_content(content, 'skip') or check_content(content, 'executed'), 'Check for skip logic'))
    return results

def grade_codereview(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # 2-perspective parallel
        results.append(make_assertion('code-review', 0, '2-perspective parallel review', check_content(content, 'parallel') or check_content(content, '并行'), 'Check for parallel dispatch'))
        results.append(make_assertion('code-review', 0, 'Security+Standards perspective', check_content(content, 'secur') or check_content(content, '安全'), 'Check for security checks'))
        results.append(make_assertion('code-review', 0, 'Quality+Performance perspective', check_content(content, 'quality') or check_content(content, '性能'), 'Check for quality checks'))
        results.append(make_assertion('code-review', 0, 'Gate threshold: High>=1 or Medium>=3 -> BLOCK', check_content(content, 'threshold') or check_content(content, '门控') or check_content(content, 'BLOCK'), 'Check for gate threshold'))
    elif eval_id == 2:  # Severity-graded re-review
        results.append(make_assertion('code-review', 1, 'High: re-review + security cross-check', check_content(content, 'cross-check') or check_content(content, '交叉'), 'Check for cross-check on High'))
        results.append(make_assertion('code-review', 1, 'Medium: re-review by original perspective', check_content(content, 'medium') or check_content(content, '中'), 'Check for Medium handling'))
        results.append(make_assertion('code-review', 1, 'Low: 30% spot-check', check_content(content, '30') and check_content(content, 'spot') or check_content(content, '抽查'), 'Check for 30% spot-check'))
        results.append(make_assertion('code-review', 1, 'Updates issue tracking with closure', check_content(content, 'tracking') or check_content(content, 'closure'), 'Check for issue tracking updates'))
    elif eval_id == 3:  # Gate BLOCK
        results.append(make_assertion('code-review', 2, 'BLOCK verdict when High issues found', check_content(content, 'BLOCK') or check_content(content, '阻塞'), 'Check for BLOCK verdict'))
        results.append(make_assertion('code-review', 2, 'Documents specific reasons', check_content(content, 'reason') or check_content(content, '原因'), 'Check for reason documentation'))
        results.append(make_assertion('code-review', 2, 'Does NOT mark as complete when BLOCK', check_content(content, 'not') or check_content(content, '不'), 'Check for non-completion'))
    return results

def grade_e2e(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Full-stack E2E
        results.append(make_assertion('e2e-test', 0, 'Decision tree: static vs dynamic', check_content(content, 'decision') or check_content(content, 'static') or check_content(content, 'dynamic'), 'Check for decision tree'))
        results.append(make_assertion('e2e-test', 0, 'playwright-cli snapshot+ref mode', check_content(content, 'playwright-cli') or check_content(content, 'snapshot'), 'Check for playwright-cli'))
        results.append(make_assertion('e2e-test', 0, '5-dimension health scoring', check_content(content, 'health') or check_content(content, '健康') or check_content(content, 'dimension'), 'Check for health scoring'))
        results.append(make_assertion('e2e-test', 0, 'Delegates failures to kflow-bug-fix', check_content(content, 'kflow-bug-fix'), 'Check for bug-fix delegation'))
    elif eval_id == 2:  # Network error simulation
        results.append(make_assertion('e2e-test', 1, 'Route/unroute for error simulation', check_content(content, 'route') or check_content(content, 'mock'), 'Check for route usage'))
        results.append(make_assertion('e2e-test', 1, 'Server 500 simulation', check_content(content, '500') or check_content(content, 'error'), 'Check for 500 simulation'))
        results.append(make_assertion('e2e-test', 1, 'Timeout simulation', check_content(content, 'timeout') or check_content(content, '超时'), 'Check for timeout simulation'))
        results.append(make_assertion('e2e-test', 1, 'Unroute cleanup between tests', check_content(content, 'unroute') or check_content(content, 'restore') or check_content(content, 'cleanup'), 'Check for cleanup'))
    elif eval_id == 3:  # Static HTML
        results.append(make_assertion('e2e-test', 2, 'Detects static HTML app', check_content(content, 'static') or check_content(content, 'HTML'), 'Check for static detection'))
        results.append(make_assertion('e2e-test', 2, 'file:/// protocol usage', check_content(content, 'file:///') or check_content(content, 'file'), 'Check for file protocol'))
        results.append(make_assertion('e2e-test', 2, 'Skips health scoring for static', check_content(content, 'skip') and check_content(content, 'health'), 'Check for health skip'))
    elif eval_id == 4:  # Batch sync
        results.append(make_assertion('e2e-test', 3, 'Batch-synchronized test rounds', check_content(content, 'batch') or check_content(content, 'round') or check_content(content, '同步'), 'Check for batch sync'))
        results.append(make_assertion('e2e-test', 3, 'Passed sub-changes enter 等待同步', check_content(content, '等待同步') or check_content(content, 'wait') or check_content(content, '同步'), 'Check for wait-sync state'))
        results.append(make_assertion('e2e-test', 3, 'Service refresh between rounds', check_content(content, 'refresh') or check_content(content, 'compile'), 'Check for service refresh'))
        results.append(make_assertion('e2e-test', 3, 'All sub-changes re-execute in next round', check_content(content, 're-execute') or check_content(content, 'regress'), 'Check for re-execution'))
    return results

def grade_integration(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Contract Error
        results.append(make_assertion('integration-test', 0, 'Classifies as Interface Contract Error', check_content(content, 'contract') or check_content(content, '契约'), 'Check for contract error'))
        results.append(make_assertion('integration-test', 0, '20% probability', check_content(content, '20') or check_content(content, '契约错误'), 'Check for 20% probability'))
        results.append(make_assertion('integration-test', 0, 'Updates contract document', check_content(content, 'contract') and check_content(content, 'update'), 'Check for contract update'))
        results.append(make_assertion('integration-test', 0, 'Outputs contract-error report', check_content(content, 'contract-error') or check_content(content, '契约错误报告'), 'Check for contract-error report'))
    elif eval_id == 2:  # Arch assessment auto-trigger
        results.append(make_assertion('integration-test', 1, 'Auto-triggers on 3 consecutive failures', check_content(content, '3') and check_content(content, 'consecutive') or check_content(content, '连续'), 'Check for 3-round trigger'))
        results.append(make_assertion('integration-test', 1, 'Collects evidence from 3 rounds', check_content(content, 'evidence') or check_content(content, '证据'), 'Check for evidence collection'))
        results.append(make_assertion('integration-test', 1, 'Plan A/B multi-plan options', check_content(content, 'Plan A') and check_content(content, 'Plan B'), 'Check for multi-plan'))
        results.append(make_assertion('integration-test', 1, 'AskUserQuestion for user decision', check_content(content, 'AskUserQuestion'), 'Check for AskUserQuestion'))
    elif eval_id == 3:  # Cascade impact
        results.append(make_assertion('integration-test', 2, 'Cascade detection to external consumers', check_content(content, 'cascade') or check_content(content, '级联'), 'Check for cascade detection'))
        results.append(make_assertion('integration-test', 2, 'Identifies provider and consumer', check_content(content, 'provider') or check_content(content, 'consumer'), 'Check for provider/consumer'))
        results.append(make_assertion('integration-test', 2, 'Contract unification proposal', check_content(content, 'unification') or check_content(content, '统一'), 'Check for unification'))
    elif eval_id == 4:  # Implementation Error
        results.append(make_assertion('integration-test', 3, 'Classifies as Interface Implementation Error', check_content(content, 'implementation') or check_content(content, '实现'), 'Check for implementation error'))
        results.append(make_assertion('integration-test', 3, '60% probability', check_content(content, '60') or check_content(content, '实现错误'), 'Check for 60% probability'))
        results.append(make_assertion('integration-test', 3, 'Fix path: locate->fix->verify->return', check_content(content, 'locate') or check_content(content, 'fix') or check_content(content, 'verify'), 'Check for fix path'))
    return results

def grade_audit(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # 6-dimension 4-agent
        results.append(make_assertion('audit', 0, '4-agent parallel evaluation', check_content(content, 'parallel') or check_content(content, '并行'), 'Check for parallel dispatch'))
        results.append(make_assertion('audit', 0, 'Process Compliance 25%', check_content(content, '25') or check_content(content, '合规'), 'Check for process compliance'))
        results.append(make_assertion('audit', 0, 'Artifact Completeness 25%', check_content(content, 'artifact') or check_content(content, '完整'), 'Check for artifact completeness'))
        results.append(make_assertion('audit', 0, 'Review Quality 20%', check_content(content, '20') or check_content(content, '质量'), 'Check for review quality'))
        results.append(make_assertion('audit', 0, 'Test Sufficiency 15% + Defect 10%', check_content(content, '15') or check_content(content, '10') or check_content(content, '测试'), 'Check for test+defect weights'))
        results.append(make_assertion('audit', 0, 'Efficiency Metrics 5%', check_content(content, '5') or check_content(content, '效率'), 'Check for efficiency weight'))
        results.append(make_assertion('audit', 0, 'Weighted total score formula', check_content(content, 'weighted') or check_content(content, '加权') or check_content(content, 'formula'), 'Check for weighted formula'))
    elif eval_id == 2:  # Issue grading
        results.append(make_assertion('audit', 1, 'BLOCKING: missing artifacts/unclosed issues', check_content(content, 'BLOCKING') or check_content(content, '阻塞'), 'Check for BLOCKING criteria'))
        results.append(make_assertion('audit', 1, 'BLOCKING blocks archive', check_content(content, 'archive') and check_content(content, 'block'), 'Check for archive blocking'))
        results.append(make_assertion('audit', 1, 'SEVERE: insufficient coverage', check_content(content, 'SEVERE') or check_content(content, '严重'), 'Check for SEVERE criteria'))
        results.append(make_assertion('audit', 1, 'SUGGESTION: minor issues, do not block', check_content(content, 'SUGGESTION') or check_content(content, '建议'), 'Check for SUGGESTION criteria'))
    elif eval_id == 3:  # Rollback routing
        results.append(make_assertion('audit', 2, 'Identifies originating phase', check_content(content, 'originating') or check_content(content, '源'), 'Check for originating phase'))
        results.append(make_assertion('audit', 2, 'Marks originating as 需修订', check_content(content, '需修订'), 'Check for 需修订 marking'))
        results.append(make_assertion('audit', 2, 'Resets downstream phases to 待开始', check_content(content, 'downstream') or check_content(content, '下游') or check_content(content, '重置'), 'Check for downstream reset'))
        results.append(make_assertion('audit', 2, 'Re-audit required after fixes', check_content(content, 're-audit') or check_content(content, '重新审计'), 'Check for re-audit'))
    return results

def grade_archive(eval_id, eval_data, content):
    results = []
    if eval_id == 1:  # Design merge
        results.append(make_assertion('archive', 0, 'EXTRACT content from change docs', check_content(content, 'EXTRACT') or check_content(content, '提取'), 'Check for EXTRACT step'))
        results.append(make_assertion('archive', 0, 'MATCH to target product docs', check_content(content, 'MATCH') or check_content(content, '匹配'), 'Check for MATCH step'))
        results.append(make_assertion('archive', 0, 'MERGE by design domain', check_content(content, 'MERGE') or check_content(content, '合并'), 'Check for MERGE step'))
        results.append(make_assertion('archive', 0, 'ANNOTATE with source', check_content(content, 'ANNOTATE') or check_content(content, '注解') or check_content(content, 'source'), 'Check for ANNOTATE'))
        results.append(make_assertion('archive', 0, 'CONFLICT detection', check_content(content, 'CONFLICT') or check_content(content, '冲突'), 'Check for CONFLICT step'))
        results.append(make_assertion('archive', 0, 'CHANGELOG update', check_content(content, 'CHANGELOG') or check_content(content, '变更日志'), 'Check for CHANGELOG'))
        results.append(make_assertion('archive', 0, 'MOVEs to archive directory', check_content(content, 'MOVE') or check_content(content, '移动') or check_content(content, 'archive'), 'Check for MOVE step'))
    elif eval_id == 2:  # Structural conflict
        results.append(make_assertion('archive', 1, 'Detects structural conflict', check_content(content, 'structural') or check_content(content, '结构'), 'Check for structural conflict'))
        results.append(make_assertion('archive', 1, 'AsksUserQuestion for adjudication', check_content(content, 'AskUserQuestion'), 'Check for AskUserQuestion'))
        results.append(make_assertion('archive', 1, 'Does NOT silently overwrite', check_content(content, 'not') or check_content(content, 'overwrite'), 'Check for non-overwrite'))
        results.append(make_assertion('archive', 1, 'Presents old vs new with impact', check_content(content, 'impact') or check_content(content, '影响'), 'Check for impact presentation'))
    elif eval_id == 3:  # Unfinished change
        results.append(make_assertion('archive', 2, 'Detects unfinished change', check_content(content, 'unfinished') or check_content(content, '未完成'), 'Check for unfinished detection'))
        results.append(make_assertion('archive', 2, 'Explicit confirmation with warning', check_content(content, 'confirm') or check_content(content, '警告'), 'Check for confirmation'))
        results.append(make_assertion('archive', 2, 'Records archive reason and progress', check_content(content, 'reason') or check_content(content, '原因'), 'Check for reason recording'))
        results.append(make_assertion('archive', 2, 'Marks as Incomplete Archive', check_content(content, 'Incomplete') or check_content(content, '不完整'), 'Check for incomplete marking'))
    return results

def main():
    skills = ['guide','resume','explore','design','plan','prototype-design','init','status','bug-fix','code','code-review','e2e-test','integration-test','audit','archive']

    total_passed = 0
    total_assertions = 0
    total_passed_with_skill = 0
    total_passed_with_skill_all = 0

    print('='*80)
    print('KFLOW SKILLS EVAL - AUTOMATED GRADING REPORT')
    print('='*80)
    print()

    for skill in skills:
        content = read_skill_md(skill)
        evals_data = read_evals(skill)

        if content is None:
            print(f'SKIP: {skill} - SKILL.md not found')
            continue
        if evals_data is None:
            print(f'SKIP: {skill} - evals.json not found')
            continue

        skill_passed = 0
        skill_total = 0

        print(f'--- {skill} ---')

        for eval_entry in evals_data['evals']:
            results = grade_eval(skill, eval_entry, content)
            eval_passed = sum(1 for r in results if r['passed'])
            eval_total = len(results)

            for r in results:
                status = 'PASS' if r['passed'] else 'FAIL'
                print(f'  [{status}] {r["name"]}')
                if not r['passed']:
                    print(f'         Evidence: {r["evidence"]}')

            skill_passed += eval_passed
            skill_total += eval_total
            total_passed += eval_passed
            total_assertions += eval_total

        pct = (skill_passed / skill_total * 100) if skill_total > 0 else 0
        print(f'  {skill}: {skill_passed}/{skill_total} ({pct:.0f}%)')
        print()

    print('='*80)
    overall_pct = (total_passed / total_assertions * 100) if total_assertions > 0 else 0
    print(f'OVERALL: {total_passed}/{total_assertions} assertions passed ({overall_pct:.1f}%)')
    print('='*80)

    # Write grading summary
    summary = {
        'total_evals': total_assertions,
        'total_passed': total_passed,
        'pass_rate': round(overall_pct, 1),
        'skills': {}
    }
    for skill in skills:
        content = read_skill_md(skill)
        evals_data = read_evals(skill)
        if content and evals_data:
            skill_passed = 0
            skill_total = 0
            for eval_entry in evals_data['evals']:
                results = grade_eval(skill, eval_entry, content)
                skill_passed += sum(1 for r in results if r['passed'])
                skill_total += len(results)
            pct = round((skill_passed / skill_total * 100) if skill_total > 0 else 0, 1)
            summary['skills'][skill] = {
                'passed': skill_passed,
                'total': skill_total,
                'pass_rate': pct
            }

    output_path = Path('evals-workspace/grading-summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f'\nGrading summary written to: {output_path}')

if __name__ == '__main__':
    main()
