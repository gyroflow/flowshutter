def init_multiport_packet():
    record_press_packet = '#7100*'
    record_release_packet = '#7110*'

    camera_verify_packet = '%000*'
    camera_verify_packet_ack = '&00080*'

    camera_recording_packet = '%7614*'
    camrea_recording_packet_ack = '&76140*'

    return record_press_packet, record_release_packet, camera_verify_packet, camera_verify_packet_ack, camera_recording_packet, camrea_recording_packet_ack