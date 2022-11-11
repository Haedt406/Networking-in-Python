#this is our data structure for a packet, when a packet is read in from 'packet.csv', the information is stored in this and then sent over a network,
#in this case from 'simulation.py' to 'network.py', where 'simulation' acts as a client and 'network' acts as the host
#packets are sent as a byte stream using 'pickle' library through 'sockets'

class packet(object):
    def __init__(self, src_ip_address, dst_ip_address,src_tl_port,dst_tl_port, protocol):
        self.src_ip_address = src_ip_address
        self.dst_ip_address = dst_ip_address
        self.src_tl_port = src_tl_port   
        self.dst_tl_port = dst_tl_port
        self.protocol = protocol

    def get_src_ip(self):
        return self.src_ip_address

    def get_dst_ip(self):
        return self.dst_ip_address

    def get_src_tl(self):
        return self.src_tl_port

    def get_dst_tl(self):
        return self.dst_tl_port

    def get_protocol(self):
        return self.protocol

    def set_protocol(self, protocol):
        self.protocol = protocol

    def set_src_ip(self,src_ip_address):
        self.src_ip_address = src_ip_address

    def set_dst_ip(self, dst_ip_address):
        self.dst_ip_address = dst_ip_address

    def set_dst_tl(self,dst_tl_port):
        self.dst_tl_port = dst_tl_port

    def set_src_tl(self,src_tl_port):
        self.src_tl_port = src_tl_port
        
        
