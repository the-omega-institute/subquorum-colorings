"""Package the checked tag, generated PDF and verification receipts."""
import hashlib
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED


ROOT = Path(__file__).resolve().parents[1]


def package(path, files):
    manifest = {}
    with ZipFile(path,'w',ZIP_DEFLATED) as out:
        for name, source in sorted(files.items()):
            data = source.read_bytes()
            out.writestr(name,data)
            manifest[name] = hashlib.sha256(data).hexdigest()
        out.writestr('MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
    with ZipFile(path) as check:
        assert check.testzip() is None
        assert all(hashlib.sha256(check.read(name)).hexdigest()==digest
                   for name,digest in manifest.items())


if __name__ == '__main__':
    output = ROOT/'dist'
    output.mkdir(exist_ok=True)
    pdf = ROOT/'validation/manuscript/paper.pdf'
    assert pdf.is_file()
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    required = ['manuscript','lean-verification','finite-controls']
    required += [f'grid-width-{m}' for m in (8,9,10,11)]
    for artifact in required:
        receipts = list((ROOT/'validation'/artifact).rglob('commit.txt'))
        assert receipts, f'missing verification receipt: {artifact}'
        assert all(p.read_text().strip()==commit for p in receipts), artifact
    (output/'paper.pdf').write_bytes(pdf.read_bytes())
    package(output/'latex-source.zip', {'paper.tex':ROOT/'manuscript/paper.tex',
                                       'README.md':ROOT/'docs/LATEX_SOURCE.md',
                                       'LICENSE':ROOT/'LICENSE', 'NOTICE':ROOT/'NOTICE'})
    tracked = subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    files = {name:ROOT/name for name in tracked if name}
    files.update({str(p.relative_to(ROOT)):p for p in (ROOT/'validation').rglob('*') if p.is_file()})
    package(output/'research-package.zip',files)
    sums = [f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}'
            for p in sorted(output.iterdir()) if p.name!='SHA256SUMS']
    (output/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
