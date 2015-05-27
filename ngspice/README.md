# Installing ngspice-26 on Ubuntu (a quick guide)

Prequisites:

    $ sudo apt-get install libreadline6-dev libopenmpi-dev libxaw7 libxaw7-dev

Install ngspice:

    $ tar -zxvf ngspice-26.tar.gz
    $ cd ngspice-26
    $ mkdir release
    $ cd release
    $ ../configure --with-x --enable-xspice --disable-debug --enable-cider --with-readline=yes --enable-openmp
    $ make 2>&1 | tee make.log
    $ sudo make install

For a detailed installation guide, see the "INSTALL" file which come along with the ngspice source code tarball.
