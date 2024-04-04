#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import os
import json
import subprocess
import concurrent.futures

import deep_sdf
import deep_sdf.workspace as ws


def filter_classes_glob(patterns, classes):
    import fnmatch

    passed_classes = set()
    for pattern in patterns:
        passed_classes = passed_classes.union(
            set(filter(lambda x: fnmatch.fnmatch(x, pattern), classes))
        )

    return list(passed_classes)


def filter_classes_regex(patterns, classes):
    import re

    passed_classes = set()
    for pattern in patterns:
        regex = re.compile(pattern)
        passed_classes = passed_classes.union(set(filter(regex.match, classes)))

    return list(passed_classes)


def filter_classes(patterns, classes):
    if patterns[0] == "glob":
        return filter_classes_glob(patterns, classes[1:])
    elif patterns[0] == "regex":
        return filter_classes_regex(patterns, classes[1:])
    else:
        return filter_classes_glob(patterns, classes)


def process_mesh(mesh_filepath, target_filepath, executable, additional_args):
    print(mesh_filepath + " --> " + target_filepath)
    command = [executable, "-m", mesh_filepath, "-o", target_filepath] + additional_args

    subproc = subprocess.Popen(command, stdout=subprocess.DEVNULL)
    subproc.wait()


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
    data_dir = "/home/chli/chLi/Dataset/ShapeNet/sdf/"
    data_dir = "./output/sdf/"
    source_dir = "/home/chli/chLi/Dataset/ShapeNet/Core/ShapeNetCore.v2/"
    source_name = None
    split = False
    skip = True
    num_threads = 8
    test_sampling = False

    debug = True
    quiet = False
    log_file = None

    additional_general_args = []

    deepsdf_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
    srf_executable = deepsdf_dir + "bin/SampleVisibleMeshSurface"
    srf_subdir = "SurfaceSamples"
    srf_extension = ".ply"
    sdf_executable = deepsdf_dir + "bin/PreprocessMesh"
    sdf_subdir = "SdfSamples"
    sdf_extension = ".npz"

    if test_sampling:
        additional_general_args += ["-t"]

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

    specific_args = ["-n", normalization_param_filename]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.submit(
            process_mesh,
            mesh_file_path,
            processed_filepath,
            srf_executable,
            specific_args + additional_general_args,
        )

        executor.shutdown()
