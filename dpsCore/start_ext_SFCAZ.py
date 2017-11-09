from E2XT.e2xt import run_sfcaz


run_sfcaz(
        omega=-4,
        v=-2.25,
        delta=0.05,
        region_name='kmch',
        mc_mag='3.5',
        mag_array=['7', '7,5', '8'],
        q='[-2.0; -3.0]',
        read_k='III',
        target_it=5
)

