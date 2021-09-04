import json
import pandas as pd

class json2xlsx_err(object):

    def __init__(self):
        self.JSON_PATH = "./"
        self.XLSX_PATH = "./"
    
    def main(self):
        with open(self.JSON_PATH + "interfaces_error_counters.json") as json_file:
            data = json.load(json_file)

        data_new = []
        for item in data:
            dn = item['item']

            if dn is None:
                continue

            if len(item['imdata']) == 0:
                continue 

            tmp = {
                "dn"                            : dn, 

                # Dot1D Stats
                "Port in Discards"              : item['imdata'][0]['rmonDot1d']['attributes']['portInDiscards'],

                # Dot3 Stats
                "Allignment Errors"             : item['imdata'][2]['rmonDot3Stats']['attributes']['alignmentErrors'],
                "Carrier Sense Errors"          : item['imdata'][2]['rmonDot3Stats']['attributes']['carrierSenseErrors'],
                "Deferred Transmisstions"       : item['imdata'][2]['rmonDot3Stats']['attributes']['deferredTransmissions'],
                # "CRC Errors"                    : item['imdata'][2]['rmonDot3Stats']['attributes'][''],
                # "Stomped CRC Errors"            : item['imdata'][2]['rmonDot3Stats']['attributes'][''],
                "Internal Mac Receive Errors"   : item['imdata'][2]['rmonDot3Stats']['attributes']['internalMacReceiveErrors'],
                "Internal Mac Transmit Errors"  : item['imdata'][2]['rmonDot3Stats']['attributes']['internalMacTransmitErrors'],
                "Late Collisions"               : item['imdata'][2]['rmonDot3Stats']['attributes']['lateCollisions'],
                "Multiple Collision Frames"     : item['imdata'][2]['rmonDot3Stats']['attributes']['multipleCollisionFrames'],
                "SQETTest Errors"               : item['imdata'][2]['rmonDot3Stats']['attributes']['sQETTestErrors'],
                "Single Collision Frames"       : item['imdata'][2]['rmonDot3Stats']['attributes']['singleCollisionFrames'],
                "Symbol Errors"                 : item['imdata'][2]['rmonDot3Stats']['attributes']['symbolErrors'],
                
                # Ehternet Statstics Counters
                "CRC Align Errors"              : item['imdata'][1]['rmonEtherStats']['attributes']['cRCAlignErrors'],
                "Collisions"                    : item['imdata'][1]['rmonEtherStats']['attributes']['collisions']
            }
            data_new.append(tmp)
        
        df = pd.DataFrame(data_new)
        df.to_excel(self.XLSX_PATH + "인터페이스_에러.xlsx")

if __name__ == "__main__":
    func = json2xlsx_err()
    func.main()