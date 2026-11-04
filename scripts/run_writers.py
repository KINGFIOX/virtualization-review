#!/usr/bin/env python3
"""Run the user-selected DeepSeek writer with scoped chapter prompts."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import argparse
import json
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
PROVIDER = 'glm-gateway-r'  # Existing via-feilian route, confirmed by the user.
MODEL = 'deepseek-v4-pro'


def run_one(name):
    prompt_path = ROOT / 'prompts' / f'{name}.md'
    usage_path = ROOT / 'logs' / f'{name}-usage.json'
    stdout_path = ROOT / 'logs' / f'{name}-stdout.txt'
    stderr_path = ROOT / 'logs' / f'{name}-stderr.txt'
    prompt = prompt_path.read_text(encoding='utf-8')
    command = [
        'hermes', '--provider', PROVIDER, '--model', MODEL,
        '--ignore-rules', '--toolsets', 'file', '--reasoning', 'high',
        '--usage-file', str(usage_path), '-z', prompt,
    ]
    start = time.monotonic()
    print(f'START {name}: provider={PROVIDER} model={MODEL}', flush=True)
    with stdout_path.open('w', encoding='utf-8') as out, stderr_path.open('w', encoding='utf-8') as err:
        try:
            result = subprocess.run(command, cwd=ROOT, stdout=out, stderr=err, timeout=1500)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = 124
    usage = json.loads(usage_path.read_text()) if usage_path.exists() else {}
    output = ROOT / 'chapters' / f'{name}.tex'
    text = output.read_text(encoding='utf-8') if output.exists() else ''
    cjk = len(re.findall(r'[\u4e00-\u9fff]', text))
    record = {
        'task': name, 'requested_provider': PROVIDER, 'requested_model': MODEL,
        'usage_model': usage.get('model'), 'cli_exit_code': code,
        'reported_completed': usage.get('completed'), 'reported_failed': usage.get('failed'),
        'seconds': round(time.monotonic() - start, 2), 'output': str(output),
        'output_bytes': len(text.encode('utf-8')), 'cjk_characters': cjk,
        'prompt': str(prompt_path), 'usage_file': str(usage_path),
        'stdout': str(stdout_path), 'stderr': str(stderr_path),
    }
    record['ready_for_review'] = (code == 0 and usage.get('model') == MODEL and bool(text) and cjk >= 500 and not usage.get('failed', False))
    (ROOT/'logs'/f'{name}-result.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('FINISH '+json.dumps(record, ensure_ascii=False), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tasks', nargs='*', default=['00-intro','01-software','02-hardware','03-nested'])
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    records = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(run_one, n) for n in args.tasks]
        for future in as_completed(futures):
            records.append(future.result())
    records.sort(key=lambda x:x['task'])
    manifest = ROOT/'logs'/'writer-run.json'
    manifest.write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('ALL_TASKS_FINISHED '+str(manifest), flush=True)
    raise SystemExit(0 if all(r['ready_for_review'] for r in records) else 1)

if __name__ == '__main__':
    main()
