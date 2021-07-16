from onmt.translate.translator import build_translator
from argparse import Namespace
import json
import pathlib

pathToModels = "translator/trainedmodels/"
modelsExt = ".pt"


class myTranslator:
    n_best = 5
    # passed opt should at least have models path

    def __init__(self, passedopt):
        self.opt = self.GetStandardOpt()
        for k, v in passedopt.items():
            if k == "models":
                for key, name in enumerate(v):
                    v[key] = ''.join([pathToModels, name, modelsExt])
            setattr(self.opt, k, v)

        self.translator = build_translator(self.opt, report_score=False)

    def Translate(self, srcText):
        return self.translator.translate([srcText], batch_size=self.opt.batch_size)

    def GetStandardOpt(self):
        opt = Namespace(align_debug=False, alpha=0.0, attn_debug=False,
                        avg_raw_probs=False, ban_unk_token=False, batch_size=30,
                        batch_type='sents', beam_size=5, beta=-0.0, block_ngram_repeat=0,
                        config=None, coverage_penalty='none', data_type='text', dump_beam='',
                        fp32=False, gpu=-1, ignore_when_blocking=[], int8=False, length_penalty='none',
                        log_file='', log_file_level='0', max_length=100, max_sent_length=None, min_length=0,
                        models=None, n_best=self.n_best, output="translatelog.txt", phrase_table='',
                        random_sampling_temp=1.0, random_sampling_topk=0, random_sampling_topp=0.0, ratio=-0.0,
                        replace_unk=False, report_align=False, report_time=False, save_config=None, seed=-1,
                        shard_size=10000, src=None, stepwise_penalty=False, tgt=None, tgt_prefix=False,
                        verbose=False)
        return opt
