import argparse
import pathlib
import graphviz
import os

dst = pathlib.Path("other/diagrams")
src = pathlib.Path("pseudocode")
format = "png"

if not dst.exists():
    os.mkdir(dst)

files = pathlib.Path(src).glob('**/*.gv')
for file in files:
    print(f"Process {file.name}")
    source = graphviz.Source.from_file(file.name, directory=file.parent)
    source.render(directory=dst, format=format, cleanup=True)