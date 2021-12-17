import os
import json
from glob import glob

for i in glob('tner_output/twitter_ner*/*'):
    if 'combine' not in i:
        continue
    h = '{}/metric.2nd.json'.format(i)
    if not os.path.exists(h):
        continue
    print('\n*************************')
    print('*** MODEL: {} ***'.format(i))
    print('*************************')
    with open(h) as f:
        tmp = json.load(f)
    _, best_metric = tmp[0]
    best_models = [t[0] for t in tmp if t[1] == best_metric]
    if len(best_models) > 1:
        print('\t WARNING: {} best models: {}'.format(len(best_models), best_models))
    best_model = best_models[0]
    best_model = '/'.join(best_model.split('/')[-2:])
    path_prefix = '/'.join(i.split('/')[:3])
    print('\t - model ckpt: {}'.format(best_model))
    with open('{}/{}/trainer_config.json'.format(path_prefix, os.path.dirname(best_model))) as f:
        config = json.load(f)
    print('\t - config')
    for k, v in config.items():
        print('\t\t{}: {}'.format(k, v))
    with open('{}/{}/eval/metric.json'.format(path_prefix, best_model)) as f:
        tmp = json.load(f)
        for k, v in tmp.items():
            print('\t - best micro f1 ({}) : {}'.format(k, v['micro/f1']))
    print()
