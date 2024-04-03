cd ..
git clone https://github.com/CLIUtils/CLI11

sudo apt install ninja-build doxygen -y

cd CLI11
mkdir build
cd build
cmake ..
make -j
sudo cmake --install .

cd ../../deep-sdf/deep_sdf/Lib/eigen
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=./install ..
maks -j
make install

cd ../../Pangolin
cd external
git clone https://github.com/pybind/pybind11.git
cd ..
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=./install ..
make -j
make install

if [ "$(uname)" == "Darwin" ]; then
	brew install brewsci/science/nanoflann
elif [ "$(uname)" = "Linux" ]; then
	sudo apt install libnanoflann-dev
fi

cd ../../../..
mkdir build
cd build
cmake -DEigen3_DIR=./deep_sdf/Lib/eigen/build/install \
	-DPangolin_DIR=./deep_sdf/Lib/Pangolin/build/install \
	..
make -j
