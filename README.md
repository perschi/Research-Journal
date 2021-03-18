# Research-Journal
A template for creating a research journal in Markdown exportable to Html supporting helpful tags.


## Features

The research journal can be written entirely in Markdown but is inteded to be read in html in the browser.
The conversion in mainly done using pandoc but includes some tags that support you while writing it.

### Table of Content

The html version of your journal will contain a table of content of hyperlinks.

### Customizable Appearance using CSS

When you are not happy with the appearance of your research journal you can adapt the journal.css to your liking.

### Tikz plots

Using the following 

```
<tikz name=[Name of the file]>
% Your tikz code goes here
</tikz>
```
The building scripts creates svgs in the assets directory that are included in your html.

### Interactive Plots

The building script supports the creation of interactive charts using vega.
To create an interactive chart use the following syntax

```
<altair data=[path to a csv file]>
# Python code that can use altair as alt, pandas as pd and data as the read csv.
# The final chart should be assigned to a variable named chart.
<altair>
```

### Findings
Another special tag is the finding tag. The idea is to highlight main findings within its scope.
Additionally, the findings are summarized in the end of the document.

```
<finding>
Your main points
</finding>
```

### Citations

Citations can be put in the bibliography.bib file as usually. To cite a key in the markdown file use @[key of bib entry].

## Requirements

- pandoc
- pdflatex
    - tikz
- pdf2svg
- python
    - pandas
    - altair
