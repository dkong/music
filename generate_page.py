import json
import sys
import glob
import os
import time

PAGE_TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Music</title><link rel="stylesheet" href="index.css"></head><body><ul>%(items)s</ul></body></html>"""

ENTRY_TEMPLATE = """<li><a href="%(filename)s">%(title)s<img src=%(image)s /></a><div>Saved: %(time)s</div><div><span>Length: %(duration)s</span> <span><a href=%(url)s>Original</a></span></div></li>"""

directory = sys.argv[1]
serve_directory = sys.argv[2]
output_page = sys.argv[3]

entries = []

files = glob.glob(os.path.join(directory, '*.mp3'))
for f in files:
    base, ext = os.path.splitext(f)
    filename = os.path.basename(f)
    asset_filename = serve_directory + '/' + filename

    json_filename = base + '.info.json'
    if os.path.exists(json_filename):
        data = json.load(open(json_filename))
    else:
        data = {}

    creation_time = os.stat(f).st_mtime

    duration = data.get('duration')
    if duration:
        minutes = duration / 60
        seconds = duration % 60
        duration = '%d:%02d' % (minutes, seconds)
    else:
        duration = '0'

    title = data.get('title', filename)

    metadata = {
        'title' : title,
        'filename' : unicode(asset_filename, 'utf-8'),
        'time' : time.ctime(creation_time) if creation_time else '',
        'ts' : creation_time,
        'duration' : duration,
        'image' : data.get('thumbnail'),
        'url' : data.get('webpage_url')
    }
    entries.append(metadata)

entries.sort(key=lambda x: x['ts'], reverse=True)

# Index identiifer
size = len(entries)
for i, entry in enumerate(entries):
    entry['title'] = '%d - %s' % (size - i, entry['title'])

with open(output_page, 'w') as f:
    entries_html = ''.join([ENTRY_TEMPLATE % d for d in entries])
    page_html = PAGE_TEMPLATE % {'items' : entries_html}
    f.write(page_html.encode('utf-8'))
    f.close()
