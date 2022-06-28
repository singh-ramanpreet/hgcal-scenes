#!/bin/sh

for i in `seq 9 12`
do
    args="$args fh_layer_${i}L.pdf fh_layer_${i}R.pdf "
done

for i in `seq 1 12`
do
    args="$args bh_layer_${i}L.pdf bh_layer_${i}R.pdf "
done

pdfunite $args mixed_layers_tmp.pdf
gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -sOutputFile=mixed_layers.pdf mixed_layers_tmp.pdf
rm mixed_layers_tmp.pdf
