#!/bin/bash
qemu-system-x86_64 \
    -m 256M \
    -cpu kvm64,+smep,+smap \
    -smp cores=2,threads=2 \
    -kernel bzImage \
    -hda ./rootfs.img \
    -nographic \
    -monitor /dev/null \
    -snapshot \
    -append "console=ttyS0 root=/dev/sda rw rdinit=/sbin/init kaslr pti=on ignore_loglevel oops=panic panic=1" \
    -drive file=./flag,if=virtio,format=raw,readonly=on \
    -no-reboot
