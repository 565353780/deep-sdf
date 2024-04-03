cd ..
git clone https://github.com/CLIUtils/CLI11
git clone https://gitlab.com/libeigen/eigen.git
git clone https://github.com/stevenlovegrove/Pangolin.git
git clone https://github.com/jlblancoc/nanoflann

cd CLI11
mkdir build
cd build
git submodule update --init
cmake ..
cmake --build .
sudo cmake --install .

cd ../../eigen
git checkout 3.4
mkdir build
cd build
cmake ..
sudo make install

cd ../../Pangolin
git checkout v0.6
sudo apt install ninja-build doxygen -y
git submodule update --init
mkdir build
cd build
cmake ..
cmake --build .
sudo make install

if [ "$(uname)" == "Darwin" ]; then
  brew install brewsci/science/nanoflann
elif [ "$(uname)" = "Linux" ]; then
  sudo apt install libnanoflann-dev
