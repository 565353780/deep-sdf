import os
from concurrent.futures import ThreadPoolExecutor

from deep_sdf.Method.func import processMesh
from deep_sdf.Method.path import createFileFolder


class SDFSampler(object):
    def __init__(self, dataset_root_folder_path: str, num_threads: int = os.cpu_count()) -> None:
        self.dataset_root_folder_path = dataset_root_folder_path

        self.executor = ThreadPoolExecutor(max_workers=num_threads)
        return

    def sampleSDF(self, mesh_file_path: str, save_sdf_file_path: str) -> bool:
        sdf_executable = "../deep-sdf/bin/PreprocessMesh"

        createFileFolder(save_sdf_file_path)

        normalization_param_dir = data_dir + "NormalizationParameters/"
        os.makedirs(normalization_param_dir, exist_ok=True)

        processed_filepath = data_dir + "test.npz"

        mesh_folder_path = self.dataset_root_folder_path + "02691156/"

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
                specific_args,
            )

            executor.shutdown()

        return True
