# Run swig:

swig -python -c++ helloworld.i

# Compile with

ROOT=`python -c "import sys; print(sys.prefix)"`
VER=`python -c "import sys; print(sys.version[:3])"`
g++ -std=c++0x -fPIC -O -c -I$ROOT/include/python$VER \
         HelloWorld.cpp HelloWorld2.cpp helloworld_wrap.cxx
         g++ -std=c++0x -shared -o _helloworld.so HelloWorld.o HelloWorld2.o helloworld_wrap.o

# Test new module
python test.py
