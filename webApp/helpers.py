from flask import request, url_for

notes = {
  0: 'do the shopping',
  1: 'build the codez',
  2: 'paint the door',
}

def note_repr(key):
  return {
    'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
    'text': notes[key]
  }