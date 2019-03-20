cd /home/isa22/lab2/sim
        source /software/scripts/init_msim6.2g
        rm vsim.wlf
        if [ ! -d work ]; then vlib work; fi
        vsim -c -do py-sim-script.tcl
        mv iir_filter_back.saif ../version0