import os
import re

with open('journal.md', 'r') as f:
    text = f.read()

pattern = re.compile('(?P<finding><finding>.*?<\/finding>)', re.DOTALL)

# build tikz patterns --------------------------------------------------------------------------------------------
tikz_pattern = re.compile('<tikz name=(?P<figure_name>.*?)>(?P<content>.*?)<\/tikz>', re.DOTALL)

print(tikz_pattern.findall(text))

# build pdf pictures

texfile = '\\documentclass{article}\n\
\\usepackage{tikz}\n\
\\usetikzlibrary{external}\n\
\\tikzexternalize[prefix=tikz/]\n\
\\begin{document}\n'


for name, tikz in tikz_pattern.findall(text):
    texfile += '\\begin{tikzpicture}\n' + tikz +'\n\\end{tikzpicture}\n'

texfile += '\\end{document}'

with open('assets/__tmp.tex', 'w') as f:
    f.write(texfile)

os.system('cd assets;pdflatex -synctex=1 -interaction=nonstopmode --shell-escape __tmp.tex')

# convert to svg
for k,(name, tikz) in enumerate(tikz_pattern.findall(text)):
    os.system('cd assets/tikz;pdf2svg __tmp-figure'+str(k)+'.pdf '+ name +'.svg')

# Remove tmp files
os.system('cd assets/; rm __tmp*')
os.system('cd assets/tikz/; rm __tmp*')



tikz_pattern = re.compile('<tikz name=(?P<figure_name>.*?)>.*?<\/tikz>', re.DOTALL)
text = tikz_pattern.sub('<img src=\"assets/tikz/\g<figure_name>.svg\" alt="Error">', text)

# altair plot support -------------------------------------------------------------------------------------------------------------
altair_header = """
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega@5"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-lite@4.8.1"></script>
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm//vega-embed@6"></script>
"""

altair_pattern = re.compile('<altair data=(?P<file>.*?)>(?P<code>.*?)<\/altair>', re.DOTALL)
matches = altair_pattern.finditer(text)
print(matches)
# add data loading
import pandas as pd
import altair as alt
wrapper = [
"""
data = pd.read_csv(""",
None,
')\n',
None,
'\nchart.save(\'./__tmp.html\')',
]

chart_pattern = re.compile('(?P<s><script>.*?</script>)', re.DOTALL)
for k,(match) in enumerate(reversed(list(matches))):
    wrapper[1] = match.group('file')
    wrapper[3] = match.group('code').lstrip(' \n')
    complete_code = ''.join(wrapper)
    exec(complete_code)
    
    with open('__tmp.html', 'r') as f:
        graph_text = f.read()
    
    graph_text = chart_pattern.findall(graph_text)[-1]

    text = text[:match.start()] +\
    "<div id=\"v"+str(k)+"\" class=\"altair\"></div>\n" +\
     graph_text.replace("\"vis\"",'\"v'+str(k)+'\"').replace("\"#vis\"",'\"#v'+str(k)+'\"') +\
      text[match.end():]


os.system('rm __tmp.html')
# latex math support --------------------------------------------------------------------------------------------------------------
equation_support = '\n<script type="text/x-mathjax-config">\n\
    MathJax.Hub.Config({\n\
      tex2jax: {\n\
        inlineMath: [["$","$"], ["\\(","\\)"]],\n\
        processEscapes: true\n\
      }\n\
    });\n\
    </script>\n\
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>\n\
    '

adapted_str =\
    '<div id=\'text\'>\n'+\
    equation_support +\
    altair_header +\
    text.replace('<finding>', '<div class="finding">').replace('</finding>','</div>') +\
    '\n\n# Overview of important findings\n\n' +\
    '\n'.join([x.replace('\n','').replace('<finding>','').replace('</finding>','').replace(' -', '-') for x in pattern.findall(text)]) +\
    '\n</div>'

with open('tmp.md', 'w') as f:
    f.write(adapted_str)

os.system('pandoc tmp.md -o journal.html -c journal.css -s --toc')
os.system('rm tmp.md')

# Add Table of content ---------------------------------------------
with open('journal.html', 'r') as f:
    html = f.read()

h_pattern = re.compile('<h(?P<depth>[1-6]) id=\"(?P<id>.*?)\">(?P<title>.*?)</h[1-6]>')

toc ="""
</header>
<div id=\"toc\">
<h1>Table of Content</h1>
"""

for k,(match) in enumerate(h_pattern.finditer(html)):
    depth = match.group('depth')
    id = match.group('id')
    content = match.group('title')

    toc +=  '<a href=\"#'+id+'\"><div class=\"toc_entry toc'+depth+'\">'+content+'</div></a>\n'

toc += '</div>'


with open('journal.html', 'w') as f:
    html = f.write(html.replace('</header>', toc))