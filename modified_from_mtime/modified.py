"""
If "modified" date/time is not defined in article metadata,
fall back to the UNIX mtime.
"""

from pelican import signals
from pelican.contents import Content, Article
from pelican.utils import SafeDatetime
import os
import datetime
def modified(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def add_modified(content):
    if not isinstance(content, Article):
        return
    
    if not content.settings.get('ALWAYS_MODIFIED', False):
        return

    if hasattr(content, 'date') and not hasattr(content, 'modified'):
        content.modified = modified(content.source_path)
        content.locale_modified = content.locale_date
    
def register():
    signals.content_object_init.connect(add_modified)
