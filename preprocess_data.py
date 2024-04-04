#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import os
import json
from subprocess import Popen, PIPE
from concurrent.futures import ThreadPoolExecutor

import deep_sdf.workspace as ws


def process_mesh(mesh_filepath, target_filepath, executable, additional_args):
    print(mesh_filepath + " --> " + target_filepath)
    command = [executable, "-m", mesh_filepath, "-o", target_filepath] + additional_args

    cmd = executable + ' -m ' + mesh_file_path + ' -o ' + target_filepath
    print(cmd)

    subproc = Popen(command, stdout=PIPE)
    subproc.wait()
    return

def append_data_source_map(data_dir, name, source):
    data_source_map_filename = ws.get_data_source_map_filename(data_dir)

    print("data sources stored to " + data_source_map_filename)

    data_source_map = {}

    if os.path.isfile(data_source_map_filename):
        with open(data_source_map_filename, "r") as f:
            data_source_map = json.load(f)

    if name in data_source_map:
        if not data_source_map[name] == os.path.abspath(source):
            raise RuntimeError(
                "Cannot add data with the same name and a different source."
            )

    else:
        data_source_map[name] = os.path.abspath(source)

        with open(data_source_map_filename, "w") as f:
            json.dump(data_source_map, f, indent=2)


if __name__ == "__main__":
    source_dir = "/home/chli/chLi/Dataset/ShapeNet/Core/ShapeNetCore.v2/"
    data_dir = "/home/chli/chLi/Dataset/ShapeNet/sdf/"
    data_dir = "./output/sdf/"
    num_threads = 8

    additional_general_args = []

    deepsdf_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
    srf_executable = deepsdf_dir + "bin/SampleVisibleMeshSurface"
    srf_subdir = "SurfaceSamples"
    srf_extension = ".ply"
    sdf_executable = deepsdf_dir + "bin/PreprocessMesh"
    sdf_subdir = "SdfSamples"
    sdf_extension = ".npz"

    srf_dest_dir = data_dir + srf_subdir + "/"
    sdf_dest_dir = data_dir + sdf_subdir + "/"

    print("source_dir:" + source_dir)
    print("srf_dest_dir:" + srf_dest_dir)
    print("sdf_dest_dir:" + sdf_dest_dir)

    os.makedirs(srf_dest_dir, exist_ok=True)
    os.makedirs(sdf_dest_dir, exist_ok=True)

    normalization_param_dir = data_dir + "NormalizationParameters/"
    os.makedirs(normalization_param_dir, exist_ok=True)

    processed_filepath = data_dir + "test.npz"

    mesh_folder_path = source_dir + "02691156/"

    mesh_filename_list = os.listdir(mesh_folder_path)

    mesh_file_path = (
        mesh_folder_path + mesh_filename_list[0] + "/models/model_normalized.obj"
    )

    specific_args = []

    normalization_param_filename = data_dir + "normalization_param.npz"


    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.submit(
            process_mesh,
            mesh_file_path,
            processed_filepath,
            srf_executable,
            specific_args + additional_general_args,
        )

        executor.shutdown()
