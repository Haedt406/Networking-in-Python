from operator import length_hint
import this


class packet:
    def __init__(seqNum, checkSum, ack_or_nak, length, message):
        this.seqNum = seqNum
        this.ack_or_nak = ack_or_nak
        this.checkSum = checkSum   
        this.length = length
        this.message = message

    def set_message(self,new_message):
        self.message = new_message
    
    def get_message(self):
        return self.message

    def get_sequence(self):
        return self.sequence_number
