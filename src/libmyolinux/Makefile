    all:
	gcc -c -Wall -Werror -fpic myolinux.c
	gcc -shared -o libmyolinux.so myolinux.o
	rm -f myolinux.o
	export LD_LIBRARY_PATH=$(LD_LIBRARY_PATH):`pwd`
	gcc -L`pwd` -Wall -o example example.c -lmyolinux

    clean:
	rm -f libmyolinux.so
	rm -f example
