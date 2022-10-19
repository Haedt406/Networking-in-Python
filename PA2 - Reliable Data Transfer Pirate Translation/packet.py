class packet():
    def __init__(self, seqNum, checkSum, ack_or_nak, length, message):
        self.seqNum = seqNum
        self.ack_or_nak = ack_or_nak
        self.checkSum = checkSum   
        self.length = length
        self.message = message
    def set_message(self,new_message):
        self.message = new_message
    def get_checkSum(self):
        return self.checkSum
    def get_AOK(self):
        return self.ack_or_nak
    def set_AON(self, AON):
        self.ack_or_nak = AON
    def get_len(self):
        return self.length
    def get_message(self):
        return self.message
    def get_seqNum(self):
        return self.seqNum    
    def set_checkSum(self, checkSum):
        self.checkSum = checkSum
