import sys, pypdf
for f in sys.argv[1:]:
    r = pypdf.PdfReader(f)
    t = '\n'.join((p.extract_text() or '') for p in r.pages)
    open(f[:-4] + '.txt', 'w').write(t)
    print(f, len(r.pages), 'pages', len(t), 'chars')
