def init_multiport_packet():
    rcd_prs = b'#7100*'
    rcd_rls = b'#7110*'

    cm_hdsk = b'%000*'
    cm_hdsk_ack = b'&00080*'

    cm_rcd_start = b'%7610*'
    cm_rcd_start_ack = b'&76100*'

    cm_rcd_stop  = b'%7600*'
    cm_rcd_stop_ack = b'&76000*'

    return rcd_prs, rcd_rls, cm_hdsk, cm_hdsk_ack, cm_rcd_start, cm_rcd_start_ack, cm_rcd_stop, cm_rcd_stop_ack