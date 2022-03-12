
INCLUDES=['/Library/Java/JavaVirtualMachines/jdk-17.0.2.jdk/Contents/Home/include', '/Library/Java/JavaVirtualMachines/jdk-17.0.2.jdk/Contents/Home/include/darwin']
CFLAGS=['-fno-strict-aliasing', '-Wno-write-strings', '-mmacosx-version-min=10.9', '-std=c++11', '-stdlib=libc++']
DEBUG_CFLAGS=['-O0', '-g', '-DDEBUG']
LFLAGS=['-L/Library/Java/JavaVirtualMachines/jdk-17.0.2.jdk/Contents/Home/lib', '-ljava', '-L/Library/Java/JavaVirtualMachines/jdk-17.0.2.jdk/Contents/Home/lib/server', '-ljvm', '-Wl,-rpath', '-Wl,/Library/Java/JavaVirtualMachines/jdk-17.0.2.jdk/Contents/Home/lib', '-Wl,-rpath', '-Wl,/Library/Java/JavaVirtualMachines/jdk-17.0.2.jdk/Contents/Home/lib/server', '-mmacosx-version-min=10.9']
IMPLIB_LFLAGS=[]
SHARED=True
VERSION="3.10"
