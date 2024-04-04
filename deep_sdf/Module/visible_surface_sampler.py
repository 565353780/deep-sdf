import os
from concurrent.futures import ThreadPoolExecutor

from deep_sdf.Method.func import processMesh
from deep_sdf.Method.path import createFileFolder


class VisibleSurfaceSampler(object):
    def __init__(self, dataset_root_folder_path: str, num_threads: int = os.cpu_count()) -> None:
        self.dataset_root_folder_path = dataset_root_folder_path

        self.executor = ThreadPoolExecutor(max_workers=num_threads)
        return

    def sampleSDF(self) -> bool:
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

        specific_args = ["-n", normalization_param_filename]

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.submit(
                process_mesh,
                mesh_file_path,
                processed_filepath,
                srf_executable,
                specific_args + additional_general_args,
            )

            executor.shutdown()


