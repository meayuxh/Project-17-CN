from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from os_ken.controller.handler import set_ev_cls
from os_ken.ofproto import ofproto_v1_3
from os_ken.lib.packet import packet, ethernet, ipv4, udp


class GameSDNController(app_manager.OSKenApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # Normal/default traffic
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_NORMAL)
        ]

        self.add_flow(datapath, 10, match, actions)

        # HIGH PRIORITY: Multiplayer game UDP traffic
        game_match = parser.OFPMatch(
            eth_type=0x0800,
            ip_proto=17,
            udp_dst=9999
        )

        game_actions = [
            parser.OFPActionOutput(ofproto.OFPP_NORMAL)
        ]

        self.add_flow(datapath, 100, game_match, game_actions)

        print("SDN SWITCH CONNECTED")
        print("GAME UDP PORT 9999 = HIGH PRIORITY")

    def add_flow(self, datapath, priority, match, actions):

        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        instructions = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]

        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=instructions
        )

        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):

        msg = ev.msg
        pkt = packet.Packet(msg.data)

        ip = pkt.get_protocol(ipv4.ipv4)
        udp_pkt = pkt.get_protocol(udp.udp)

        if ip and udp_pkt:

            if udp_pkt.dst_port == 9999:
                print(
                    f"[PRIORITY] GAME TRAFFIC "
                    f"{ip.src} -> {ip.dst}:9999"
                )
