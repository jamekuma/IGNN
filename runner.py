#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# Developed by Shangchen Zhou <shangchenzhou@gmail.com>

import matplotlib
import os
# Fix problem: no $DISPLAY environment variable
matplotlib.use('Agg')

from argparse import ArgumentParser
from pprint import pprint

from config import cfg
from core.build import bulid_net
import torch
import os.path as osp

def get_args_from_command_line():
    parser = ArgumentParser(description='Parser of Runner of Network')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device to use', default=None, type=str)
    parser.add_argument('--phase', dest='phase', help='phase of CNN', default=cfg.NETWORK.PHASE, type=str)
    parser.add_argument('--scale', dest='scale', help='factor of upsampling', default=cfg.CONST.SCALE, type=int)
    parser.add_argument('--weights', dest='weights', help='Initialize network from the weights file', default=cfg.CONST.WEIGHTS, type=str)
    parser.add_argument('--dataroot', dest='dataset_root', help='Set dataset root_path', default=cfg.DIR.DATASET_ROOT, type=str)
    parser.add_argument('--testname', dest='testdata_name', help='Set test dataset name', default=cfg.DATASET.DATASET_TEST_NAME, type=str)
    parser.add_argument('--demopath', dest='demodata_path', help='Set demo test images path', default=cfg.DIR.IMAGE_LR_TEST_PATH, type=str)
    parser.add_argument('--out', dest='out_path', help='Set output path', default=cfg.DIR.OUT_PATH)
    args = parser.parse_args()
    return args

def main():
    # Get args from command line
    args = get_args_from_command_line()

    if args.out_path is not None:
        cfg.DIR.OUT_PATH = args.out_path
    if args.gpu_id is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_id
    if args.phase is not None:
        cfg.NETWORK.PHASE = args.phase
    if args.scale is not None:
        cfg.CONST.SCALE = args.scale
        cfg.DIR.DATASET_SCALE = 'x'+ str(cfg.CONST.SCALE)
        if args.weights is not None:
            cfg.CONST.WEIGHTS = args.weights
        else:
            cfg.CONST.WEIGHTS = osp.join(cfg.DIR.OUT_PATH, '/ckpt/IGNN_x' + str(cfg.CONST.SCALE) + '.pth')
    
    if args.dataset_root is not None:
        cfg.DIR.DATASET_ROOT = args.dataset_root
    if args.demodata_path is not None:
        cfg.DIR.IMAGE_LR_TEST_PATH = args.demodata_path
    
    
    if args.testdata_name is not None:
        cfg.DATASET.DATASET_TEST_NAME = args.testdata_name
        if cfg.DATASET.DATASET_TEST_NAME in ['Set5', 'Set14', 'BSDS100', 'Urban100', 'Manga109']:
            cfg.DIR.DATASET_JSON_TEST_PATH      = './datasets/json_files/'+cfg.DATASET.DATASET_TEST_NAME+'.json'
            cfg.DIR.IMAGE_LR_TEST_PATH          = cfg.DIR.DATASET_ROOT + cfg.DATASET.DATASET_TEST_NAME + '/LR_bicubic/'+cfg.DIR.DATASET_SCALE+'/{1}'+cfg.DIR.DATASET_SCALE+'.png'
            cfg.DIR.IMAGE_HR_TEST_PATH          = cfg.DIR.DATASET_ROOT + cfg.DATASET.DATASET_TEST_NAME + '/HR/{1}.png'
    if cfg.DATASET.DATASET_TRAIN_NAME == 'DIV2K':
        cfg.DIR.DATASET_JSON_TRAIN_PATH     = './datasets/json_files/DIV2K.json'
        cfg.DIR.IMAGE_LR_TRAIN_PATH         = cfg.DIR.DATASET_ROOT + 'DIV2K/DIV2K_{0}_LR_bicubic_sub/'+cfg.DIR.DATASET_SCALE+'/{1}.png'
        cfg.DIR.IMAGE_HR_TRAIN_PATH         = cfg.DIR.DATASET_ROOT + 'DIV2K/DIV2K_{0}_HR_sub/{1}.png'
        # __C.DIR.IMAGE_HR_TRAIN_PATH         = __C.DIR.DATASET_ROOT + 'DIV2K/DIV2K_{0}_HR_sub/'+__C.DIR.DATASET_SCALE+'/{1}.png'
    # For DIV2K validation
    if cfg.DATASET.DATASET_TEST_NAME == 'DIV2K_val':
        cfg.DIR.DATASET_JSON_TEST_PATH      = './datasets/json_files/DIV2K_val.json'
        cfg.DIR.IMAGE_LR_TEST_PATH          = cfg.DIR.DATASET_ROOT + 'DIV2K/DIV2K_{0}_LR_bicubic/'+cfg.DIR.DATASET_SCALE+'/{1}' + cfg.DIR.DATASET_SCALE + '.png'
        cfg.DIR.IMAGE_HR_TEST_PATH          = cfg.DIR.DATASET_ROOT + 'DIV2K/DIV2K_{0}_HR/{1}.png'

    cfg.CONST.NUM_GPU = torch.cuda.device_count()

    # Print config
    print('Use config:')
    pprint(cfg)

    # Set GPU to use
    print('Using GPUs NUMBER: '+ str(cfg.CONST.NUM_GPU))

    # set torch home
    os.environ['TORCH_HOME'] = './.cache'

    # Setup Network & Start train/test process
    bulid_net(cfg)

if __name__ == '__main__':
    main()
