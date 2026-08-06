from pathlib import Path

root = Path('D:/deeplearning/yolo_manim')
mapping = {
    'MTensor1D': 'MTensor1D',
    'MTensor2D': 'MTensor2D',
    'MTensor3D': 'MTensor3D',
    'MTensor4D': 'MTensor4D',
}

changed = []
for p in root.rglob('*.py'):
    text = p.read_text(encoding='utf-8')
    new = text
    for old, newname in mapping.items():
        new = new.replace(old, newname)
    if new != text:
        p.write_text(new, encoding='utf-8')
        changed.append(str(p))

print('changed', len(changed))
for c in changed:
    print(c)
