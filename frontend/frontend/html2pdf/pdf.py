import os
from django.conf import settings
from xhtml2pdf import pisa
from django.template.loader import get_template
from frontend.common import constant as mcs
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from xhtml2pdf.default import DEFAULT_FONT
#
# pdfmetrics.registerFont(TTFont('simsun', 'static/fonts/simsun.ttf'))
# DEFAULT_FONT['simsun'] = 'simsun'


def convertHtmlToPdf(sourceHtml, outputFilename):
    resultFile = open(outputFilename, "w+b")
    pisaStatus = pisa.CreatePDF(sourceHtml,dest=resultFile, link_callback=link_callback)
    # pisaStatus = pisa.CreatePDF(sourceHtml.encode('UTF-8'), dest=resultFile, encoding='UniGB-UTF16-H')
    resultFile.close()
    return resultFile


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    # Typically /home/userX/project_static/media/
    mRoot = settings.MEDIA_ROOT

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    path = mcs.system_project_path + path

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


def render_pdf(context, outputfilepath):
    template_path = 'pdfgeneration/template.html'
    template = get_template(template_path)
    html = template.render(context)
    response = convertHtmlToPdf(html, outputfilepath)
    return response
