import progressbar # pip install progressbar2

# static class variables
serial = 0
visited = []
ignore = ['ico', 'css', 'js', 'png', 'jpg', 'xml', 'json', 'svg', 'woff2', 'doc', 'aspx', 'pdf', 'io', 'php']

# design for progress bar
widgets = [
    progressbar.Timer(format='elapsed time: %(elapsed)s'), ' ',
    progressbar.Bar('*'), '',
    progressbar.Percentage(), '',
]