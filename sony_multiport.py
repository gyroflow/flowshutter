def init_multiport_packet():
    rcd_prs = b'#7100*'
    rcd_rls = b'#7110*'

    cm_hdsk = b'%000*'
    cm_hdsk_ack = b'&00080*'

    cm_rcd_hb = b'%7614*'
    cm_rcd_hb_ack = b'&761480*'

    return rcd_prs, rcd_rls, cm_hdsk, cm_hdsk_ack, cm_rcd_hb, cm_rcd_hb_ack