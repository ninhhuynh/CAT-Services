from django.core.management.base import BaseCommand
from similarity.models import SegmentPair, TranslationMemory
from translate.storage.tmx import tmxfile
import sys
from pathlib import Path


class Command(BaseCommand):
    help = 'Add Translation memory to database'

    def add_arguments(self, parser):
        parser.add_argument('tmpath', type=str,
                            help='path to the tm file')
        parser.add_argument('-n', '--name', type=str,
                            help='Define name for the tm', )
        parser.add_argument('-sl', '--srclang', type=str,
                            help='define srclang for the tm', )
        parser.add_argument('-tl', '--tgtlang', type=str,
                            help='define tgtlang for the tm', )

    def handle(self, *args, **kwargs):
        path = kwargs['tmpath']
        tmdata = {
            "name": kwargs['name'] if kwargs['name'] else Path(kwargs['tmpath']).stem,
            "src_lang": kwargs['srclang'] if kwargs['srclang'] else "unknown",
            "tgt_lang": kwargs['tgtlang'] if kwargs['tgtlang'] else "unknown",
        }
        print(tmdata)

        tm = TranslationMemory.objects.create(**tmdata)
        with open(path, 'rb') as fin:
            tmx_file = tmxfile(fin, 'en', 'ar')
        unitList = tmx_file.getunits()
        print("the tmx file has {} units".format(len(unitList)))
        objList = [SegmentPair(
            src_segment=node.source, tgt_segment=node.target, src=tm) for node in unitList]
        SegmentPair.objects.bulk_create(objList)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
