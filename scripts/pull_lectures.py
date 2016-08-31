import re
import sys
import urllib.request

def main(args):

    url = args[0]
    keyword = args[1]

    page_info = urllib.request.urlopen(url).read().decode('utf-8')
    hrefs = re.findall(r'href=".*?"', page_info)

    file_paths = []

    for ref in hrefs:
        if keyword in ref and ".pdf" in ref:
            file_paths.append(ref.split('"')[1])

    for path in file_paths:
        filename = path.split('/')[-1]
        try:
            data = urllib.request.urlopen(path).read()
            with open(filename, 'wb') as filehandle:
                print("Opening {}.".format(path))
                filehandle.write(data)
        except urllib.request.HTTPError as e:
            if "404" in str(e):
                print("Could not find file: {}, continuing.".format(filename))
                continue


def guess_iteration():

    stub_url = "http://fileadmin.cs.lth.se/cs/Education/EDAN65/2015/lectures/L{}.pdf"

    iteration = 1
    suffix = ""
    while(True):
        iteration_num = "{:02d}".format(iteration)
        if iteration in [5, 6, 7]:
            if not suffix:
                suffix = "A"
            elif suffix == "A":
                suffix = "B"
            elif suffix == "B":
                iteration += 1
                suffix = ""
                continue
        else:
            suffix = ""
            iteration += 1
        if iteration >= 30:
            break
        if suffix:
            iteration_num += suffix;
        url = stub_url.format(iteration_num)
        print("trying: {}".format(url))
        try:
            data = urllib.request.urlopen(url).read()
        except urllib.error.HTTPError:
            print("HTTPError, continuing.")
            continue

        with open("L{}.pdf".format(iteration_num), 'wb') as filehandle:
            filehandle.write(data)

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "guess":
        guess_iteration()
    else:
        main(args)
