import os
import sys
import shutil
from pybtex.database import parse_file  # pip install pybtex
from pybtex.database import BibliographyData, Entry  # pip install pybtex


# location of files
path_base = os.path.dirname(os.path.abspath(__file__))
path_bibfile = os.path.join(path_base, "my_citations.bib")
path_output_html = os.path.join(path_base, "my_citations.html")
path_output_bibs = os.path.join(path_base, "../downloads/bibtex/")


# loop through the citations
# find all the ones that have my name attached to it
bib_data = parse_file(path_bibfile)
my_publications = {}
for key in bib_data.entries:
    entry = bib_data.entries[key]
    for author in entry.persons["author"]:
        if "geneva" in author.last_names[0].lower():
            my_publications[key] = entry

# now separate them into different types
bib_journals = {}
bib_conferences = {}
bib_workshops = {}
bib_unknown = {}
for key in my_publications:
    pub = my_publications[key]
    if pub.type == "article":
        bib_journals[key] = pub
    elif pub.type == "inproceedings":
        bib_conferences[key] = pub
    elif pub.type == "conference":
        bib_workshops[key] = pub
    else:
        bib_unknown[key] = pub

# debug stats to see if we processed ok...
print("parsed total of " + str(len(my_publications)) + " publications")
print("  - " + str(len(bib_journals)) + " journals")
print("  - " + str(len(bib_conferences)) + " conferences")
print("  - " + str(len(bib_workshops)) + " workshops")
if len(bib_unknown) > 0:
    for pub in bib_unknown:
        print(pub)
    sys.exit("ERROR: UNKNOWN TYPES IN BIB!!")

# now we can save the bibtex to file!
# we will delete the old folder, and create it as needed
if os.path.exists(path_output_bibs):
    shutil.rmtree(path_output_bibs)
if not os.path.exists(path_output_bibs):
    os.makedirs(path_output_bibs)
for key in my_publications:
    pub = my_publications[key]
    path_file = os.path.join(path_output_bibs, key + ".bib")
    clean_fields = {}
    valid_fields = [
        "title",
        "year",
        "booktitle",
        "pages",
        "organization",
        "journal",
        "publisher",
        "volume",
        "number",
        "url",
    ]
    for key_field in pub.fields:
        if key_field in valid_fields:
            clean_fields[key_field] = pub.fields[key_field]
    clean_pub = Entry(pub.type, fields=clean_fields, persons=pub.persons)
    data = BibliographyData(entries=[(key, clean_pub)])
    data.to_file(path_file, bib_format="bibtex")
print("done updating .bib files on disk...")


# now lets try to generate our HTML file!
def get_html_from_bibs(publications):
    html = '<table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;">'
    html += '<tbody>\n\n'
    for key, pub in publications:
        # image block
        extra_stuff = ''
        if "highlight" in pub.fields:
            extra_stuff += 'class="highlight"'
        html += '<tr onmouseout="stop(\''+key+'\')" onmouseover="start(\''+key+'\')" '+extra_stuff+'>\n'
        html += '<td style="padding:20px;width:25%;vertical-align:middle">\n'
        html += '<div class="one">\n'
        if "img0" in pub.fields:
            html += '<a href="images/'+pub.fields["img0"]+'">'
            if "img1" in pub.fields:
                html += '<div class="two" id="'+key+'_2">\n'
                # html += '<video width=100% height=100% muted autoplay loop paused>\n'
                # html += '<source src="images/'+pub.fields["img1"]+'" type="video/mp4">\n'
                # html += '</video>\n'
                html += '<img lazyload async id="'+key+'_3" data-src="images_compressed/'+pub.fields["img1"]+'" type="image/webp" />\n'
                html += '</div>\n'
            html += '<img lazyload async id="'+key+'_1" src="thumbnails/'+pub.fields["img0"]+'" />'
            if "img1" in pub.fields:
                html += '<script type="text/javascript">stop("'+key+'")</script>\n'
        html += '</div>\n'
        html += '</td>\n'
        # title
        html += '<td style="padding:20px;width:75%;vertical-align:middle">\n'
        clean_title = pub.fields["title"].replace("{","").replace("}","")
        if "url_paper" in pub.fields:
            html += '<a href="'+pub.fields["url_paper"]+'">'
            html += '<papertitle>'+clean_title+'</papertitle>'
            html += '</a>\n'
        else:
            html += '<papertitle>'+clean_title+'</papertitle>'
        html += '<br>\n'
        # authors
        equalcontrib = False
        if 'equalcontrib' in pub.fields:
            equalcontrib = True
        count = 0
        for author in pub.persons["author"]:
            if "geneva" in author.last_names[0].lower():
                html += '<strong>'
                html += author.first_names[0] + " " + author.last_names[0]
                if equalcontrib and count < 2:
                    html += '<sup>*</sup>'
                html += '</strong>'
            else:
                # html += '<a href="">'
                html += author.first_names[0] + " " + author.last_names[0]
                if equalcontrib and count < 2:
                    html += '<sup>*</sup>'
                # html += '</a>'
            if count + 1 != len(pub.persons["author"]):
                html += ', '
            count = count + 1
            html += '\n'
        # conference / journal
        html += '<br>\n'
        if "journal" in pub.fields:
            html += '<em>'+pub.fields["journal"]+'</em>, '+pub.fields["year"]+'\n'
        elif "booktitle" in pub.fields:
            html += '<em>'+pub.fields["booktitle"]+'</em>, '+pub.fields["year"]+'\n'
        else:
            print(pub)
            os.exit("invalid entry, no conference...")
        # links to things
        html += '<br>\n'
        html += '<a href="downloads/bibtex/'+key+'.bib">bibtex</a>'
        if "url_pdf" in pub.fields:
            html += ' / \n<a href="'+pub.fields["url_pdf"]+'">pdf</a>'
        if "url_arxiv" in pub.fields:
            html += ' / \n<a href="'+pub.fields["url_arxiv"]+'">arXiv</a>'
        if "url_report" in pub.fields:
            html += ' / \n<a href="'+pub.fields["url_report"]+'">tech report</a>'
        if "url_video" in pub.fields:
            html += ' / \n<a href="'+pub.fields["url_video"]+'">video</a>'
        if "url_talk" in pub.fields:
            html += ' / \n<a href="'+pub.fields["url_talk"]+'">talk</a>'
        if "url_code" in pub.fields:
            html += ' / \n<a href="'+pub.fields["url_code"]+'">code</a>'
        if "url_dataset" in pub.fields:
            html += ' / \n<a href="'+pub.fields["url_dataset"]+'">dataset</a>'
        if "url_slides" in pub.fields:
            html += ' / \n<a href="'+pub.fields["url_slides"]+'">slides</a>'
        if "url_poster" in pub.fields:
            html += ' / \n<a href="'+pub.fields["url_poster"]+'">poster</a>'
        # if "url" in pub.fields:
        #     html += ' / \n<a href="'+pub.fields["url"]+'">project</a>'
        html += '\n'
        # abstract / description
        html += '<p></p>\n'
        if "description" in pub.fields: 
            html += '<p>'+pub.fields["description"]+'</p>\n'
        html += '</td>\n'
        html += '</tr>\n\n'
    # finish table
    html += '</tbody></table>\n'
    return html


# html = '<table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;">'
# html += '<tbody><tr><td style="padding:20px;width:100%;vertical-align:middle"><heading>Journal</heading>\n'
# html += get_html_from_bibs(bib_journals)
# html += "</td></tr></tbody></table>\n"
# html += '<table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;">'
# html += '<tbody><tr><td style="padding:20px;width:100%;vertical-align:middle"><heading>Conference</heading>\n'
# html += get_html_from_bibs(bib_conferences)
# html += "</td></tr></tbody></table>\n"
# html += '<table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;">'
# html += '<tbody><tr><td style="padding:20px;width:100%;vertical-align:middle"><heading>Workshops</heading>\n'
# html += get_html_from_bibs(bib_workshops)
# html += "</td></tr></tbody></table>\n"


# https://stackoverflow.com/a/56842689
class reversor:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
           return other.obj < self.obj
def get_conf(pub):
    if "journal" in pub.fields:
        return pub.fields["journal"]
    elif "booktitle" in pub.fields:
        return pub.fields["booktitle"]
    print(pub)
    os.exit("invalid entry, no conference...")



list_my_publications = []
for key in my_publications:
    list_my_publications.append((key, my_publications[key]))
list_my_publications.sort(key=lambda x: (x[1].fields["year"], reversor(get_conf(x[1]))), reverse=True)



html = '<table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;">'
html += '<tbody><tr><td style="padding:20px;width:100%;vertical-align:middle">\n'
html += get_html_from_bibs(list_my_publications)
html += "</td></tr></tbody></table>\n"


# finally write it to file!
text_file = open(path_output_html, "w")
text_file.write(html)
text_file.close()


