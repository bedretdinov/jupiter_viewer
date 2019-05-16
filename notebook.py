
from nbconvert import HTMLExporter
from pyquery import PyQuery as pq
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor



def htmlNoteboook(file):

    exporter = HTMLExporter(template_file='/app/custom.tpl')

    output, resources = exporter.from_filename(file)

    dom = pq(output)
    dom('.output_stderr, .prompt').remove()

    return pq(dom).html()


def execNoteboook(file):

    try:

        with open(file) as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=999999, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': '/app/notebooks/'}})



        with open(file, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

    except:
        print(file)