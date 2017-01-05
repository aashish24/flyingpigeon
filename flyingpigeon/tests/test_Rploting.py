import pytest
from rpy2.robjects.packages import importr

from os import remove
grDevices = importr("grDevices")
base = importr("base")


def test_plot():
    # ds = importr("datasets")
    gr = importr("graphics")
    gr.plot(500,400)
    grDevices.dev_off()


def test_plain():
    grDevices.pdf(file='Rplot.pdf')
    grDevices.dev_off()
    remove('Rplot.pdf')
    png = grDevices.png(filename='Rplot.png', type='cairo')
    grDevices.dev_off()
    grDevices.postscript('Rplot.eps')
    grDevices.dev_off()
    remove('Rplot.eps')


def test_pdf_garbage():
    grDevices.pdf(file='Rplot.pdf')
    garbage = grDevices.dev_off()
    remove('Rplot.pdf')


def test_png_garbage():
    png = grDevices.png(filename='Rplot.png', type='cairo')
    garbage = grDevices.dev_off()


def test_png_sink():
    logfile = "test_logfile.txt"
    base.sink(logfile)
    png = grDevices.png(filename='Rplot.png', type='cairo')
    grDevices.dev_off()
    base.unlink(logfile)


def test_png_invisible():
    png = grDevices.png(filename='Rplot.png', type='cairo')
    base.invisible(grDevices.dev_off())