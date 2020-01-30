
def parse_line(file):
    """
    Go to next line and parse it, extract the first field and transform it in int.
    Ignore comments (line starting with #)

    :param file: the file to parse
    :type file: a file object
    :return: the position parsed
    :rtype: int
    :raise StopIteration: when reach the end of file
    """
    line = next(file)
    while line.startswith('#'):
        line = next(file)
    else:
        current_pos = int(line.split()[0])
    return current_pos, line


def diff_generator(txt_file, vcf_file):
    """
    create a generator which can iterate over line in vcf
    where position not appear in text file
    the position are extract from the first column of text_file and vcf_file.

    .. _warning:
        the position in the text_file and vcf_file must be sorted (ascending)

    :param txt_file: the text file to extract
    :type txt_file: file object
    :param vcf_file: the vcf to compare
    :type vcf_file: file object
    :return: a generator
    :rtype: generator
    """
    txt_pos, line = parse_line(txt_file)
    vcf_pos, _ = parse_line(vcf_file)
    vcf_end = False
    txt_end = False
    while True:
        if txt_pos == vcf_pos:
            try:
                vcf_pos, _ = parse_line(vcf_file)
            except StopIteration:
                vcf_end = True
            try:
                txt_pos, line = parse_line(txt_file)
            except StopIteration:
                txt_end = True
        elif txt_pos > vcf_pos:
            try:
                vcf_pos, _ = parse_line(vcf_file)
            except StopIteration:
                vcf_end = True
        else:  # txt_pos < vcf_pos
            yield line
            try:
                txt_pos, line = parse_line(txt_file)
            except StopIteration:
                txt_end = True
        if txt_end:
            break
        if vcf_end:
            yield line
            for line in txt_file:
                _, line = parse_line(line)  # to remove comment
                yield line


if __name__ == '__main__':
    import sys
    import os

    def usage():
        return "grep_vcf.py position_file"

    if len(sys.argv) != 2:
        # if there is no argument or more than 1
        # I print a message to the user and quit
        print(usage)
        raise RuntimeError()

    # I compute the name of the vcf according to the name of position text file
    text_path = sys.argv[1]
    vcf_path = os.path.splitext(text_path)[0] + '.vcf'

    vcf_path = os.path.splitext(text_path)[0] + '.vcf'

    # I test the existence of the text file and the vcf
    # if one of them does not exists
    # I quit
    for path in text_path, vcf_path:
        if not os.path.exists(vcf_path):
            raise FileNotFoundError(f"the file {path} does not exists.")
    # I open the both files
    # and parse them
    with open(text_path) as text, open(vcf_path) as vcf:
        for line in diff(text, vcf):
            print(line, end="")
